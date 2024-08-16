from django.shortcuts import render
import pandas as pd
import os

def display_keyword_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    keyword_excel_file = os.path.join(BASE_DIR, 'data/keyword_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    keyword_df = pd.read_excel(keyword_excel_file, sheet_name='keyword_data')
    keyword_data = keyword_df.to_dict(orient='records')
    
    # 템플릿에 데이터 전달
    return render(request, 'keyword_app/keyword.html', {'keyword_data': keyword_data})
