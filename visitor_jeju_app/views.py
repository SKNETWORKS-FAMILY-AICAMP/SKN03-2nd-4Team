import pandas as pd
import os
import json
from django.shortcuts import render

def display_visitor_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_jeju_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # 엑셀 파일에서 실제 열 이름을 사용합니다 (예: "날짜", "personal_trip").
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    
    # 날짜 형식 변환
    df["Date"] = df["Date"].dt.strftime("%Y-%m")

    # 필요한 데이터만 추출
    df_filtered = df[["Date", "personal_trip"]]

    # 데이터를 JSON으로 변환
    visitor_data = df_filtered.to_dict(orient="records")
    visitor_data_json = json.dumps(visitor_data)
    
    # 템플릿에 데이터 전달
    return render(request, 'visitor_jeju_app/visitor_jeju.html', 
                  {
                      'json_data': visitor_data_json
                  }
                 )
