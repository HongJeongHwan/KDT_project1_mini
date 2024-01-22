import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# 파일불러오기
file_path1_4 = './data/tpss_bcycl_od_statnhm_20240104.csv'
file_path1_5 = './data/tpss_bcycl_od_statnhm_20240105.csv'
file_path1_6 = './data/tpss_bcycl_od_statnhm_20240106.csv'

df_rent1_4 = pd.read_csv(file_path1_4,encoding='cp949')
df_rent1_5 = pd.read_csv(file_path1_5,encoding='cp949')
df_rent1_6 = pd.read_csv(file_path1_6,encoding='cp949')

# 전처리

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



 
# 조회조건 설정 =======================================================================

# 날짜 목록 가져오기
std_date = df_rent1['기준_날짜'].unique()
std_date = np.insert(std_date,0,'선택하세요.')

# 시작대여소 목록 가져오기
st_rent_id = df_rent1['시작_대여소_ID'].unique()
st_rent_id = np.insert(st_rent_id,0,'선택하세요.')

# 종료대여소 목록 가져오기
end_rent_id = df_rent1['종료_대여소_ID'].unique()
end_rent_id = np.insert(end_rent_id,0,'선택하세요.')



# 화면 구성 ============================================================================
st.header('■ KDT mini porject (1조)')
st.subheader(': 서울시 공공자전거 "따릉이" 데이터 수집 및 분석')
st.subheader('')
st.subheader('- 1단계: 날짜, 대여소별 건수, 이용시간 및 거리 분석')
st.subheader('')

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
    sel_st_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '시작_대여소_ID',
        # selectbox 구성요소(튜플의 형태로)
        (st_rent_id)
    )  

with col3:
    # selectbox 
    sel_end_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '종료_대여소_ID',
        # selectbox 구성요소(튜플의 형태로)
        (end_rent_id)
    ) 


# 데이터 필터링 조건 지정 : 날짜, 시작대여소, 종료대여소
# cond = pd.Series('')
# cond = ''

if sel_date!='선택하세요.':
    cond_date = (df_rent1['기준_날짜']==sel_date)
    IsSelected_date = True
else:
    IsSelected_date = False
    
if sel_st_rent_id!='선택하세요.':
    cond_st = (df_rent1['시작_대여소_ID']==sel_st_rent_id)
    IsSelected_st_rent_id = True
else:
    IsSelected_st_rent_id = False
    
if sel_end_rent_id!='선택하세요.':
    cond_end = (df_rent1['종료_대여소_ID']==sel_end_rent_id)
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



## 필터링된 데이터 표시
if ((IsSelected_date==True) | (IsSelected_st_rent_id==True) | (IsSelected_end_rent_id==True)):
    st.subheader('데이터프레임 출력')
    st.write(df_rent1.loc[cond,:])
    st.subheader('')
    
# 차트 보여주기
    st.subheader('통계 그래프 시각화')
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