import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import datetime
    
# 환경설정
tqdm.pandas()
# matplotlib 한글사용을 위한 코드
matplotlib.rcParams['font.family'] = 'Malgun Gothic'




# 데이터 불러오기
# 대여소 마스터파일 : 대여소아이디별 경도, 위도 정보
file_path = './data/groupby_lat_dong_23년12월렌탈.csv'
df_rent_sum = pd.read_csv(file_path)


###########################################################################################
# 데이터 전처리 : 노트북 파일에서 다하고 저장한 csv를 불러옴.
###########################################################################################
# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent_sum['기준_날짜'] = df_rent_sum['기준_날짜'].astype('str')

###########################################################################################
# 화면출력을 위한 구성정보
###########################################################################################
# 날짜 목록 가져오기
std_date = df_rent_sum['기준_날짜'].unique()
std_date = np.insert(std_date,0,'선택하세요.')

# 시작대여소 목록 가져오기
st_rent_dong = df_rent_sum['시작_대여소_동명'].unique()
st_rent_dong = np.insert(st_rent_dong,0,'선택하세요.')










###########################################################################################
# 화면 출력
###########################################################################################
st.header('대여소의 활성화 정도를 지리적으로 분석')
with st.expander('1. 따릉이 정보중 NaN 데이터 처리방법'):
    st.write('  가. 대여소명 : 대여소명에 동명이 포함되어 있어 이를 활용하기로 결정')
    st.write('  나. 하지만 분석기간인 12월 파일에는 대여소명이 모두 NaN')
    st.write('  다. 이를 해결하기 위해 대여소ID와 대여소명이 모두 존재하는 추가 데이터 수집')
    st.write('  라. 추가 수집된 정보를 이용하여 대여소명 채우기')
with st.expander('2. 지리적 분석을 위해 따릉이 대여소 데이터 수집'):
    st.write('  가. 대여소의 위도, 경도정보')
with st.expander('3. 동별 대여소 위치 확인'):
    ## 선택 상자 생성
    # 조회조건 layout
    col1, col2 = st.columns(2)

    # 컬럼별 소제목 지정
    # col1.subheader("날짜 선택")
    # col2.subheader("시작대여소 선택")

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
        sel_st_rent_dong = st.selectbox(
            # selectbox 위의 설명글
            '시작_대여소_동명',
            # selectbox 구성요소(튜플의 형태로)
            (st_rent_dong)
        )
    
    # 데이터 필터링 조건 지정 : 날짜, 시작대여소, 종료대여소
    # cond = pd.Series('')
    cond = ':'
    IsNoSelected = False

    if sel_date!='선택하세요.':
        cond_date = (df_rent_sum['기준_날짜']==sel_date)
        IsSelected_date = True
    else:
        IsSelected_date = False
        
    if sel_st_rent_dong!='선택하세요.':
        cond_dong = (df_rent_sum['시작_대여소_동명']==sel_st_rent_dong)
        IsSelected_st_rent_dong = True
    else:
        IsSelected_st_rent_dong = False


    if IsSelected_date == True:
        if IsSelected_st_rent_dong == True:
            cond = cond_date & cond_dong
        else:
            cond = cond_date
    else:
        if IsSelected_st_rent_dong == True:
            cond = cond_dong
        else:
            IsNoSelected = True
    
    if (IsSelected_date == True) | (IsSelected_st_rent_dong == True):
        show_df = df_rent_sum.loc[cond,['기준_날짜','시작_대여소_동명','시작_대여소_ID','종료_대여소_ID','전체_건수','전체_이용_분','전체_이용_거리','시작_대여소_lat','시작_대여소_lon']]
        map_df = df_rent_sum.loc[cond,['시작_대여소_lat','시작_대여소_lon']]
        map_df.rename(columns={'시작_대여소_lat':'lat','시작_대여소_lon':'lon'},inplace=True)
        st.write(show_df)
        st.map(map_df)
    
    
with st.expander('4. 활성화/비활성화 동 추출'):
    st.write('- 활성화 판단기준 : 이용시간 및 거리')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dong_cnt = st.number_input('분석할 동의 개수 입력', value=5)
    with col2:
        start_date = st.date_input('시작날짜 선택', datetime.date(2023, 12, 1))
        start_date = str(start_date).replace('-','')
    with col3:
        end_date = st.date_input('종료날짜 선택', datetime.date(2023, 12, 31))
        end_date = str(end_date).replace('-','')
        
    # st.write('시작날짜:', start_date)
    # st.write('종료날짜:', end_date)
    # st.write('The current number is ', dong_cnt)
    
    st.write('- 활성화 정도가 높은 TOP'+str(dong_cnt)+'개의 동')
    # 날짜계산을 위해 새로운 df 생성
    df_rent_sum_date = df_rent_sum
    df_rent_sum_date.set_index('기준_날짜', inplace=True)
    
    top_ranking = df_rent_sum_date[start_date:end_date].groupby(by=['시작_대여소_동명'])\
        .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})\
        .sort_values(by=['전체_이용_거리','전체_이용_분','전체_건수'],ascending=False)
    top_ranking.reset_index(inplace=True)    
    st.write(top_ranking.iloc[:dong_cnt,:])
    
    # top map
    cond_TN_chk = 0
    # st.write(top_ranking.iloc[:dong_cnt,:]['시작_대여소_동명'].values)
    for dong in top_ranking.iloc[:dong_cnt,:]['시작_대여소_동명'].values:
        if cond_TN_chk==0:
            cond_TN = (df_rent_sum_date[start_date:end_date]['시작_대여소_동명']==dong)
            cond_TN_chk += 1
            # st.write('aaaaa')
        else:
            cond_TN = cond_TN | (df_rent_sum_date[start_date:end_date]['시작_대여소_동명']==dong)
            # st.write('bbbbb')
    # st.write(cond_TN)
    df_map_top = df_rent_sum_date[start_date:end_date].loc[cond_TN,['시작_대여소_lat','시작_대여소_lon']].drop_duplicates()
    df_map_top.rename(columns={'시작_대여소_lat':'lat','시작_대여소_lon':'lon'},inplace=True)
    st.map(df_map_top)
    st.write('')     
    st.write('')     
    
    st.write('- 활성화 정도가 낮은 BOTTOM '+str(dong_cnt)+'개의 동')
    bottom_ranking = df_rent_sum_date[start_date:end_date].groupby(by=['시작_대여소_동명'])\
        .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})\
        .sort_values(by=['전체_이용_거리','전체_이용_분','전체_건수'],ascending=True)
    bottom_ranking.reset_index(inplace=True)    
    st.write(bottom_ranking.iloc[:dong_cnt,:])
    
    # bottom map
    cond_BN_chk = 0
    # st.write(bottom_ranking.iloc[:dong_cnt,:]['시작_대여소_동명'].values)
    for dong in bottom_ranking.iloc[:dong_cnt,:]['시작_대여소_동명'].values:
        if cond_BN_chk==0:
            cond_TN = (df_rent_sum_date[start_date:end_date]['시작_대여소_동명']==dong)
            cond_BN_chk += 1
            # st.write('aaaaa')
        else:
            cond_TN = cond_TN | (df_rent_sum_date[start_date:end_date]['시작_대여소_동명']==dong)
            # st.write('bbbbb')
    # st.write(cond_TN)
    df_map_bottom = df_rent_sum_date[start_date:end_date].loc[cond_TN,['시작_대여소_lat','시작_대여소_lon']].drop_duplicates()
    df_map_bottom.rename(columns={'시작_대여소_lat':'lat','시작_대여소_lon':'lon'},inplace=True)
    st.map(df_map_bottom)
    
    st.write('')

with st.expander('5. 지리적 분석의 결과'):
    st.write('이상 지리적인 측면에서 보았을때 대여소의 활성화정도가 높은 동은 비교적 한강, 안양천 등의 수변접근성이 좋은 가양1동, 여의동, 목1동, 발산1동, 방화1동 등이었고 고궁이 있거나 청계천변 자전거도로가 비교적 잘 갖추어진 종료1,2,3,4가동으로 파악되었습니다.')
    st.write('그리고 지리적인 측면에서 보았을때 대여소의 비활성화정도가 높은 동은 관악산, 삼성산 주변의 경사가 심한 사당5동, 난향동이나 나머지 비교적 한강이나 자전거도로 접근성이 좋지 않은 지역으로 추정됩니다.')


###################################################################################
# 기존화면 출력
###################################################################################
# st.header('대여소의 활성화 정도를 지리적으로 분석')

# tab1, tab2 = st.tabs(["2D Map", "3D Map"])

# with tab1:
# #    st.header('2_1단계 : 대여소 정보를 지도에 시각화')
#    st.write(df_master1)
#    st.map(df_master1) 

# with tab2:
#    st.header("3D Map")
#    chart_data = df_master1.loc[:,['lat','lon']]
   
#    # 지도 그려주기
#    st.pydeck_chart(pdk.Deck(
#    map_style=None,
#    initial_view_state=pdk.ViewState(
#            latitude=37.51,
#            longitude=126.98,
#            zoom=10.2,
#            pitch=50,
#    ),
#    layers=[
#            pdk.Layer(
#            'HexagonLayer',
#            data=chart_data,
#            get_position='[lon, lat]',
#            radius=200,
#            elevation_scale=4,
#            elevation_range=[0, 1000],
#            pickable=True,
#            extruded=True,
#            ),
#            pdk.Layer(
#            'ScatterplotLayer',
#            data=chart_data,
#            get_position='[lon, lat]',
#            get_color='[200, 30, 0, 160]',
#            get_radius=200,
#            ),
#    ],
#    ))
