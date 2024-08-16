import pandas as pd
from django.shortcuts import render
import os
import json

def display_keyword_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/keyword_data.xlsx')

    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file, sheet_name='keyword_data')
    df["date"] = df["date"].dt.strftime("%Y-%m")
    
    # 관광지 리스트 생성
    area_list = df['관광지'].unique().tolist()

    # 기본 지역 설정
    area = "새별 오름"
    
    # POST 요청이 들어오면 선택된 지역으로 필터링
    if request.method == "POST":
        area = request.POST.get("areaSelect")
        print(area)
    
    # 선택된 지역의 데이터 필터링
    filtered_df = df[df["관광지"] == area]

    print(filtered_df)

    keyword_data = filtered_df.to_dict(orient="records")

    # 데이터를 JSON으로 변환
    keyword_data = json.dumps(keyword_data)
    
    # 템플릿에 데이터와 선택된 지역 전달
    return render(request, 'keyword_app/keyword.html', {
        'keyworkd_data': keyword_data,
        'area_list': area_list,
        'selected_area': area  # 선택된 지역 전달
    })
