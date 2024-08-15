from django.shortcuts import render
import pandas as pd
import os
from datetime import datetime
import json
from .forms import DateForm

def display_visitor_data(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/visitor_jeju_data.xlsx')
    
    df = pd.read_excel(excel_file, sheet_name='tourist_data')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
    df['YearMonth'] = df['Date'].dt.strftime('%Y-%m')

    chart_data = None
    full_table_data = None
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            start_date_str = form.cleaned_data['start_date']
            end_date_str = form.cleaned_data['end_date']

            start_date = datetime.strptime(start_date_str, '%Y-%m')
            end_date = datetime.strptime(end_date_str, '%Y-%m')
            
            filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
            grouped = filtered_df.groupby('YearMonth')['personal_trip'].sum()
            chart_data = grouped.to_dict()

            # 전체 데이터를 JSON으로 변환하여 템플릿으로 전달
            full_table_data = filtered_df.copy()
            full_table_data['Date'] = full_table_data['Date'].dt.strftime('%Y-%m-%d')
            full_table_data = full_table_data.to_dict(orient='records')

    return render(request, 'visitor_jeju_app/visitor_jeju.html', {
        'form': form,
        'chart_data': json.dumps(chart_data),  # 템플릿에 JSON으로 전달
        'full_table_data': json.dumps(full_table_data)  # 템플릿에 JSON으로 전달
    })
