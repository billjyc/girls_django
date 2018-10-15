from django import forms


class BirthdayForm(forms.Form):
    user_id = forms.CharField(max_length=24)
    province_code = forms.IntegerField()
    birthday_wish = forms.CharField(max_length=240, widget=forms.Textarea)
    ip = forms.CharField(max_length=100)

