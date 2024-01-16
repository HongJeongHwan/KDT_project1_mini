import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns


# matplotlib 한글사용을 위한 코드
matplotlib.rcParams['font.family'] = 'Malgun Gothic'


# 파일불러오기
file_path1_4 = './data/tpss_bcycl_od_statnhm_20240104.csv'
file_path1_5 = './data/tpss_bcycl_od_statnhm_20240105.csv'
file_path1_6 = './data/tpss_bcycl_od_statnhm_20240106.csv'

df_rent1_4 = pd.read_csv(file_path1_4,encoding='cp949')
df_rent1_5 = pd.read_csv(file_path1_5,encoding='cp949')
df_rent1_6 = pd.read_csv(file_path1_6,encoding='cp949')

# 전처리 =======================================================================

# 날짜별 데이터 합치기
df_rent1 = pd.concat([df_rent1_4,df_rent1_5,df_rent1_6],axis=0)
# 데이터가 많아서 streamlit share에서 에러나서 일단 파일 하나로만 테스트 진행
# df_rent1 = df_rent1_4

# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent1['기준_날짜'] = df_rent1['기준_날짜'].astype('str')
# df_rent1['기준_날짜'] = pd.to_datetime(df_rent1['기준_날짜'], format='%Y-%m-%d')

# 컬럼명 영문으로 변경
# df_rent1.rename(columns={'기준_날짜':'std_date','집계_기준':'type','기준_시간대':'std_time','시작_대여소_ID':'st_spot_id',
#                          '시작_대여소명':'st_spot_name','종료_대여소_ID':'end_spot_id','종료_대여소명':'end_spot_name',
#                          '전체_건수':'tot_count','전체_이용_분':'tot_use_min','전체_이용_거리':'tot_dist'}, inplace=True)

# 대여소명에 '동'이 표시되어 있지 않은 행 찾기 : 182개 존재
# cond_dong = df_rent1['시작_대여소명'].str.contains('동')
# df_rent1.loc[~cond_dong,:]

# 종료_대여소명 : NaN --> X
df_rent1['종료_대여소명'].fillna('X',inplace=True)



# Feature Engineering
# df_featured_rent : '시작_대여소_동명', '종료_대여소_동명' 추출
df_featured_rent = df_rent1
df_featured_rent['시작_대여소_동명'] = df_rent1['시작_대여소명'].apply(lambda x:x[:x.find('동')+1])
df_featured_rent['종료_대여소_동명'] = df_rent1['종료_대여소명'].apply(lambda x:x[:x.find('동')+1])

# 동별정보를 추가한 df_featured_rent에서 동명이 없는 행을 삭제
cond = ((df_featured_rent['시작_대여소_동명']=='') | (df_featured_rent['종료_대여소_동명']==''))
df_featured_rent.drop(df_featured_rent.loc[cond,:].index, axis=0, inplace=True)

 
# 조회조건 설정 =======================================================================

# 날짜 목록 가져오기
std_date = df_rent1['기준_날짜'].unique()
std_date = np.insert(std_date,0,'선택하세요.')

# 시작대여소 목록 가져오기
st_rent_name = df_rent1['시작_대여소명'].unique()
st_rent_name = np.insert(st_rent_name,0,'선택하세요.')

# 종료대여소 목록 가져오기
end_rent_name = df_rent1['종료_대여소명'].unique()
end_rent_name = np.insert(end_rent_name,0,'선택하세요.')



# 화면 구성 ============================================================================
st.title('■ KDT mini Project (七面鳥)')
st.subheader('1단계: 따릉이 대여소 데이터 수집 및 분석')
st.subheader('')
st.subheader('- 날짜, 대여소별 건수, 이용시간 및 거리 분석')
st.write('개요 : 특정날짜에 빌린대여소, 반납대여소별 이용건수, 이용시간, 이용거리정보를 가지고 있는 csv파일을 불러와서 \
            DataFrame으로 만든다음 화면에 출력한다.')
st.write('빌린날짜, 빌린대여소명, 반납대여소명을 조회조건으로 지정후 조건에 맞는 데이터를 Boolean Indexing을 통해 \
         조회조건을 만족하는 행만 화면에 출력한다.')
    # 코드보기
with st.expander('Boolean Indexing 코드보기'):
    code = '''
    cond1 = (df_rent1['기준_날짜']=='2024-01-05')
    cond2 = (df_rent1['시작_대여소_ID']=='목5동_059_1')
    cond3 = (df_rent1['종료_대여소_ID']=='강일동_001_1')
    cond = cond1 & cond2 & cond3
    df_rent1.loc[cond,:]'''
    st.code(code, language='python')

## 선택 상자 생성
# 조회조건 layout
col1, col2, col3 = st.columns(3)

# 컬럼별 소제목 지정
# col1.subheader("날짜 선택")
# col2.subheader("시작대여소 선택")
# col3.subheader("종료대여소 선택")

with col1:
    # selectbox 
    sel_date = st.selectbox(
        # selectbox 위의 설명글
        '날짜',
        # selectbox 구성요소(튜플의 형태로)
        (std_date)
    )

with col2:
    # selectbox 
    sel_st_rent_name = st.selectbox(
        # selectbox 위의 설명글
        '시작_대여소명',
        # selectbox 구성요소(튜플의 형태로)
        (st_rent_name)
    )  

with col3:
    # selectbox 
    sel_end_rent_name = st.selectbox(
        # selectbox 위의 설명글
        '종료_대여소명',
        # selectbox 구성요소(튜플의 형태로)
        (end_rent_name)
    ) 


# 데이터 필터링 조건 지정 : 날짜, 시작대여소, 종료대여소
cond = pd.Series('')
cond = ''

if sel_date!='선택하세요.':
    cond_date = (df_rent1['기준_날짜']==sel_date)
    IsSelected_date = True
else:
    IsSelected_date = False
    
if sel_st_rent_name!='선택하세요.':
    cond_st = (df_rent1['시작_대여소명']==sel_st_rent_name)
    IsSelected_st_rent_id = True
else:
    IsSelected_st_rent_id = False
    
if sel_end_rent_name!='선택하세요.':
    cond_end = (df_rent1['종료_대여소명']==sel_end_rent_name)
    IsSelected_end_rent_id = True
else:
    IsSelected_end_rent_id = False

if IsSelected_date == True:
    if IsSelected_st_rent_id == True:
        if IsSelected_end_rent_id == True:
            cond = cond_date & cond_st & cond_end
        else:
            cond = cond_date & cond_st
    else:
        if IsSelected_end_rent_id == True:
            cond = cond_date & cond_end
        else:
            cond = cond_date
else:
    if IsSelected_st_rent_id == True:
        if IsSelected_end_rent_id == True:
            cond = cond_st & cond_end
        else:
            cond = cond_st
    else:
        if IsSelected_end_rent_id == True:
            cond = cond_end
        # else:
        #     IsNoSelected = True



# 필터링된 데이터 표시
if ((IsSelected_date==True) | (IsSelected_st_rent_id==True) | (IsSelected_end_rent_id==True)):

    # 기본정보 DataFrame 출력 : 지정된 조건
    st.subheader('▷ 기본정보 데이터프레임 출력')
    st.write(df_rent1.loc[cond,:].sort_values(by=['기준_날짜','시작_대여소명','종료_대여소명']))
    st.subheader('')

    # 기본정보 차트 출력 : 지정된 조건
    st.subheader('▷ 기본정보 통계그래프 시각화')
    st.write('개요 : 기본정보를 데이터프레임에 출력한 것을 기반으로 이용건수, 이용시간, 이용거리를 시각화')
    
    col_plt1, col_plt2, col_plt3 = st.columns(3)

    fig1, ax1 = plt.subplots()

    ## col1 --> 그래프 생성
    with col_plt1:
        # sns.histplot() 실행
        st.subheader('건수')
        sns.countplot(data=df_rent1.loc[cond,:], x='전체_건수', ax=ax1)
        st.pyplot(fig1)

    with col_plt2:
        # sns.histplot() 실행
        st.subheader('이용시간(분)')
        sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_분', ax=ax1)
        st.pyplot(fig1)

    with col_plt3:
        # sns.histplot() 실행
        st.subheader('이용거리(m)')
        sns.histplot(data=df_rent1.loc[cond,:], x='전체_이용_거리', ax=ax1)
        st.pyplot(fig1)

    
    # Groupby.smu() DataFrame 출력 : 지정된 조건
    st.write('')
    st.write('')
    st.subheader('- 날짜, 동별 건수, 이용시간 및 거리 분석')
    st.subheader('▷ Feature Engineering')
    st.write('개요 : 대여소 컬럼에서 "동"정보을 추출해 새로운 컬럼을 생성')
    st.write('대여소의 정보가 3천여개로 너무 많아 의미있는 분석이 어려워, 동별정보를 만든 다음 이를 분석진행')
    # 코드보기
    with st.expander('기존 컬럼에서 동명 추출하는 코드보기'):
        code = '''
        # Feature Engineering
        # df_featured_rent : '시작_대여소_동명', '종료_대여소_동명' 추출
        df_featured_rent = df_rent1
        df_featured_rent['시작_대여소_동명'] = df_rent1['시작_대여소명'].apply(lambda x:x[:x.find('동')+1])
        df_featured_rent['종료_대여소_동명'] = df_rent1['종료_대여소명'].apply(lambda x:x[:x.find('동')+1])'''
        st.code(code, language='python')

    st.subheader('▷ Data Preprocessing')
    st.write('"동"명이 없는 행은 제거')
    # 코드보기
    with st.expander('동명이 없는 행 제거하는 코드보기'):
        code = '''
        cond = ((df_featured_rent['시작_대여소_동명']=='') | (df_featured_rent['종료_대여소_동명']==''))
        df_featured_rent.drop(df_featured_rent.loc[cond,:].index, axis=0, inplace=True)'''
        st.code(code, language='python')

    st.subheader('▷ 동별 합계데이터의 데이터프레임 출력')
    # 코드보기
    with st.expander('동별 합계데이터 생성코드 보기'):
        code = '''
        df_featured_rent.groupby(['시작_대여소_동명'])
        .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})
        .sort_values(by=['전체_건수','전체_이용_분','전체_이용_거리'],ascending=False)'''
        st.code(code, language='python')
    # st.write(df_rent1.groupby(['기준_날짜','시작_대여소_ID','종료_대여소_ID']).agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum}))
    
    st.write('개요 : 빌린대여소명을 기준으로 groupby.sum()을 한 결과를 전체_건수,전체이용_분,전체이용_거리순으로 정렬해서 보여준다.')
    st.write('단, 조회할 동의 개수를 선택하면 선택한 개수만큼만 보여준다.')
    # selectbox
    # 전체 동의 개수를 구하기 위해 df_for_count을 저장
    df_for_count = df_featured_rent.groupby(['시작_대여소_동명'])\
        .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})\
        .sort_values(by=['전체_건수','전체_이용_분','전체_이용_거리'],ascending=False).shape[0]

    sel_dong = st.selectbox(
        # selectbox 위의 설명글
        '데이터프레임으로 볼 동의 개수 선택',
        # selectbox 구성요소(튜플의 형태로)
        (np.arange(10,df_for_count+1))
    )

    df_featured_rent_sum = df_featured_rent.groupby(['시작_대여소_동명'])\
        .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})\
        .sort_values(by=['전체_건수','전체_이용_분','전체_이용_거리'],ascending=False).iloc[:sel_dong,:]
    
    st.write(df_featured_rent_sum)
    st.subheader('')

    st.subheader('▷ 동별 합계데이터의 시각화')

    fig2, ax2 = plt.subplots()

    # sns.histplot() 실행
    st.subheader('동별 이용건수')
    sns.barplot(data=df_featured_rent_sum,x='시작_대여소_동명',y='전체_건수',ax=ax2)
    st.pyplot(fig2)
    sns.barplot(data=df_featured_rent_sum,x='시작_대여소_동명',y='전체_이용_분',ax=ax2)
    st.pyplot(fig2)
    sns.barplot(data=df_featured_rent_sum,x='시작_대여소_동명',y='전체_이용_거리',ax=ax2)
    st.pyplot(fig2)
    