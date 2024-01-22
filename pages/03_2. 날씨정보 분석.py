import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기 : 마스터파일
file_path = './data/SeoulBikeData.csv'
df_weather_org = pd.read_csv(file_path,encoding='cp949')


# 데이터 전처리
# 한글이 깨진 컬럼명 변경
df_weather_org.rename(columns={'Temperature(캜)':'Temperature',
                           'Dew point temperature(캜)':'Dew point temperature'},inplace=True)

# Date 컬럼을 Datetime으로 변경
# df_weather['Date'] = pd.to_datetime(df_weather['Date'])

# Month 컬럼 추가
# df_weather['Month'] = pd.to_datetime(df_weather['Date']).dt.month

### 데이터 구성 -> 사용할 컬럼만 DataFrame 다시 구성

# 'Dew point temperature(캜)'이슬점, 'Solar Radiation (MJ/m2)'(자외선), 'Functioning Day' 우선 drop -> 필요시 다시 합치자
df_weather = df_weather_org.drop(['Dew point temperature', 'Solar Radiation (MJ/m2)', 'Functioning Day'], axis=1)

# 단위가 깨진 글자로 나오는 컬럼이름 포함 전체 컬럼 이름을 한글로 변경
df_weather.columns=['날짜','대여건수','시간','기온','습도','풍속','가시거리(10m)','강우량(mm)','강설량(cm)','계절','휴일']

### 계절 수치화 -> replace
df_weather.replace({'계절': {'Spring':1,'Summer':2,'Autumn':3,'Winter':4}}, inplace=True)

### 날짜 컬럼 object -> datetime 으로 변경
df_weather['날짜'] = pd.to_datetime(df_weather['날짜'])

### '날짜' 컬럼을 활용해서 '년', '월', '일, '요일 컬럼 추가
df_weather['년'] = df_weather['날짜'].dt.year
df_weather['월'] = df_weather['날짜'].dt.month
df_weather['일'] = df_weather['날짜'].dt.day
df_weather['요일'] = df_weather['날짜'].dt.weekday




###################################################################################
# 화면 출력
###################################################################################
st.subheader('대여소의 활성화 정도를 기후적인 측면에서 분석')
with st.expander('- 기본정보 데이터프레임 출력'):
    st.write(df_weather.loc[:,['날짜','대여건수','시간','기온','습도','풍속','가시거리(10m)','강우량(mm)','강설량(cm)','계절','휴일']])

with st.expander('- Feature Engineering'):
    st.write('기본데이터에서 날짜별 대여정보 및 날씨정보가 있었는데, 이를 연도별, 월별, 일별, 요일별로 분석해보기 위해 \
            날짜 컬럼을 Datatime 형식으로 변경후 년도,월,일,요일 정보를 추출하여 별로의 컬럼으로 추가')
    # 코드보기
    if st.button('년도,월,일,요일 정보를 추출하는 코드보기'):
        code = '''
        ### 날짜 컬럼 object -> datetime 으로 변경
        df_weather['날짜'] = pd.to_datetime(df_weather['날짜'])

        ### '날짜' 컬럼을 활용해서 '년', '월', '일, '요일 컬럼 추가
        df_weather['년'] = df_weather['날짜'].dt.year
        df_weather['월'] = df_weather['날짜'].dt.month
        df_weather['일'] = df_weather['날짜'].dt.day
        df_weather['요일'] = df_weather['날짜'].dt.weekday'''
        st.code(code, language='python')

with st.expander('- 년,월,일,요일별 대여건수 시각화'):
    ### [1] 년,월,일,요일별 대여건수 시각화 (방법1)
    col1, col2 = st.columns(2)
    col1.subheader('[연도별] 대여건수')
    col2.subheader('[월별] 대여건수')

    # 연도별
    with col1:
        st.bar_chart(data=df_weather, x='년', y='대여건수')

    # 월별
    with col2:
        st.bar_chart(data=df_weather, x='월', y='대여건수')


    col3, col4 = st.columns(2)
    col3.subheader('[일별] 대여건수')
    col4.subheader('[요일별] 대여건수')
    # 일
    with col3:
        st.bar_chart(data=df_weather, x='일', y='대여건수')

    # 요일
    with col4:
        st.bar_chart(data=df_weather, x='요일', y='대여건수')

with st.expander('- 계절, 휴일별 대여건수 시각화'):
    col5, col6 = st.columns(2)
    col5.subheader('[계절별] 대여건수')
    col6.subheader('[휴일여부별] 대여건수')
    # 계절
    with col5:
        st.bar_chart(data=df_weather, x='계절', y='대여건수')

    # 휴일여부
    with col6:
        st.bar_chart(data=df_weather, x='휴일', y='대여건수')


# # scatter_chart
# col7, col8 = st.columns(2)
# col7.subheader('[기온]과 대여건수 상관관계')
# col8.subheader('[습도]와 대여건수 상관관계')

# # [기온]과 대여건수 상관관계
# with col7:
#     st.scatter_chart(data=df_weather.loc[:,['일','대여건수']], x='일', y='대여건수')

# # [습도]와 대여건수 상관관계
# with col8:
#     st.scatter_chart(data=df_weather.loc[:,['습도','대여건수']], x='습도', y='대여건수')



# col9, col10 = st.columns(2)
# col9.subheader('[풍속]과 대여건수 상관관계')
# col10.subheader('[가시거리]와 대여건수 상관관계')

# # 풍속
# with col9:
#     st.scatter_chart(data=df_weather.loc[:,['풍속','대여건수']], x='풍속', y='대여건수')

# # 가시거리
# with col10:
#     st.scatter_chart(data=df_weather.loc[:,['가시거리(10m)','대여건수']], x='가시거리(10m)', y='대여건수')


# col11, col12 = st.columns(2)
# col11.subheader('[강우량]과 대여건수 상관관계')
# col12.subheader('[강설량]와 대여건수 상관관계')

# # 강우량
# with col11:
#     st.scatter_chart(data=df_weather.loc[:,['강우량(mm)','대여건수']], x='강우량(mm)', y='대여건수')

# # 강설량
# with col12:
#     st.scatter_chart(data=df_weather.loc[:,['강설량(cm)','대여건수']], x='강설량(cm)', y='대여건수')


# st.scatter_chart 그림이 예쁘지 않아서 이미지 처리
with st.expander('- 기온,습도,풍속,가시거리,강우량,강설량별 대여건수 시각화'):
    file_path = './data/weather_scatter.png'
    st.image(file_path)

# heatmap
with st.expander('- correlation_matrix 분석 시각화'):
    fig1, ax1 = plt.subplots()

    st.subheader('correlation_matrix 차트')
    correlation_matrix=df_weather.corr()
    sns.heatmap(correlation_matrix,annot=True, cmap='coolwarm',ax=ax1)
    plt.xticks(rotation=45, ha='right')
    plt.title('Correlation Analysis')
    st.pyplot(fig1)
