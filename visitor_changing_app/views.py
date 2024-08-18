import pandas as pd
from django.shortcuts import render
import os
import json

def display_visitor_changing_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_changing_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # "date" 열을 datetime 형식으로 변환
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # 날짜 형식 변환
    df["date"] = df["date"].dt.strftime("%Y-%m")

    # 지역명 리스트 생성
    area_list = df["지역명"].unique().tolist()

    # POST 요청이 들어오면 선택된 지역명으로 필터링
    if request.method == "POST":
        selected_area = request.POST.get("areaSelect")
    else:
        selected_area = area_list[0]  # 기본 선택 지역명 설정

    # 선택된 지역명에 따라 데이터 필터링
    filtered_df = df[df["지역명"] == selected_area]
    visitor_changing_data = filtered_df.to_dict(orient="records")
    
    visitor_changing_data = json.dumps(visitor_changing_data)
    
    # 템플릿에 데이터 전달
    return render(request, 'visitor_changing_app/visitor_changing.html', 
                  {
                      'json_data': visitor_changing_data,
                      'area_list': area_list,
                      'selected_area': selected_area
                   }
                  )
