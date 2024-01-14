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
# df_rent1 = pd.concat([df_rent1_4,df_rent1_5,df_rent1_6],axis=0)
# 데이터가 많아서 streamlit share에서 에러나서 일단 파일 하나로만 테스트 진행
df_rent1 = df_rent1_4

# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent1['기준_날짜'] = df_rent1['기준_날짜'].astype('str')
 
## 국가 목록 가져오기
std_date = df_rent1['기준_날짜'].unique()
 
## 선택 상자 생성
sel_date = st.selectbox('날짜 선택:', std_date)
 
## 데이터 필터링
filtered_data = df_rent1[df_rent1['기준_날짜'] == sel_date]
 
## 필터링된 데이터 표시
st.write(filtered_data)