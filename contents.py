import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# 환경설정
tqdm.pandas()
# matplotlib 한글사용을 위한 코드
matplotlib.rcParams['font.family'] = 'Malgun Gothic'


# 데이터 불러오기
# 대여소 마스터파일 : 대여소아이디별 경도, 위도 정보
file_path = './data/rent_sample.csv'
df_rent = pd.read_csv(file_path)

###########################################################################################
# 데이터 전처리 : 노트북 파일에서 다하고 저장한 csv를 불러옴.
###########################################################################################
# 기준날짜 : csv에서 불러오면 dataframe에서는 int64로 들어오기 때문에 datetime으로 변환
df_rent['기준_날짜'] = df_rent['기준_날짜'].astype('str')

###########################################################################################
# 화면출력을 위한 구성정보
###########################################################################################
# 날짜 목록 가져오기
std_date = df_rent['기준_날짜'].unique()
std_date = np.insert(std_date,0,'선택하세요.')

# 시작대여소 목록 가져오기
st_rent_id = df_rent['시작_대여소_ID'].unique()
st_rent_id = np.insert(st_rent_id,0,'선택하세요.')



###########################################################################################
# 화면 출력
###########################################################################################
st.title('■ KDT mini Project')
st.subheader('조명 : 七面鳥')
st.write('조원 : 김동욱,김지영,김형경,윤선명,지영민,지예준,홍정환')
st.subheader('주제 : 따릉이의 활성화 정도를 지역 및 날씨측면에서 분석')
with st.expander('분석개요 보기'):
    st.write('- 분석 목적 : 최근 지구온난화의 문제가 심각해져 전지구적인 재난이 초래되고 있다. \
            지구온난화의 주범인 이산화탄소 저감을 위해 세계 각국은 전기차보급율 법률로 제정하는 등의 다양한 노력을 기울이고 있다. \
            이러한 추세에 발맞추어 서울시에서 운영하는 공공자전거 따릉이가 탄소저감에 얼마나 효율적인지를 파악하고, \
            더 나은 정책수립을 위해 필요한 정보를 제공함을 목적으로 한다.')
    st.write('- 제공 정보')
    st.write('  : 활성화 및 비활성화 대여소의 목록')
    st.write('  : 활성화의 및 비활성화의 원인으로 추정되는 지리 및 날씨 정보')
    st.write('- 분석 방향')
    st.write('  : 대여소의 활성화 정도를 지리적으로 분석')
    st.write('  : 대여소의 활성화 정도를 날씨정보와의 상관관계 분석')
    st.write('  : 대여소의 활성화 정도를 탄소배출감축량과의 상관관계 분석')
    st.write('- 수집 데이터')
    st.write('  : 2023년 10월 - 12월 따릉이 대여 데이터')
    st.write('  : 동 기간 날씨 데이터')
    st.write('  : 따릉이 대여소 데이터')
    st.write('- 데이터 수집 경로')
    st.write('  : 서울 열린데이터광장 (https://data.seoul.go.kr/)')
    st.write('  : 공공데이터 포털 (https://www.data.go.kr/)')


st.write('1. 따릉이 데이터 수집 및 저장')
st.write('수집된 데이터를 pandas의 DataFrame으로 저장')
st.write('2. 인덱스불리언을 이용해 수집된 따릉이 데이터 확인')
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
    sel_st_rent_id = st.selectbox(
        # selectbox 위의 설명글
        '시작_대여소',
        # selectbox 구성요소(튜플의 형태로)
        (st_rent_id)
    )  



# 데이터 필터링 조건 지정 : 날짜, 시작대여소, 종료대여소
cond = pd.Series('')
cond = ''
IsNoSelected = False

if sel_date!='선택하세요.':
    cond_date = (df_rent['기준_날짜']==sel_date)
    IsSelected_date = True
else:
    IsSelected_date = False
    
if sel_st_rent_id!='선택하세요.':
    cond_id = (df_rent['시작_대여소_ID']==sel_st_rent_id)
    IsSelected_st_rent_id = True
else:
    IsSelected_st_rent_id = False


if IsSelected_date == True:
    if IsSelected_st_rent_id == True:
        cond = cond_date & cond_id
    else:
        cond = cond_date
else:
    if IsSelected_st_rent_id == True:
        cond = cond_id
    else:
        IsNoSelected = True




        
if (IsNoSelected==False):
    # 기본정보 DataFrame 출력 : 지정된 조건
    with st.expander('▷ 수집된 따릉이 정보 데이터프레임 출력'):
        st.write(df_rent.loc[cond,:])

    # # Chart 출력을 위한 groupby한 데이터프레임 출력
    # with st.expander('▷ 시각화를 위한 기본정보의 동별합계 데이터프레임 출력'):
    #     df_rent_tot_group = df_rent_tot.groupby(by=['기준_날짜','시작_대여소_동명','시작_대여소명'])\
    #     .agg({'전체_건수':sum,'전체_이용_분':sum,'전체_이용_거리':sum})\
    #     .sort_values(by=['전체_건수','전체_이용_분','전체_이용_거리'],ascending=False)
    #     st.write(df_rent_tot_group)

    # # Chart 출력
    # with st.expander('▷ 시각화'):
        
    #     fig1, ax1 = plt.subplots()

    #     # sns.histplot() 실행
    #     st.subheader(sel_st_rent_dong+'의 이용시간(분), 이용거리')
    #     sns.barplot(data=df_rent_tot_group,x='시작_대여소명',y='전체_이용_분',ax=ax1)
    #     st.pyplot(fig1)
    #     sns.barplot(data=df_rent_tot_group,x='시작_대여소명',y='전체_이용_거리',ax=ax1)
    #     st.pyplot(fig1)
