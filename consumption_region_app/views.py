from django.shortcuts import render
import pandas as pd
import os
import json

def display_consumption_region_data(request):
    if request.method == "POST":
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_file = os.path.join(BASE_DIR, 'data/consumption_region_data.xlsx')
        area = request.POST.get("areaSelect")
        print(area) ## 서귀포시
        df = pd.read_excel(excel_file, sheet_name='consumption_region_data')
        df["date"] = df["date"].dt.strftime("%Y-%m")
        df["매출금액"] = df["매출금액"].round(2)
        area_list = df["지역명"].unique().tolist()
        filtered_df = df[df["지역명"] == area]
        consumption_region_data = filtered_df.to_dict(orient="records")
        consumption_region_data = json.dumps(consumption_region_data)
        # return filtered_df
        return render(request, 'consumption_region_app/consumption_region.html', \
                        {'consumption_region_data': consumption_region_data,
                        'area_list': area_list})
    
    else:
        # 엑셀 파일의 경로 설정
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_file = os.path.join(BASE_DIR, 'data/consumption_region_data.xlsx')
        
        # pandas를 사용하여 엑셀 파일 읽기
        df = pd.read_excel(excel_file, sheet_name='consumption_region_data')
        # select option에 지역명 44개 추가를 위해 지역명 unique 값만 뽑아 list로 전달
        area_list = df["지역명"].unique().tolist()
        # 전체 지역 조회는 시간이 오래 걸리므로 최초 선택 지역에 대해서만 데이터 전달
        df = df[df["지역명"] == "제주시 추자면"]
        # 데이트타임 형식 스트링으로 변경 (데이트타임은 json 형식 변경 불가)
        df["date"] = df["date"].dt.strftime("%Y-%m")
        # 매출금액 반올림
        df["매출금액"] = df["매출금액"].round(2)
        consumption_region_data = df.to_dict(orient='records')
        # 프론트엔드에서 데이터를 파싱하기위해 데이터를 JSON으로 변경
        consumption_region_data = json.dumps(consumption_region_data)
        
        # 템플릿에 데이터 전달
        return render(request, 'consumption_region_app/consumption_region.html', \
                        {'consumption_region_data': consumption_region_data,
                        'area_list': area_list})