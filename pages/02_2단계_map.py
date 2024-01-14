import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 데이터 불러오기 : 마스터파일
file_path = './data/서울시 따릉이대여소 마스터 정보.csv'
df_master = pd.read_csv(file_path,encoding='cp949')


# 데이터 전처리

# 경도,위도 컬럼명 변경 : map
df_master.rename(columns={'위도':'lat','경도':'lon'}, inplace = True)

# 이상치 처리(실질적 Nan Data 제거)
# df_master.loc[:,['lat','lon']].plot(kind='box')
# plt.show()

# 경도, 위도가 0인 컬럼이 77개 존재 : 삭제처리
cond = (df_master['lat']==0) | (df_master['lon']==0)
# df_master.loc[cond,:].index
df_master1 = df_master.drop(df_master.loc[cond,:].index,axis=0)
df_master1.reset_index(inplace=True)


###################################################################################
# 화면 출력
###################################################################################
st.header('2_1단계 : 대여소 정보를 지도에 시각화')
st.write(df_master1)
st.map(df_master1) 
'''
숙제 : 마스터 데이터로는 경도,위도 정보가 있는 대여소의 위치만 표시
        추후에 메인의 대여정보 데이터에 경도,위도 컬럼을 추가하여 데이터 표시 해보자.    
'''
