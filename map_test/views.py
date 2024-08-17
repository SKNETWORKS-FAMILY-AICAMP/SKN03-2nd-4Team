from django.shortcuts import render
import pandas as pd
import os
import json
from .forms import DateForm

def map_view(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_changing_data.xlsx')  # 엑셀 파일 경로 설정
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file)
    
    # Date 열을 datetime 형식으로 변환하고 연-월 형식으로 변환
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    
    chart_data = None
    full_table_data = None

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            start_date_str = form.cleaned_data['start_date']
            end_date_str = form.cleaned_data['end_date']

            # 선택한 날짜 필터링
            filtered_df = df[(df['date'] >= start_date_str) & (df['date'] <= end_date_str)]
            grouped = filtered_df.groupby('date')['방문인구수'].sum()  # 방문자 수 합계
            chart_data = grouped.to_dict()

            # 전체 데이터를 JSON으로 변환하여 템플릿으로 전달
            full_table_data = filtered_df.to_dict(orient='records')
            
            print(full_table_data)
    else:
        form = DateForm()

    return render(request, 'map_test/map_test.html', {
        'form': form,
        'chart_data': json.dumps(chart_data, ensure_ascii=False),  # JSON 데이터로 변환하여 템플릿에 전달
        'full_table_data': json.dumps(full_table_data, ensure_ascii=False)  # JSON 데이터로 변환하여 템플릿에 전달
    })
