from django.shortcuts import render
import pandas as pd
import os
import json

def map_view(request):
    
    return render(request, 'map_app/map_app.html')

def new_page1(request):
    value = request.GET.get('value', None)
    
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    region_file = os.path.join(BASE_DIR, 'data/consumption_region_data.xlsx')
    visitor_file = os.path.join(BASE_DIR, 'data/visitor_changing_data.xlsx')
    keyword_file = os.path.join(BASE_DIR, 'data/keyword_data.xlsx')

    # pandas를 사용하여 엑셀 파일 읽기
    df_consumption = pd.read_excel(region_file, sheet_name='consumption_region_data')
    df_visitor = pd.read_excel(visitor_file)
    df_keyword = pd.read_excel(keyword_file)

    df_consumption["date"] = df_consumption["date"].dt.strftime("%Y-%m")
    df_visitor["date"] = df_visitor["date"].dt.strftime("%Y-%m")
    df_keyword['date'] = pd.to_datetime(df_keyword['date'], errors='coerce')
    df_keyword["date"] = df_keyword["date"].dt.strftime("%Y-%m")


    df_consumption["매출금액"] = df_consumption["매출금액"].round(2)

    # 제주 각 지역에 해당하는 지역명
    region_jeju = ['애월읍', '제주시', '조천읍', '구좌읍', '성산읍', '표선면', '남원읍', '서귀포시', '안덕면', '대정읍', '한경면', '한림읍', '우도면']

    # df의 새로운 컬럼 생성, 지역명의 분류를 위해
    # Column1을 띄어쓰기 기준으로 분리
    df_split = df_consumption['지역명'].str.split(' ', expand=True)

    # 분리된 단어에 따라 새로운 열 이름 설정
    # 예를 들어, 최대 3개의 단어로 나뉘는 경우:
    df_split.columns = [f'Word{i+1}' for i in range(df_split.shape[1])]

    # 기존 데이터 프레임에 분리된 열 추가
    df_consumption = pd.concat([df_consumption, df_split], axis=1)

    for index, row in df_consumption.iterrows():
        if df_consumption.iloc[index]['Word2'] in region_jeju:
            df_consumption.loc[index, 'Word3'] = df_consumption.loc[index, 'Word2']

        elif df_consumption.iloc[index]['Word1'] in region_jeju:
            df_consumption.loc[index, 'Word3'] = df_consumption.loc[index, 'Word1']

    # df 의 Word3 컬럼에는 제주 각 지역에 해당하는 지역명이 반드시 포함되어 있는 상태
    # df_visitor 의 지역명 컬럼에도 지역명 포함
    # keyword 의 지역명 컬럼에도 지역명 포함

    # 날짜와 지역 선택 시 해당 지역의 매출액, 방문객, 방문지가 출력되도록...
    
    parameter_region = region_jeju[int(value)-1]

    parameter_region_df = df_consumption[df_consumption['Word3'] == parameter_region]
    df_grouped = parameter_region_df.groupby(['date', '지역명', 'Word3'], as_index=False)['매출금액'].sum()
    df_grouped = df_grouped[['date', 'Word3', '매출금액']]
    consumption_region_data = df_grouped.to_dict(orient="records")
    
    image_url = "images/jeju/hover_image_" + value +".png"

    # keyword 부분
    df_grouped2 = df_keyword[df_keyword['지역명'] == parameter_region]

    keyword_data = df_grouped2.to_dict(orient="records")


    # 방문 인구수
    df_grouped3 = df_visitor[df_visitor['지역명2'] == parameter_region]    
    
    df_grouped3 = df_grouped3.groupby(['date', '지역명2'], as_index=False)['방문인구수'].sum()
    
    df_grouped3 = df_grouped3[['date', '방문인구수', '지역명2']]

    visitor_data = df_grouped3.to_dict(orient="records")

    print(json.dumps(visitor_data, ensure_ascii=False))

    context = {
        'image_url': image_url,
        'chart_data' : json.dumps(consumption_region_data, ensure_ascii=False),
        'chart_data2' : json.dumps(keyword_data, ensure_ascii=False),
        'chart_data3' : json.dumps(visitor_data, ensure_ascii=False)
    }

    # 새로운 페이지 1에 대한 처리 로직
    return render(request, 'map_app/new_page1.html', context)

