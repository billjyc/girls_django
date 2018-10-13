from django import forms


class BirthdayForm(forms.Form):
    userid = forms.CharField(max_length=30)
    province_code = forms.IntegerField()
    birthdaywish = forms.CharField(max_length=100)

