from django.shortcuts import render
import pandas as pd
import os

def display_visitor_region_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/vistor_region_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)
    visitor_region_data = df.to_dict(orient='records')
    
    # 템플릿에 데이터 전달
    return render(request, 'visitor_region_app/visitor_region.html', {'visitor_region_data': visitor_region_data})
