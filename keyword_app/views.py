import pandas as pd
from django.shortcuts import render
import os
import json

def display_keyword_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/keyword_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)

    # "date" 열을 datetime 형식으로 변환
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # 날짜 형식 변환
    df["date"] = df["date"].dt.strftime("%Y-%m")

    # 키워드 리스트 생성
    keyword_list = df["관광지"].unique().tolist()

    # POST 요청이 들어오면 선택된 키워드로 필터링
    if request.method == "POST":
        keyword = request.POST.get("keywordSelect")
    else:
        keyword = keyword_list[0]  # 기본 선택 키워드 설정

    # 선택된 키워드에 따라 데이터 필터링
    filtered_df = df[df["관광지"] == keyword]
    keyword_data = filtered_df.to_dict(orient="records")
    
    keyword_data = json.dumps(keyword_data)
    
    # 템플릿에 데이터 전달
    return render(request, 'keyword_app/keyword.html', 
                  {
                      'json_data': keyword_data,
                      'keyword_list': keyword_list,
                      'selected_keyword': keyword
                   }
                  )
