# map_app/views.py

from django.shortcuts import render

def map_view(request):
    # 특별한 로직이 필요 없다면 바로 템플릿을 렌더링합니다.
    return render(request, 'map_app/map_app.html')
