import pandas as pd
import plotly.express as px
import colorsys
# CSV 파일 불러오기
data = pd.read_csv("./data/aggregated_data_2.csv", encoding='utf-8-sig')
data['평균 사용시간'] = data['총 사용시간'] / data['Android+IOS 사용자 수']
# '날짜' 열을 datetime 형식으로 변환하여 연도 추출
# 연도별로 트리 맵을 그리기 위해 반복문을 사용

data['파일명'] = data['파일명'].replace('cargo.csv', '화물')
data['파일명'] = data['파일명'].replace('drive.csv', '대리')
data['파일명'] = data['파일명'].replace('deliver.csv', '배달')
data['파일명'] = data['파일명'].replace('taxi.csv', '택시')
data['파일명'] = data['파일명'].replace('taekbae.csv', '택배')

file_names = data['파일명'].unique()
color_mapping = {
    '화물': '#00c7be',
    '대리': '#5856d6',
    '배달': '#af52de',
    '택시': '#ff3b30',
    '택배': '#ff9500'
}

data['색상'] = data['파일명'].map(color_mapping)

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
def hsv_to_rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def a(s,y,z):
    r=y[y[z] == s]['rgba색상'].values[0]
    return '#'+str(hex(r[0])[2:])+str(hex(r[1])[2:])+str(hex(r[2])[2:])

for year in data['연도'].unique():
    yearly_data = data[data['연도'] == year]
    yearly_data['평균 사용시간'] = yearly_data['평균 사용시간'].round(2)
    yearly_data['Android+IOS 사용자 수']=yearly_data['Android+IOS 사용자 수'].round(0)
    yearly_data['파일_패키지'] = yearly_data['파일명'] + " - " + yearly_data['패키지명']
    usage_min, usage_max = yearly_data['평균 사용시간'].min(), yearly_data['평균 사용시간'].max()
    yearly_data['사용시간_정규화'] = (yearly_data['평균 사용시간'] - usage_min) / (usage_max - usage_min)
    yearly_data['rgba색상'] = yearly_data.apply(
        lambda row: hsv_to_rgb(rgb_to_hsv(*hex_to_rgb(row['색상']))[0], row['사용시간_정규화'], rgb_to_hsv(*hex_to_rgb(row['색상']))[2]), axis=1
    )
    fig = px.treemap(
        yearly_data, 
        path=['파일명', '패키지명'],
        values='Android+IOS 사용자 수',
        title=f'{year} 10월 교통플랫폼산업 종사자 트리 맵',
        color_continuous_scale="Greys"
    )
    abc =[a(sector.split('/')[-1],yearly_data,'패키지명') for sector in fig.data[0]['ids'] if len(sector.split("/")) == 2]
    abc.extend( [color_mapping[sector] for sector in fig.data[0]['ids'] if '/'not in sector])
    fig.data[0]['marker']['colors']=abc

    fig.update_layout(
            title_font=dict(size=48),
            font=dict(size=32),
            title=f'{year} 10월 교통플랫폼산업 종사자 트리 맵',
            margin=dict(t=100, b=0, l=0, r=0),
        )

    fig.write_image(f"treemap_{year}.png", width=1920, height=1080, scale=3)