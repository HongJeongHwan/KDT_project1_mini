import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기 : 마스터파일
file_path = './data/reduced_서울특별시 공공자전거 이용정보(시간대별)_2304.csv'
df = pd.read_csv(file_path,encoding='cp949')


# 데이터 전처리
### 분석데이터 구성
df_bike = df.drop(['대여소번호', '대여소명', '대여구분코드'], axis=1)

### 성별 컬럼 -> 누락 데이터 -> 'O' (other) 대체
# 누락치 dropna() 처리하는 것으로 변경
df_bike.dropna(subset=['성별'],inplace=True)

### index -> reset 필요 -> reset_index()
df_bike.reset_index(drop=True, inplace=True) # drop=True 를 사용해서 기존 index가 남지 않도록 한다


# Feature Engineering
# # 성별 컬럼 -> replace()
# df_bike.replace({'성별': {'M':1,'m':1,'F':2,'f':2,'O':3}}, inplace=True)

### 굳이 숫자로 replace 하지 말고, 소문자 -> 대문자로 변경하는 것이 나을듯...
df_bike.replace({'성별': {'m':'M','f':'F'}}, inplace=True)


### 운동량, 탄소량 컬럼 -> '\N' -> -1 로 대체
# 운동량, 탄소량 컬럼을 수치형 데이터로 변경하려고 하면 '\N' 때문에 error 발생되어 -1 로 대체함
df_bike.iloc[:,5] = df_bike.iloc[:,5].replace(r'\N',-1) # 운동량
df_bike.iloc[:,6] = df_bike.iloc[:,6].replace(r'\N',-1) # 탄소량

### 운동량, 탄소량 컬럼 numeric으로 형변환
df_bike["운동량"] = pd.to_numeric(df_bike["운동량"]) # 운동량
df_bike.iloc[:, 6] = df_bike.iloc[:, 6].astype(float) # 탄소량


# 시간대별 대여건수
count_t = df_bike.loc[:,'대여시간'].value_counts().sort_index()

### 시간대별 이용건수
df_bike_time = df_bike.loc[:, ('대여시간','이용건수')]

# 대여시간별 이용건수를 그룹핑하여 -> 그룹핑 결과 합계
use_per_hour = df_bike_time[['이용건수']].groupby(df_bike_time['대여시간']).sum()

# 요일별 이용건수
# 대여일자를 datetime으로 형변환해서 weekday 추가
df_bike_day = df_bike.loc[:, ('대여일자','대여시간','이용건수')]
df_bike_day['일자(date)'] = pd.to_datetime(df_bike_day['대여일자'])
df_bike_day['weekday'] = df_bike_day['일자(date)'].dt.weekday

# 요일별 이용건수를 그룹핑하여 -> 그룹핑 결과 합계
use_per_weekday = df_bike_day[['이용건수']].groupby(df_bike_day['weekday']).sum()
use_per_weekday1 = use_per_weekday
use_per_weekday1.index = ['0월','1화','2수','3목','4금','5토','6일']

# 성별 대여건수
count_s = df_bike.loc[:,'성별'].value_counts().sort_index()
# 성별 대여 비율
ratio_s = df_bike.loc[:,'성별'].value_counts(normalize=True).sort_index()

# 연령대별 대여건수
count_a = df_bike.loc[:,'연령대코드'].value_counts().sort_index()
# 연령대별 비율
ratio_a = df_bike.loc[:,'연령대코드'].value_counts(normalize=True).sort_index()


# 성별 컬럼 -> replace()
df_bike_numeric = df_bike.copy()
df_bike_numeric.replace({'성별': {'M':1,'F':2}}, inplace=True)

table1_1 = pd.pivot_table(df_bike_numeric, index=['성별'], \
                        values=['운동량', '탄소량','이동거리(M)','이용시간(분)' ], \
                        aggfunc=np.mean)

table1_2 = pd.pivot_table(df_bike_numeric, index=['성별'], \
                        values=['운동량', '탄소량','이동거리(M)','이용시간(분)' ], \
                        aggfunc=np.mean).round(2) # 소숫점 2자리










###################################################################################
# 화면 출력
###################################################################################
st.subheader('4단계 : 탄소발자국 정보와 연관성 시각화')
st.subheader('- 기본정보 출력')
st.write("데이터 량이 (3601047, 12) 많아서 '대여소번호', '대여소명', '대여구분코드' 컬럼을 제외하고 분석함")
st.write('성별을 제대로 표시하지 않은 데이터를 dropna() 처리하거나 다른 값으로 대체 필요 -> 우선 데이터가 많아서 다른 값으로 대체함')
st.write(df_bike)


st.subheader('시간대별 대여건수 시각화')
st.write('시간대별 대여건수 : ' + str(count_t))

fig1 = plt.figure()
ax = sns.countplot(data=df_bike, x='대여시간')
st.pyplot(fig1)

st.subheader('요일별 이용건수 시각화')
st.bar_chart(use_per_weekday)

st.subheader('성별 이용건수 시각화')
st.write('성별 대여건수 : ' + str(count_s))
st.write('성별 대여비율 : ' + str(ratio_s))
fig1 = plt.figure()
ax = sns.countplot(data=df_bike, x='성별')
st.pyplot(fig1)


st.subheader('연령대별 이용건수 시각화')
st.write('연령대별 대여건수 : ' + str(count_a))
st.write('연령대별 대여비율 : ' + str(ratio_a))
fig1 = plt.figure()
ax = sns.countplot(data=df_bike, x='연령대코드')
st.pyplot(fig1)



# st.scatter_chart : hue 적용이 안됨
# col1, col2 = st.columns(2)
# col1.subheader('[성별] 이동거리, 운동량 상관관계')
# col2.subheader('[연령대별] 이동거리, 운동량 상관관계')

# with col1:
#     st.scatter_chart(data=df_bike, x='이동거리(M)', y='운동량', hue='성별')
# with col2:
#     st.scatter_chart(data=df_bike, x='이동거리(M)', y='운동량', hue='연령대코드')
st.subheader('이동거리, 운동량 상관관계')
st.scatter_chart(data=df_bike, x='이동거리(M)', y='운동량')






