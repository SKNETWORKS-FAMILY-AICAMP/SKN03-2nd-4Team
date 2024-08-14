from django.shortcuts import render
import pandas as pd
import os

def display_weather_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/weather_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file, sheet_name='평균기온')
    
    # 날짜 열을 날짜 형식으로 변환합니다.
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')

    # DataFrame을 딕셔너리로 변환
    weather_data = df.to_dict(orient='records')

    # 템플릿에 데이터 전달
    return render(request, 'weather_app/weather.html', {'weather_data': weather_data})
