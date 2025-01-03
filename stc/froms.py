from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date,timedelta

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class StockSearchForm(forms.Form):
    ticker = forms.CharField(label="Stock Ticker", max_length=10)

class StockForecastForm(forms.Form):
    stock = forms.CharField(label='Stock Symbol', max_length=20, initial='TCS.NS')
    time_period_type = forms.ChoiceField(
        label='Time Period Type',
        choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')],
        initial='Days'
    )
    time_period_value = forms.IntegerField(label='Time Period Value', min_value=1, initial=7)
    start_date = forms.DateField(label='Start Date', initial='2017-01-01')
    end_date = forms.DateField(label='End Date', initial=date.today())
			
class Portfolioform(forms.Form):
	tickers=forms.CharField(    label="Stock Tickers ",
	widget=forms.TextInput(attrs={'placeholder':'e.g.,RELIANC.NS,TCS.NS,INFY.NS'}),
	help_text="Enter stock tickers separated by commas. "
	)
	investment= forms.FloatField( label="Investment Amount in rupees",
		min_value=0,help_text="Enter the total investment amount. "	)