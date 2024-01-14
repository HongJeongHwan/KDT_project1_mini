import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기 : 마스터파일
file_path = './data/SeoulBikeData.csv'
df_weather = pd.read_csv(file_path,encoding='cp949')


# 데이터 전처리
# 한글이 깨진 컬럼명 변경
df_weather.rename(columns={'Temperature(캜)':'Temperature',
                           'Dew point temperature(캜)':'Dew point temperature'},inplace=True)

# Date 컬럼을 Datetime으로 변경
df_weather['Date'] = pd.to_datetime(df_weather['Date'])

# Month 컬럼 추가
df_weather['Month'] = pd.to_datetime(df_weather['Date']).dt.month



###################################################################################
# 화면 출력
###################################################################################
st.header('3단계 : 날씨 정보와 연관성 시각화')
st.write(df_weather)

'''
숙제 : 현재 데이터를 대여기록과 연계해.. 날씨데이터와 대여건수를 비교분석해보자.    
'''