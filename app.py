import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# 파일불러오기
file_path1_4 = 'tpss_bcycl_od_statnhm_20240104.csv'
file_path1_5 = 'tpss_bcycl_od_statnhm_20240105.csv'
file_path1_6 = 'tpss_bcycl_od_statnhm_20240106.csv'

df_rent1_4 = pd.read_csv(file_path1_4,encoding='cp949')
df_rent1_5 = pd.read_csv(file_path1_5,encoding='cp949')
df_rent1_6 = pd.read_csv(file_path1_6,encoding='cp949')

# 전처리

# 날짜별 데이터 합치기
df_rent1 = pd.concat([df_rent1_4,df_rent1_5,df_rent1_6],axis=0)

# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent1['기준_날짜'] = df_rent1['기준_날짜'].astype('str')
df_rent1['기준_날짜'] = pd.to_datetime(df_rent1['기준_날짜'], format='%Y-%m-%d')

# 조회조건 설정 =======================================================================

# 기준날짜
std_date = df_rent1['기준_날짜'].value_counts(ascending=False)[:].index.to_list()
std_date.insert(0,'전체')
std_date = tuple(std_date)

# 시작대여소 : 사용량이 많은 순으로 10개 보여줌
st_rent_id = df_rent1['시작_대여소_ID'].value_counts(ascending=False)[:].index.to_list()
st_rent_id.insert(0,'전체')
st_rent_id = tuple(st_rent_id)

# 시작대여소 : 사용량이 많은 순으로 10개 보여줌
end_rent_id = df_rent1['종료_대여소_ID'].value_counts(ascending=False)[:].index.to_list()
end_rent_id.insert(0,'전체')
end_rent_id = tuple(end_rent_id)





# 화면 구성 ============================================================================
st.title('서울시 따릉이 대여소 대여건수')


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
        '날짜 선택',
        # selectbox 구성요소(튜플의 형태로)
        (std_date)
    )
    
with col2:
    # selectbox 
    sel_st_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '시작대여소 선택',
        # selectbox 구성요소(튜플의 형태로)
        (st_rent_id)
    )
    
with col3:
    sel_end_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '종료대여소 선택',
        # selectbox 구성요소(튜플의 형태로)
        (end_rent_id)
    )

# 조회조건 지정 : 날짜, 시작대여소, 종료대여소
cond_date = df_rent1['기준_날짜']==sel_date
cond_st = df_rent1['시작_대여소_ID']==sel_st_rent_id
cond_end = df_rent1['종료_대여소_ID']==sel_end_rent_id

# DataFrame 보여주기(하드코딩) : 아래 코드 해결되면 대체예정 
if sel_date=='전체':
    if sel_st_rent_id=='전체':
        if sel_end_rent_id=='전체':
            cond = ''
            st.write(df_rent1.loc[:,:])
        else:
            cond = cond_end
            st.write(df_rent1.loc[cond,:])
            
    else:
        if sel_end_rent_id=='전체':
            cond = cond_st
            st.write(df_rent1.loc[cond,:])
        else:
            cond = cond_st & cond_end
            st.write(df_rent1.loc[cond,:])
else:
    if sel_st_rent_id=='전체':
        if sel_end_rent_id=='전체':
            cond = cond_date
            st.write(df_rent1.loc[cond,:])
        else:
            cond = cond_date & cond_end
            st.write(df_rent1.loc[cond,:])
    else:
        if sel_end_rent_id=='전체':
            cond = cond_date & cond_st
            st.write(df_rent1.loc[cond,:])
        else:
            cond = cond_date & cond_st & cond_end
            st.write(df_rent1.loc[cond,:])
    
#########################################################################
# # 문제 해결이 안되어서 일단 보류 : 나중에 다시 시도해 보자(위의 코드 대체)
#########################################################################
# cond = ''

# if sel_date!='전체':
#     cond_date = "(df_rent1['기준_날짜']=='" + str(sel_date) + "')"
#     cond = cond + " & " + cond_date

# if sel_st_rent_id!='전체':
#     cond_st = "(df_rent1['시작_대여소_ID']=='" + sel_st_rent_id + "')"
#     cond = cond + " & " + cond_st 

# if sel_end_rent_id!='전체':
#     cond_end = "(df_rent1['종료_대여소_ID']=='" + sel_end_rent_id + "')"
#     cond = cond + " & " + cond_end 

# if cond=='':
#     # cond=':'
#     st.write(df_rent1.loc[:,:])
# else:
#     cond=cond[3:]
#     st.write(df_rent1.loc[cond,:]) 

# DataFrame 보여주기
# st.write(df_rent1.loc[cond,'종료_대여소_ID'].value_counts(ascending=False))
# st.write(df_rent1.loc[cond,:])
# st.write(df_rent1.loc[:,:])
#########################################################################





col_plt1, col_plt2, col_plt3 = st.columns(3)


fig1, ax1 = plt.subplots()

## col1 --> 그래프 생성
with col_plt1:
    # sns.histplot() 실행
    st.subheader('전체 건수')
    sns.countplot(data=df_rent1.loc[cond,:], x='전체_건수', ax=ax1)
    st.pyplot(fig1)

with col_plt2:
    # sns.histplot() 실행
    st.subheader('전체 이용시간(분)')
    sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_분', ax=ax1)
    st.pyplot(fig1)

with col_plt3:
    # sns.histplot() 실행
    st.subheader('전체 이용거리(m)')
    sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_거리', ax=ax1)
    st.pyplot(fig1)

