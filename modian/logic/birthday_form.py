from django import forms


class BirthdayForm(forms.Form):
    user_id = forms.CharField(max_length=30)
    province_code = forms.IntegerField()
    birthday_wish = forms.CharField(max_length=100, widget=forms.Textarea)

