import json
import requests
from datetime import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
from user import User

def retrieval_stock_info():
    st.title("Get Recommendations from Analyst")

    ticker = st.text_input('Please input stock ticker')
    if ticker != '':
        stock = yf.Ticker(ticker)
        range = st.selectbox('Select Range', ['1y','3mo', '1mo', '5d', 'ytd', '5y', 'max'])
    
        hist = stock.history(period=range)
        st.line_chart(hist['Close'])

        # Recommendations
        st.subheader('Analyst recommendations')
        st.dataframe(stock.recommendations.iloc[::-1])

        # Stock Event
        st.subheader('Stock Event')
        st.dataframe(stock.calendar)

def retrieval_account_info():

    BASIC_URL = 'http://datastudio.simnectzplatform.com/gateway/SIMNECTZ/'
    TOKEN = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9'
    AUTHORIZATION = '5e46871f34a6e5748c2c4171319dbe6d3dec43c295c5949f056e3319'

    HEADERS = {
        'token': TOKEN,
        'Authorization': AUTHORIZATION,
        'Content-Type': 'application/json'
    }

    call_url = BASIC_URL + 'term_deposit_enquiry_presentation///termDeposit/enquiry'
    input_dict = {
        'accountnumber': "HK760001001000000005100",
        'tdnumber': "000000001"
    }

    response = requests.post(url = call_url, data = json.dumps(input_dict), headers = HEADERS)
    return response.json()
    #1

class Profile():
    def __init__(self, balance=0., name='FTEC3002'):

        self.stockProfile = pd.DataFrame(np.empty((0, 5)))
        self.stockProfile.columns = ['Date', 'Time', 'Symbol', 'Quantity', 'Cost']
        self.balance = float(balance)
        self.name = name
        self.trade_info = pd.DataFrame(data={'Data': [],
                                             'L/S': [],
                                             'Symbol': [],
                                             'Quantity': [],
                                             'Cost/Price': [],
                                             'Profit': [],
                                             'Trade Fee': []
                                             })

    def to_deposit(self, money=0.):
        if isinstance(money, float) or isinstance(money, int):
            self.balance += float(money)
            st.text("Current Balance: %.3f" % self.balance)
        else:
            st.text("Input Error")

    def to_withdrawal(self, money=0.):

        if isinstance(money, float) or isinstance(money, int):
            if money > self.balance:
                st.text("Insufficient Balance")
            else:
                self.balance -= float(money)
                st.text("Current Balance: %.3f" % self.balance)
        else:
            st.text("Input Error")

    def to_short(self, symbol, quantity, price):
        now = datetime.now()
        trade_date = now.strftime("%d/%m/%Y")
        trade_time = now.strftime("%H:%M:%S")
        if symbol in list(self.stockProfile['Symbol']):
            temp_count = 0
            for x in list(self.stockProfile['Symbol']):
                if symbol == x:
                    break
                temp_count += 1
            if 0 > quantity > self.stockProfile['Quantity'][temp_count]:
                st.text('Quantity Error')
            elif float(quantity) == self.stockProfile['Quantity'][temp_count]:
                self.balance += self.stockProfile['Cost'][temp_count]*quantity
                profit = (price - self.stockProfile['Cost'][temp_count]) * quantity
                self.to_deposit(profit)
                self.stockProfile = self.stockProfile.drop([temp_count])
                st.text('Short ' + str(quantity) + ' ' + symbol + ' at ' + str(price))
                st.text('Profit: %.3f' % profit)
                return profit
            else:
                self.stockProfile['Date'].iloc[temp_count] = trade_date
                self.stockProfile['Time'].iloc[temp_count] = trade_time
                self.stockProfile['Quantity'].iloc[temp_count] -= quantity
                self.balance += self.stockProfile['Cost'][temp_count] * quantity
                profit = (price - self.stockProfile['Cost'][temp_count]) * quantity
                self.to_deposit(profit)
                st.text('Long ' + str(quantity) + ' ' + symbol + ' at ' + str(price))
                st.text('Profit: %.3f' % profit)
                return profit
        else:
            st.text("Symbol Error")

    def to_long(self, symbol, quantity, cost):
        now = datetime.now()
        trade_date = now.strftime("%d/%m/%Y")
        trade_time = now.strftime("%H:%M:%S")

        if 0 > quantity:
            st.text('Quantity Error')

        else:
            if symbol in list(self.stockProfile['Symbol']):
                temp_count = 0
                for x in list(self.stockProfile['Symbol']):
                    if symbol == x:
                        break
                    temp_count += 1

                self.balance -= cost * quantity
                temp_cost = (self.stockProfile['Cost'][temp_count] * self.stockProfile['Quantity'][temp_count] +
                             cost * quantity) / (self.stockProfile['Quantity'][temp_count] + quantity)
                temp_quantity = self.stockProfile['Quantity'][temp_count]
                cost = temp_cost

                self.stockProfile['Date'].iloc[temp_count] = trade_date
                self.stockProfile['Time'].iloc[temp_count] = trade_time
                self.stockProfile['Symbol'].iloc[temp_count] = symbol
                self.stockProfile['Quantity'].iloc[temp_count] = temp_quantity + quantity
                self.stockProfile['Cost'].iloc[temp_count] = cost
                # new_column = pd.Series([trade_date, trade_time, symbol, quantity, cost])
                # self.stockProfile = self.stockProfile.append(new_column, ignore_index=True)
                st.text('Long ' + str(quantity) + ' ' + symbol + ' at ' + str(cost))

            else:
                new_column = [trade_date, trade_time, symbol, quantity, cost]
                self.stockProfile.loc[len(self.stockProfile)] = new_column
                self.balance -= cost*quantity
                st.text('Long ' + str(quantity) + ' ' + symbol + ' at ' + str(cost))

    def show_profile(self):
        st.text('Balance: ' + str(self.balance))
        if len(self.stockProfile) == 0:
            st.text('Empty Profile')
        else:
            st.text(self.name + '\'s Stock Profile:\n' + str(self.stockProfile))


    def show_t_history(self):
        if len(self.trade_info) == 0:
            st.text('No transactions')
        else:
            st.text(self.trade_info)

    def to_compare(self, comparedIndex='.SPX'):
        # to compare return with market index, DJI, SPX etc.

        pass

    def market_info(self, date, act, symbol, quantity, CorP, profit, fee):
        temp_len = len(self.trade_info)
        self.trade_info.loc[temp_len] = [date, act, symbol, quantity, CorP, profit, fee]

    def market_fee(self, quan):
        self.to_withdrawal(max(quan * 0.0049, 0.99)
                           + 0.003 * quan
                           + max(1., 0.005 * quan))
        return max(quan * 0.0049, 0.99) + 0.003 * quan + max(1., 0.005 * quan)

def main_portfolio():
    st.title("Welcome to Mock Investment")
    st.header('Here is your Virtual Account')
    virtual_account = Profile()
    user = User()
    st.text("Current Balance: %.3f" % user.fetch_info('virtual'))
    # virtual_account.to_deposit(1000000)

    # st.subheader(virtual_account.show_profile())

    trans = st.selectbox('Transaction', ('Long', 'Short'))

    if trans == 'Long':
        symbol = st.text_input('Ticker')
        quantity = st.number_input('Quantity')
        cost = st.number_input('Cost')

        if len(symbol) != 0 and quantity > 0 and cost > 0:
            virtual_account.to_long(symbol, quantity, cost)
            amount = int(quantity * cost)
            user.edit_info('virtual', user.fetch_info('virtual')-int(amount))
            st.text('Transaction successful')


    if trans == 'Short':
        symbol = st.text_input('Ticker')
        quantity = st.number_input('Quantity')
        price = st.number_input('Price')

        if len(symbol) != 0 and quantity > 0 and price > 0:
            virtual_account.to_short(symbol, quantity, price)
            amount = int(quantity * price)
            user.edit_info('virtual', user.fetch_info('virtual')-int(amount))
            st.text('Transaction successful')

    expected_return = 0.032

    if len(virtual_account.stockProfile['Symbol']) > 0:
        for stock_index in range(len(virtual_account.stockProfile['Symbol'])):
            expected_return += float((virtual_account.stockProfile['Cost'][stock_index]
                                * virtual_account.stockProfile['Quantity'][stock_index])/
                                virtual_account.balance)* 0.1

        risk_free = 0.02
        volatility = 0.2
        sharpe_ratio = (expected_return - risk_free)/volatility
        var = expected_return - 1.65*(0.95) #VaR 5% in 1 year

        st.text('Expected return: ' + str(round(expected_return, 5)*100) + '%')
        st.text('Volatility: ' + str(round(volatility, 5)*100) + '%')
        st.text('Value at Risk: ' + str(round(var, 5)*100) + '%')
        st.text('Shapre Ratio: ' + str(round(sharpe_ratio, 5)*100) + '%')


    # st.header('Portfolio')
    # st.subheader('Asset')
    # # st.text(retrieval_account_info())
    # risk_free = 0.02

    # virtual_account = Profile()
    # if len(virtual_account.stockProfile['Symbol']) > 0:
    #     for stock_index in len(virtual_account.stockProfile['Symbol']):
    #         expected_return += ((virtual_account.stockProfile['Cost'][stock_index]
    #                             * virtual_account.stockProfile['Quantity'][stock_index])/
    #                             virtual_account.balance)* 0.1


    #     volatility = 0.2
    #     sharpe_ratio = (expected_return - risk_free)/volatility
    #     var = expected_return - 1.65(0.95) #VaR 5% in 1 year

    #     st.text('Expected return: %s', expected_return)
    #     st.text('Volatility: %s', volatility)
    #     st.text('Value at Risk: %s', var)
    #     st.text('Shapre Ratio: %s', sharpe_ratio)


# side = st.sidebar.selectbox('Function', ('Stock Info', 'Portfolio', 'Virtual Account'))
# if side == 'Stock Info':
#     st.header('Stock Info')
#     st.subheader('Input stock ticker, eg. AAPL')
#     # get stock info
#     retrieval_stock_info()




# elif side == 'Portfolio':
#     st.header('Portfolio')
#     st.subheader('Asset')
#     st.text(retrieval_account_info())
#     risk_free = 0.02



#     if len(virtual_account.stockProfile['Symbol']) > 0:
#         for stock_index in len(virtual_account.stockProfile['Symbol']):
#             expected_return += ((virtual_account.stockProfile['Cost'][stock_index]
#                                 * virtual_account.stockProfile['Quantity'][stock_index])/
#                                 virtual_account.balance)* 0.1


#         volatility = 0.2
#         sharpe_ratio = (expected_return - risk_free)/volatility
#         var = expected_return - 1.65(0.95) #VaR 5% in 1 year

#         st.text('Expected return: %s', expected_return)
#         st.text('Volatility: %s', volatility)
#         st.text('Value at Risk: %s', var)
#         st.text('Shapre Ratio: %s', sharpe_ratio)


# elif side == 'Virtual Account':
#     st.header('Virtual Account')
#     virtual_account = Profile()
#     virtual_account.to_deposit(1000000)

#     st.subheader(virtual_account.show_profile())

#     trans = st.selectbox('Transaction', ('Long', 'Short'))

#     if trans == 'Long':
#         symbol = st.text_input('Ticker')
#         quantity = st.number_input('Quantity')
#         cost = st.number_input('Cost')

#         if len(symbol) != 0 and quantity >= 0 and cost >= 0:
#             virtual_account.to_long(symbol, quantity, cost)
#             # st.text('Transaction successful')


#     if trans == 'Short':
#         symbol = st.text_input('Ticker')
#         quantity = st.number_input('Quantity')
#         price = st.number_input('Price')

#         if len(symbol) != 0 and quantity >= 0 and price >= 0:
#             virtual_account.to_short(symbol, quantity, price)
#             # st.text('Transaction successful')

#     expected_return = 0

#     if len(virtual_account.stockProfile['Symbol']) > 0:
#         for stock_index in range(len(virtual_account.stockProfile['Symbol'])):
#             expected_return += float((virtual_account.stockProfile['Cost'][stock_index]
#                                 * virtual_account.stockProfile['Quantity'][stock_index])/
#                                 virtual_account.balance)* 0.1

#         risk_free = 0.02
#         volatility = 0.2
#         sharpe_ratio = (expected_return - risk_free)/volatility
#         var = expected_return - 1.65*(0.95) #VaR 5% in 1 year

#         st.text('Expected return: ' + str(round(expected_return, 5)*100) + '%')
#         #st.text('Volatility: %s', volatility)
#         #st.text('Value at Risk: %s', var)
#         #st.text('Shapre Ratio: %s', sharpe_ratio)
