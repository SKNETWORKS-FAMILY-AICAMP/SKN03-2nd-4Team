from django.shortcuts import render
import pandas as pd
import os
import json

def display_consumption_region_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/consumption_region_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file, sheet_name='consumption_region_data')
    df["date"] = df["date"].dt.strftime("%Y-%m")
    df["매출금액"] = df["매출금액"].round(2)
    
    # 지역명 리스트 생성
    area_list = df["지역명"].unique().tolist()
    
    # 기본 지역 설정
    area = "제주시 추자면"
    
    # POST 요청이 들어오면 선택된 지역으로 필터링
    if request.method == "POST":
        area = request.POST.get("areaSelect")
    
    # 선택된 지역에 따라 데이터 필터링
    filtered_df = df[df["지역명"] == area]
    consumption_region_data = filtered_df.to_dict(orient="records")
    
    # 데이터를 JSON으로 변환
    consumption_region_data = json.dumps(consumption_region_data)
    
    # 템플릿에 데이터와 선택된 지역 전달
    return render(request, 'consumption_region_app/consumption_region.html', {
        'consumption_region_data': consumption_region_data,
        'area_list': area_list,
        'selected_area': area  # 선택된 지역 전달
    })
