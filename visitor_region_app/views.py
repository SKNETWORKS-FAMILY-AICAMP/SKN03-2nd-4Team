import pandas as pd
from django.shortcuts import render
import os
import json

def display_visitor_region_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_region_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # "date" 열을 datetime 형식으로 변환
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # 날짜 형식 변환
    df["date"] = df["date"].dt.strftime("%Y-%m")

    # 시군구 리스트 생성
    sigungu_list = df["시군구"].unique().tolist()

    # POST 요청이 들어오면 선택된 시군구로 필터링
    if request.method == "POST":
        sigungu = request.POST.get("sigunguSelect")
    else:
        sigungu = sigungu_list[0]  # 기본 선택 시군구 설정

    # 선택된 시군구에 따라 데이터 필터링
    filtered_df = df[df["시군구"] == sigungu]
    visitor_region_data = filtered_df.to_dict(orient="records")
    
    visitor_region_data = json.dumps(visitor_region_data)
    
    # 템플릿에 데이터 전달
    return render(request, 'visitor_region_app/visitor_region.html', 
                  {
                      'json_data': visitor_region_data,
                      'sigungu_list': sigungu_list,
                      'selected_sigungu': sigungu
                   }
                  )
