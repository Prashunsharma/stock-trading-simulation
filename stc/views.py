from django.shortcuts import render,redirect
from .models import UserStock 
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .froms import SignUpForm , StockSearchForm ,StockForecastForm,Portfolioform
import yfinance as yf           
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
import base64
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date,timedelta
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from django.http import JsonResponse
from plotly.io import to_html
import yfinance as yf 
from pypfopt import EfficientFrontier , risk_models , expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation , get_latest_prices
from io import BytesIO

def login_user(request):
    if request.method=="POST":
         username=request.POST['username']
         password=request.POST['password']
         user=authenticate(request,username=username,password=password)
         if user is not None:
              login(request,user)
              messages.success(request,(f"You have been logged  in sucessfully {username} "))
              return redirect('home')
         else :
               messages.success(request,("There was an error try again ..."))
               return redirect('login')
    else : 
        return render(request,'login.html',{})

def about(request):
    return render(request , 'about.html',{}) 

def register_user(request):
    form= SignUpForm()
    if request.method=="POST":
         form=SignUpForm(request.POST)
         if form.is_valid():
               form.save()
               username=form.cleaned_data['username']
               password=form.cleaned_data['password1']
               user=authenticate(username=username,password=password)
               login(request,user)
               messages.success(request,(f"You are registered {username} Welcome..."))
               return redirect('home')
         else :
               messages.success(request,("There is some problem ..."))
               return redirect('register')
    else :          
        return render(request, 'register.html',{'form':form})

def logout_user(request):
    logout(request)
    messages.success(request, (" You have been logout thanks ....."))
    return redirect('home')

def home (request):
    stock_data = None

    if request.method == 'POST':
        form = StockSearchForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            
            # Fetch stock data using yfinance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract relevant details
            stock_data = {
                'ticker': ticker.upper(),
                'name': info.get('longName', 'N/A'),
                'price': stock.fast_info.last_price,
                'high': info.get('dayHigh', 'N/A'),
                'low': info.get('dayLow', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'previous_close': info.get('previousClose', 'N/A'),
            }
    else:
        form = StockSearchForm()

    return render(request, 'home.html', {'form': form, 'stock_data': stock_data})

@login_required
@transaction.atomic 
def buy_sell_views(request):
     if request.method == 'POST':
        action = request.POST.get('action')  # 'buy' or 'sell'
        ticker = request.POST.get('ticker')
        quantity = int(request.POST.get('quantity'))
        
        # Fetch stock price using yfinance
        stock = yf.Ticker(ticker)
        current_price = stock.fast_info.last_price

        # Validate inputs
        if not current_price:
            messages.error(request, f"Could not fetch price for {ticker}.")
            return redirect('portfolio')
        
        total_cost = current_price * quantity
        user_stock, created = UserStock.objects.get_or_create(
        user=request.user,
        defaults={'stocks': {}, 'balance': 1000000}  # Set initial values if creating a new entry
    )

        if action == 'buy':
            if user_stock.balance < total_cost:
                messages.error(request, "Insufficient balance.")
            else:
                user_stock.balance -= round(total_cost,3)
                user_stock.stocks[ticker] = user_stock.stocks.get(ticker, 0) + quantity
                messages.success(request, f"Bought {quantity} shares of {ticker} at ₹{current_price} .")
        
        elif action == 'sell':
            if user_stock.stocks.get(ticker, 0) < quantity:
                messages.error(request, f"Not enough shares to sell {quantity} of {ticker}.")
            else:
                user_stock.balance += round(total_cost,3)
                user_stock.stocks[ticker] -= quantity
                if user_stock.stocks[ticker] <= 0:
                    del user_stock.stocks[ticker]
                messages.success(request, f"Sold {quantity} share of {ticker} at  ₹{current_price} .")
        
        user_stock.save()  

    
    
     
     return render(request, 'buy_sell.html')


def stock_graph_view(request):
    stock_name = request.GET.get('stock_name', '').strip()
    date_range = request.GET.get('date_range', '1y')
    graph_type = request.GET.get('graph_type', 'line')
    graph_html = None
    graphic = None

    if stock_name:
        try:
            # Define the period based on the selected time period
            if date_range not in ['1y', '5y', '1m', '6m']:
                return HttpResponse("Invalid date range. Use '1y', '5y', '1m', or '6m'.")

            # Fetch stock data using yfinance
            stock_data = yf.Ticker(stock_name)
            df = stock_data.history(period=date_range)

            # Plot the graph based on selected graph type
            if graph_type == 'candlestick':
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name=f'{stock_name} Candlestick'
                )])
                fig.update_layout(title=f'{stock_name} Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
                graph_html = fig.to_html(full_html=False)

            elif graph_type == 'line':
                plt.figure(figsize=(10, 6))
                plt.plot(df['Close'], label=f"{stock_name} Close Price")
                plt.title(f"{stock_name} Stock Price Over {date_range}")
                plt.xlabel("Date")
                plt.ylabel("Close Price")
                plt.legend()
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_png = buf.getvalue()
                buf.close()
                graphic = base64.b64encode(image_png).decode('utf-8')
                plt.close()

            elif graph_type == 'moving_average':
                plt.figure(figsize=(10, 6))
                df['MA20'] = df['Close'].rolling(window=20).mean()
                df['MA50'] = df['Close'].rolling(window=50).mean()
                plt.plot(df['Close'], label=f"{stock_name} Close Price")
                plt.plot(df['MA20'], label='20-Day Moving Average')
                plt.plot(df['MA50'], label='50-Day Moving Average')
                plt.title(f"{stock_name} Moving Averages Over {date_range}")
                plt.xlabel("Date")
                plt.ylabel("Price")
                plt.legend()

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_png = buf.getvalue()
                buf.close()
                graphic = base64.b64encode(image_png).decode('utf-8')
                plt.close()

            elif graph_type == 'volume':
                plt.figure(figsize=(10, 6))
                fig, ax1 = plt.subplots(figsize=(10, 6))

                # Plot the closing price on the primary y-axis
                ax1.plot(df.index, df['Close'], color='blue', label="Close Price")
                ax1.set_xlabel("Date")
                ax1.set_ylabel("Close Price", color='blue')
                ax1.tick_params(axis='y', labelcolor='blue')

                # Create a secondary y-axis for the volume
                ax2 = ax1.twinx()
                ax2.bar(df.index, df['Volume'], color='gray', alpha=0.3, label="Volume")
                ax2.set_ylabel("Volume", color='gray')
                ax2.tick_params(axis='y', labelcolor='gray')

                plt.title(f"{stock_name} Volume and Price Over {date_range}")
                plt.legend(loc="upper left")

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_png = buf.getvalue()
                buf.close()
                graphic = base64.b64encode(image_png).decode('utf-8')
                plt.close()
    
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
  



    return render(request, 'stock_chart.html', {
        'graphic': graphic,
        'graph_html': graph_html
    })

def stock_forecast(request):
    # Default values for stock symbol and date range
    form = StockForecastForm()
    forecast_data = None
    raw_plot_html = None
    forecast_plot_html = None
    components_plot_html = None

    if request.method == 'POST':
        form = StockForecastForm(request.POST)
        if form.is_valid():
            # Get cleaned form data
            stock = form.cleaned_data['stock']
            time_period_type = form.cleaned_data['time_period_type']
            time_period_value = form.cleaned_data['time_period_value']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Convert prediction period to days
            period = time_period_value
            if time_period_type == 'Years':
                period *= 365
            elif time_period_type == 'Months':
                period *= 30
            elif time_period_type == 'Weeks':
                period *= 7

            # Fetch stock data
            try:
                stock_data = yf.download(stock, start=start_date, end=end_date)
                stock_data.reset_index(inplace=True)

                # Prepare data for Prophet
                df_train = stock_data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

                # Train Prophet model
                model = Prophet()
                model.fit(df_train)

                # Predict future stock prices
                future = model.make_future_dataframe(periods=period)
                forecast = model.predict(future)

                # Create plots
                # Raw data plot
                raw_plot = go.Figure()
                raw_plot.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Open'], name="Open Price"))
                raw_plot.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name="Close Price"))
                raw_plot.update_layout(
                    title="Stock Prices with Rangeslider",
                    xaxis_rangeslider_visible=True
                )
                raw_plot_html = raw_plot.to_html(full_html=False)

                # Forecast plot
                forecast_plot_html = plot_plotly(model, forecast).to_html(full_html=False)

                # Forecast components
               

                # Extract forecast data
                forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(period).to_dict(orient='records')

            except Exception as e:
                form.add_error(None, f"An error occurred: {e}")

    return render(request, 'forecast.html', {
        'form': form,
        'forecast_data': forecast_data,
        'raw_plot_html': raw_plot_html,
        'forecast_plot_html': forecast_plot_html,
        'components_plot_html': components_plot_html,
    })

def portfolio_opt(request):
    chart=None
    allocation=None
    leftover=None
    performance=None

    if request.method=="POST":
        form= Portfolioform(request.POST)
        if form.is_valid():
            tickers=form.cleaned_data['tickers'].replace(" ","").split(",")
            investment=form.cleaned_data['investment']

            data=yf.download(tickers, start="2018-01-01", end="2023-01-01")["Adj Close"]

            mu=expected_returns.mean_historical_return(data)
            S=risk_models.sample_cov(data)

            ef=EfficientFrontier(mu,S)
            weights=ef.max_sharpe()
            cleaned_weights=ef.clean_weights()

            latest_prices=get_latest_prices(data)
            da=DiscreteAllocation(cleaned_weights,latest_prices,total_portfolio_value=investment)
            allocation , leftover= da.lp_portfolio()
            performance=ef.portfolio_performance(verbose=False)
            
            fig, ax=plt.subplots(figsize=(8,6), dpi=100)
            labels=list(cleaned_weights.keys())
            sizes=list(cleaned_weights.values())
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
            ax.set_title("Optimized Portfolio Allocation", fontsize=16)
            #convert plot into a base64 string 
            buffer = BytesIO()
            plt.savefig(buffer, format='png',bbox_inches='tight')
            buffer.seek(0)
            chart = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close(fig)
    else :
        form =Portfolioform()            

    return render(request, 'portfolio.html',
                  {
                      'form':form,
                      'chart':chart,
                      'allocation': allocation,
                      'leftover': leftover ,
                      'performance': performance
                  })