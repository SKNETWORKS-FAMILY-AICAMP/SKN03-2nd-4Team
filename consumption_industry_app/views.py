from django.shortcuts import render
import pandas as pd
import os
import json

def display_consumption_industry_data(request):
    # 엑셀 파일의 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_file = os.path.join(BASE_DIR, 'data/consumption_industry_data.xlsx')
    
    # pandas를 사용하여 엑셀 파일 읽기
    df = pd.read_excel(excel_file, sheet_name='consumption_industry_data')
    # 데이트타임 형식 스트링으로 변경 (데이트타임은 json 형식 변경 불가)
    df["date"] = df["date"].dt.strftime("%Y-%m")
    # 매출금액 반올림
    df["매출금액"] = df["매출금액"].round(2)
    consumption_industry_data = df.to_dict(orient='records')
    # 프론트엔드에서 데이터를 파싱하기위해 데이터를 JSON으로 변경
    consumption_industry_data = json.dumps(consumption_industry_data)
    
    # 템플릿에 데이터 전달
    return render(request, 'consumption_industry_app/consumption_industry.html', {'consumption_industry_data': consumption_industry_data})
