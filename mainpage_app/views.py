from django.http import JsonResponse
from django.shortcuts import render
from .models import (
    VisitingPopulation,
    VisitorJeju,
    ConsumptionRegion,
    VisitorRegion,
    KeywordVolume,
)
from django.db.models import Sum


# 홈 페이지에서 기본 데이터를 표시하는 뷰
def home(request):
    return render(request, "mainpage_app/home.html")


def get_previous_month_data(year, month):
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    return {
        "visits": VisitingPopulation.objects.filter(
            date__year=year, date__month=month, foreigner="전체"
        ),
        "visitors_domestic": VisitingPopulation.objects.filter(
            date__year=year, date__month=month, foreigner="내국인"
        ),
        "visitors_overseas": VisitingPopulation.objects.filter(
            date__year=year, date__month=month, foreigner="외국인"
        ),
        "sales_amount": ConsumptionRegion.objects.filter(
            date__year=year, date__month=month
        ),
    }


def calculate_changes(current, previous):
    response = {}
    # 각 데이터 타입에 맞는 필드 이름 지정
    field_mapping = {
        "visits": "count",
        "visitors_domestic": "count",
        "visitors_overseas": "count",
        "sales_amount": "consumption",
    }

    for key, queryset in current.items():
        field_name = field_mapping[key]
        current_sum = queryset.aggregate(sum=Sum(field_name))["sum"] or 0
        previous_sum = previous[key].aggregate(sum=Sum(field_name))["sum"] or 0

        # 변화율 계산
        if previous_sum:
            change = ((current_sum - previous_sum) / previous_sum) * 100
            formatted_change = f"{change:.2f}%"
        else:
            formatted_change = (
                "n/a"  # 이전 데이터가 없거나 0인 경우 변화율 표시하지 않음
            )

        response[key] = current_sum
        response[key + "_change"] = formatted_change

    return response


def get_chart_data_for_visits(year, month):
    # 주어진 연도와 월을 기준으로 최근 6개월의 방문 데이터
    chart_data = []
    labels = []
    for i in range(6):
        visits = (
            VisitingPopulation.objects.filter(
                date__year=year, date__month=month, foreigner="전체"
            ).aggregate(Sum("count"))["count__sum"]
            or 0
        )
        chart_data.append(visits)
        labels.append(f"{year}-{month:02d}")
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    chart_data.reverse()  # 최신 데이터를 마지막에 오도록 순서 변경
    labels.reverse()
    return {"labels": labels, "data": chart_data}


def get_chart_data_for_provinces(year, month):
    # 주어진 연도와 월의 데이터를 가져와서 state별로 방문자 수를 합산
    provinces = (
        VisitorRegion.objects.filter(date__year=year, date__month=month)
        .values("state")
        .annotate(count=Sum("count"))
    )

    # 라벨과 데이터 생성
    labels = [province["state"] for province in provinces]
    data = [province["count"] for province in provinces]

    return {"labels": labels, "data": data}


def get_chart_data_for_countries(year, month):
    countries_data = VisitorJeju.objects.filter(
        date__year=year, date__month=month
    ).values(
        "jpn",
        "chn",
        "hkg",
        "twn",
        "sgp",
        "mys",
        "idn",
        "vnm",
        "tha",
        "asia_etc",
        "usa",
        "west_etc",
    )
    labels = [
        "Japan",
        "China",
        "Hong Kong",
        "Taiwan",
        "Singapore",
        "Malaysia",
        "Indonesia",
        "Vietnam",
        "Thailand",
        "Other Asia",
        "USA",
        "Other Western",
    ]
    data = [
        countries_data.aggregate(Sum(field))[f"{field}__sum"] or 0
        for field in [
            "jpn",
            "chn",
            "hkg",
            "twn",
            "sgp",
            "mys",
            "idn",
            "vnm",
            "tha",
            "asia_etc",
            "usa",
            "west_etc",
        ]
    ]
    return {"labels": labels, "data": data}


def get_chart_data_for_sales(year, month):
    chart_data = []
    labels = []
    for i in range(12):  # 최근 12개월 데이터 가져오기
        sales = (
            ConsumptionRegion.objects.filter(
                date__year=year, date__month=month
            ).aggregate(Sum("consumption"))["consumption__sum"]
            or 0
        )
        chart_data.append(sales)
        labels.append(f"{year}-{month:02d}")
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    chart_data.reverse()
    labels.reverse()
    return {"labels": labels, "data": chart_data}


# 상위 5개 키워드를 가져오는 함수
def get_top_keywords(year, month):
    keywords = KeywordVolume.objects.filter(
        date__year=year, date__month=month
    ).order_by("-count")[
        :5
    ]  # 상위 5개 키워드를 count 기준으로 정렬하여 가져옴

    top_keywords = []
    for keyword in keywords:
        top_keywords.append(
            {
                "keyword": keyword.keyword,
                "city": keyword.city,
                "date": keyword.date.strftime("%b %d, %Y"),
                "count": keyword.count,
            }
        )

    return top_keywords


# AJAX 요청에 따라 대시보드 데이터를 업데이트하는 뷰
def update_dashboard(request):
    selected_date = request.GET.get("date")
    print(f"Selected Date: {selected_date}")

    if selected_date:
        year, month = map(int, selected_date.split("-"))

        # 현재 데이터 가져오기
        current_data = {
            "visits": VisitingPopulation.objects.filter(
                date__year=year, date__month=month, foreigner="전체"
            ),
            "visitors_domestic": VisitingPopulation.objects.filter(
                date__year=year, date__month=month, foreigner="내국인"
            ),
            "visitors_overseas": VisitingPopulation.objects.filter(
                date__year=year, date__month=month, foreigner="외국인"
            ),
            "sales_amount": ConsumptionRegion.objects.filter(
                date__year=year, date__month=month
            ),
        }

        # 이전 달 데이터 가져오기
        previous_data = get_previous_month_data(year, month)

        # 데이터 집계 및 변화율 계산
        response_data = calculate_changes(current_data, previous_data)

        # 차트 데이터 추가
        response_data["chartDataVisits"] = get_chart_data_for_visits(year, month)
        response_data["chartDataProvinces"] = get_chart_data_for_provinces(year, month)
        response_data["chartDataCountries"] = get_chart_data_for_countries(year, month)
        response_data["chartDataSales"] = get_chart_data_for_sales(year, month)

        # 상위 5개 키워드 데이터 추가
        response_data["topKeywords"] = get_top_keywords(year, month)

        return JsonResponse(response_data)

    return JsonResponse({"error": "No data for selected date"}, status=404)
