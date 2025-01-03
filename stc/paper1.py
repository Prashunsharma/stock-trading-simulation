import yfinance as yf
import datetime

class PaperTradingApp:
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance  # Initial cash balance
        self.portfolio = {}  # Holds stock symbol and amount of shares
        self.transaction_history = []  # Logs of buy/sell actions

    def get_stock_price(self, ticker):
        """Fetch current stock price using yfinance."""
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        else:
            print("Error: Could not retrieve data for", ticker)
            return None

    def buy_stock(self, ticker, num):
        """Simulate buying stock by updating portfolio and balance."""
        price = self.get_stock_price(ticker)
        if price is None:
            print(f"Could not buy {ticker}: Price data not available.")
            return

        
        cost = num * price

        if cost > self.balance:
            print("Insufficient balance to buy.")
            return

        self.balance -= cost
        self.portfolio[ticker] = self.portfolio.get(ticker, 0) + num
        self.transaction_history.append({
            'type': 'BUY',
            'ticker': ticker,
            'shares': num,
            'price': price,
            'date': datetime.datetime.now()
        })
        print(f"Bought {num} shares of {ticker} at ${price:.2f} each. Cost: ${cost:.2f}")
    
    def sell_stock(self, ticker, num_shares):
        """Simulate selling stock by updating portfolio and balance."""
        if ticker not in self.portfolio or self.portfolio[ticker] < num_shares:
            print("Not enough shares to sell.")
            return
        
        price = self.get_stock_price(ticker)
        if price is None:
            print(f"Could not sell {ticker}: Price data not available.")
            return

        revenue = num_shares * price
        self.balance += revenue
        self.portfolio[ticker] -= num_shares
        if self.portfolio[ticker] == 0:
            del self.portfolio[ticker]

        self.transaction_history.append({
            'type': 'SELL',
            'ticker': ticker,
            'shares': num_shares,
            'price': price,
            'date': datetime.datetime.now()
        })
        print(f"Sold {num_shares} shares of {ticker} at ${price:.2f} each. Revenue: ${revenue:.2f}")

    def display_portfolio(self):
        """Display the current portfolio and balance."""
        portfolio_data = []
        portfolio_data.append("\n--- Portfolio ---")
        portfolio_data.append(f"Cash Balance: ${self.balance:.2f}")
        for ticker, shares in self.portfolio.items():
            price = self.get_stock_price(ticker)
            if price is not None:
                portfolio_data.append(f"{ticker}: {shares} shares at ${price:.2f} each (Total: ${shares * price:.2f})")
        portfolio_data.append("\n--- Transaction History ---")
        for transaction in self.transaction_history:
            portfolio_data.append(f"{transaction['date']}: {transaction['type']} {transaction['shares']} shares of {transaction['ticker']} at ${transaction['price']:.2f}")
        return portfolio_data

# Instantiate the app and simulate some trades

Ticker= input("Enter the name of the stock ! ")
num= int(input("enter the number of stocks you want to buy "))
app = PaperTradingApp()
check= input("Press b to buy and s for sell ")


# Example transactions to test the application
if(check=="b"):
   app.buy_stock("Ticker", num)
elif(check=="s"):
       # Buy $500 worth of Apple stock
  app.sell_stock("Ticker",num ) 
    # Sell 1 share of Apple stock
else :
    print("wrong input")
# Display portfolio and transaction history
portfolio_output = app.display_portfolio()
portfolio_output
