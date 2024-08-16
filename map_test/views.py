from django.shortcuts import render

def map_test_view(request):
    return render(request, 'map_test/map_test.html')