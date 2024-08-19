import os
import pandas as pd
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from mainpage_app.models import (
    KeywordVolume,
    VisitingPopulation,
    VisitorJeju,
    VisitorRegion,
    ConsumptionRegion,
    ConsumptionIndustry,
    Weather,
)


def convert_excel_date(excel_date):
    """엑셀 날짜 형식을 변환"""
    try:
        converted_date = datetime(1899, 12, 30) + timedelta(days=int(excel_date))
        return converted_date.date()
    except Exception as e:
        print(f"Error converting Excel date {excel_date}: {e}")
        return None


def parse_date(date_value):
    """다양한 형식의 날짜를 처리"""
    print(f"Parsing date: {date_value}")  # 로그 추가
    if isinstance(date_value, (int, float)):
        return convert_excel_date(date_value)
    elif isinstance(date_value, str):
        for fmt in ("%Y-%m", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y.%m.%d %I:%M:%S %p"):
            try:
                parsed_date = datetime.strptime(date_value, fmt)
                if fmt == "%Y-%m":
                    return parsed_date.replace(day=1).date()
                return parsed_date.date()
            except ValueError:
                continue
        print(f"Invalid date format for value: {date_value}")
    elif isinstance(date_value, datetime):
        return date_value.date()
    return None


def load_data_to_model(df, model, mappings):
    """DataFrame의 데이터를 지정된 모델에 저장"""
    for _, row in df.iterrows():
        data = {}
        for model_field, df_column in mappings.items():
            if model_field == "date":
                data[model_field] = parse_date(row[df_column])
                if data[model_field] is None:
                    print(f"Skipping row due to invalid date: {row}")
                    break
            else:
                data[model_field] = row[df_column]
        else:
            model.objects.create(**data)


class Command(BaseCommand):
    help = "Load data from Excel files into the database"

    def handle(self, *args, **kwargs):
        base_dir = settings.BASE_DIR  # Django 프로젝트의 루트 디렉토리
        data_dir = os.path.join(base_dir, "data")  # 데이터 파일이 저장된 디렉토리

        # 데이터 파일 경로 설정
        file_paths = {
            "keyword": os.path.join(data_dir, "keyword_data.xlsx"),
            "visiting_population": os.path.join(data_dir, "visitor_changing_data.xlsx"),
            "visitor_jeju": os.path.join(data_dir, "visitor_jeju_data.xlsx"),
            "visitor_region": os.path.join(data_dir, "visitor_region_data.xlsx"),
            "consumption_region": os.path.join(
                data_dir, "consumption_region_data.xlsx"
            ),
            "consumption_industry": os.path.join(
                data_dir, "consumption_industry_data.xlsx"
            ),
            "weather": os.path.join(data_dir, "weather_data.xlsx"),
        }

        # 데이터 로드 호출
        self.load_keyword_data(file_paths["keyword"])
        self.load_visiting_population_data(file_paths["visiting_population"])
        self.load_visitor_jeju_data(file_paths["visitor_jeju"])
        self.load_visitor_region_data(file_paths["visitor_region"])
        self.load_consumption_region_data(file_paths["consumption_region"])
        self.load_consumption_industry_data(file_paths["consumption_industry"])
        self.load_weather_data(file_paths["weather"])

    def load_keyword_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {
            "keyword": "관광지",
            "count": "count",
            "city": "지역명",
            "date": "date",
        }
        load_data_to_model(df, KeywordVolume, mappings)

    def load_visiting_population_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {
            "city": "지역명",
            "foreigner": "내외국인",
            "date": "date",
            "count": "방문인구수",
        }
        load_data_to_model(df, VisitingPopulation, mappings)

    def load_visitor_jeju_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {
            "date": "Date",
            "personal_trip": "personal_trip",
            "partial_package": "partial_package",
            "package": "package",
            "leisure": "leisure",
            "work": "work",
            "recreation": "recreation",
            "visit_rel": "visit_rel",
            "edu": "edu",
            "etc": "etc",
            "jpn": "JPN",
            "chn": "CHN",
            "hkg": "HKG",
            "twn": "TWN",
            "sgp": "SGP",
            "mys": "MYS",
            "idn": "IDN",
            "vnm": "VNM",
            "tha": "THA",
            "asia_etc": "ASIA_ETC",
            "usa": "USA",
            "west_etc": "WEST_ETC",
        }
        load_data_to_model(df, VisitorJeju, mappings)

    def load_visitor_region_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {
            "date": "date",
            "state": "지역명",
            "city": "시군구",
            "count": "방문객",
        }
        load_data_to_model(df, VisitorRegion, mappings)

    def load_consumption_region_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {"consumption": "매출금액", "city": "지역명", "date": "date"}
        load_data_to_model(df, ConsumptionRegion, mappings)

    def load_consumption_industry_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {"industry": "업종", "consumption": "매출금액", "date": "date"}
        load_data_to_model(df, ConsumptionIndustry, mappings)

    def load_weather_data(self, filepath):
        df = pd.read_excel(filepath)
        mappings = {
            "wind_speed": "풍속",
            "relative_humidity": "상대습도",
            "rain_fall": "강수량",
            "temperature": "평균기온",
            "date": "date",
        }
        load_data_to_model(df, Weather, mappings)
