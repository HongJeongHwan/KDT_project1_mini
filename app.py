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
# 그냥 한번 해봤어..
# 날짜별 데이터 합치기
# df_rent1 = pd.concat([df_rent1_4,df_rent1_5,df_rent1_6],axis=0)
# 데이터가 많아서 streamlit share에서 에러나서 일단 파일 하나로만 테스트 진행
df_rent1 = df_rent1_4

# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent1['기준_날짜'] = df_rent1['기준_날짜'].astype('str')
df_rent1['기준_날짜'] = pd.to_datetime(df_rent1['기준_날짜'], format='%Y-%m-%d')

# 컬럼명 영문으로 변경
df_rent1.rename(columns={'기준_날짜':'std_date','집계_기준':'type','기준_시간대':'std_time','시작_대여소_ID':'st_spot_id',
                         '시작_대여소명':'st_spot_name','종료_대여소_ID':'end_spot_id','종료_대여소명':'end_spot_name',
                         '전체_건수':'tot_count','전체_이용_분':'tot_use_min','전체_이용_거리':'tot_dist'}, inplace=True)
# 조회조건 설정 =======================================================================

# 기준날짜
# 컬럼명 한글일때 -----------------------------------------------------------------
# std_date = df_rent1['기준_날짜'].value_counts(ascending=False)[:].index.to_list()
# std_date.insert(0,'전체')
# std_date = tuple(std_date)

# # 시작대여소 : 사용량이 많은 순으로 n개 보여줌
# st_rent_id = df_rent1['시작_대여소_ID'].value_counts(ascending=False)[:].index.to_list()
# st_rent_id.insert(0,'전체')
# st_rent_id = tuple(st_rent_id)

# # 시작대여소 : 사용량이 많은 순으로 n개 보여줌
# end_rent_id = df_rent1['종료_대여소_ID'].value_counts(ascending=False)[:].index.to_list()
# end_rent_id.insert(0,'전체')
# end_rent_id = tuple(end_rent_id)

# 컬럼명 영문일때 -----------------------------------------------------------------
std_date = df_rent1['std_date'].value_counts(ascending=False)[:].index.to_list()
std_date.insert(0,'선택하세요.')
std_date = tuple(std_date)

# 시작대여소 : 사용량이 많은 순으로 n개 보여줌
st_rent_id = df_rent1['st_spot_id'].value_counts(ascending=False)[:].index.to_list()
st_rent_id.insert(0,'선택하세요.')
st_rent_id = tuple(st_rent_id)

# 시작대여소 : 사용량이 많은 순으로 n개 보여줌
end_rent_id = df_rent1['end_spot_id'].value_counts(ascending=False)[:].index.to_list()
end_rent_id.insert(0,'선택하세요.')
end_rent_id = tuple(end_rent_id)



# 화면 구성 ============================================================================
st.title('서울시 따릉이 정보분석')
st.header('1단계 : 날짜별, 대여소별 건수, 이용시간, 이용거리 분석')


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
        '시작대여소',
        # selectbox 구성요소(튜플의 형태로)
        (st_rent_id)
    )
    
with col3:
    sel_end_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '종료대여소',
        # selectbox 구성요소(튜플의 형태로)
        (end_rent_id)
    )

############################################################################################
# 조회버튼 : 버튼 클릭하면 조회하는 것으로 변경 (조회내용 : 시작)
############################################################################################

if st.button('위의 조건으로 데이터 프레임 출력하기'):
    # 조회조건 지정 : 날짜, 시작대여소, 종료대여소
    # 컬럼명 한글일때 -----------------------------------------------------------------
    # cond_date = df_rent1['기준_날짜']==sel_date
    # cond_st = df_rent1['시작_대여소_ID']==sel_st_rent_id
    # cond_end = df_rent1['종료_대여소_ID']==sel_end_rent_id
    # 컬럼명 영문일때 -----------------------------------------------------------------
    cond_date = df_rent1['std_date']==sel_date
    cond_st = df_rent1['st_spot_id']==sel_st_rent_id
    cond_end = df_rent1['end_spot_id']==sel_end_rent_id
    
    # DataFrame 보여주기(하드코딩) : 아래 코드 해결되면 대체예정 
    if sel_date=='전체':
        if sel_st_rent_id=='전체':
            if sel_end_rent_id=='전체':
                cond = ""
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

    # 차트 보여주기
    col_plt1, col_plt2, col_plt3 = st.columns(3)

    fig1, ax1 = plt.subplots()

    ## col1 --> 그래프 생성
    with col_plt1:
        # sns.histplot() 실행
        st.subheader('건수')
        # 일단 전체 조회안되게 막음
        # if cond=="":
        #     sns.countplot(data=df_rent1.loc[:,:], x='전체_건수', ax=ax1)
        # else:
        #     sns.countplot(data=df_rent1.loc[cond,:], x='전체_건수', ax=ax1)
        # sns.countplot(data=df_rent1.loc[cond,:], x='전체_건수', ax=ax1)     # 한글일때
        sns.countplot(data=df_rent1.loc[cond,:], x='tot_count', ax=ax1)     # 영문일때
        st.pyplot(fig1)

    with col_plt2:
        # sns.histplot() 실행
        st.subheader('이용시간(분)')
        # 일단 전체 조회안되게 막음
        # if cond=="":
        #     sns.countplot(data=df_rent1.loc[:,:], x='전체_이용_분', ax=ax1)
        # else:
        #     sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_분', ax=ax1)
        # sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_분', ax=ax1)  # 한글
        sns.countplot(data=df_rent1.loc[cond,:], x='tot_use_min', ax=ax1)   # 영문
        st.pyplot(fig1)

    with col_plt3:
        # sns.histplot() 실행
        st.subheader('이용거리(m)')
        # 일단 전체 조회안되게 막음
        # if cond=="":
        #     sns.countplot(data=df_rent1.loc[:,:], x='전체_이용_거리', ax=ax1)
        # else:
        #     sns.countplot(data=df_rent1.loc[cond,:], x='전체_이용_거리', ax=ax1)
        # sns.histplot(data=df_rent1.loc[cond,:], x='전체_이용_거리', ax=ax1) # 한글
        sns.histplot(data=df_rent1.loc[cond,:], x='tot_dist', ax=ax1) # 영문
        st.pyplot(fig1)

############################################################################################
# 조회버튼 : 버튼 클릭하면 조회하는 것으로 변경 (조회내용 : 끝)
############################################################################################