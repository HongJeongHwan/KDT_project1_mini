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
# df_weather['Date'] = pd.to_datetime(df_weather['Date'])

# Month 컬럼 추가
# df_weather['Month'] = pd.to_datetime(df_weather['Date']).dt.month

# 통계데이터프레임 생성
# Descriptive Statistics
descriptive_stats = df_weather.describe()

# Seasonal Analysis
seasonal_analysis = df_weather.groupby('Seasons')['Rented Bike Count'].mean()

#Correlation Analysis
correlation_matrix = df_weather.iloc[:,1:10].corr()

# Holiday vs. Non-Holiday Analysis
holiday_analysis= df_weather.groupby('Holiday')['Rented Bike Count'].mean()




###################################################################################
# 화면 출력
###################################################################################
st.header('3단계 : 날씨 정보와 연관성 시각화')
st.write(df_weather)

st.subheader('df_weather.describe()')
st.write(descriptive_stats)

st.subheader('df_weather.groupby(Seasons)[Rented Bike Count].mean()')
st.write(seasonal_analysis)


fig1, ax1 = plt.subplots()

st.subheader('correlation_matrix 차트')
sns.heatmap(correlation_matrix,annot=True, cmap='coolwarm',ax=ax1)
plt.xticks(rotation=45, ha='right')
plt.title('Correlation Analysis')
st.pyplot(fig1)


st.subheader('holiday_analysis')
st.write(holiday_analysis)


sns.pairplot(df_weather[['Rented Bike Count', 'Temperature', 'Humidity(%)', 'Wind speed (m/s)']],ax=ax1)
st.pyplot(fig1)

sns.pairplot(df_weather, hue='Rented Bike Count', palette='husl',ax=ax1)
st.pyplot(fig1)

