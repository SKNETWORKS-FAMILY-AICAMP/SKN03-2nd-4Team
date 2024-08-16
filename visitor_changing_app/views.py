from django.shortcuts import render
import pandas as pd
import os

def display_visitor_changing_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_changing_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file, sheet_name='visitor_changing_data')
    visitor_changing_data = df.to_dict(orient='records')
    
    # 템플릿에 데이터 전달
    return render(request, 'visitor_changing_app/visitor_changing.html', {'visitor_changing_data': visitor_changing_data})
