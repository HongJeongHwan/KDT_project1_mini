import pandas as pd
import streamlit as st

# 파일불러오기
file_path = 'tpss_bcycl_od_statnhm_20240106.csv'
df_rent1 = pd.read_csv(file_path,encoding='cp949')

s_rent = df_rent1['시작_대여소_ID'].value_counts(ascending=False)[:10].index
tpl_rent = tuple(s_rent)


st.title('서울시 따릉이 대여소 대여건수')




# sidebar 설치 + selectbox 추가
selected_id = st.selectbox(
    # selectbox 위의 설명글
    '조회할 대여소 ID를 선택해 주세요.',
    # selectbox 구성요소(튜플의 형태로)
    (tpl_rent)
)

cond = df_rent1['시작_대여소_ID']==selected_id
st.write(df_rent1.loc[cond,'종료_대여소_ID'].value_counts(ascending=False))




