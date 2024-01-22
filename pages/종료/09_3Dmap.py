import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


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

chart_data = df_master1.loc[:,['lat','lon']]
# chart_data = pd.DataFrame(
#    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#    columns=['lat', 'lon'])


st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.51,
        longitude=126.90,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))