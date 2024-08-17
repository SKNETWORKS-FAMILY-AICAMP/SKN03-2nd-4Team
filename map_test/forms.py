from django import forms

class DateForm(forms.Form):
    start_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month'}),
        label='시작 날짜'
    )
    end_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month'}),
        label='종료 날짜'
    )
