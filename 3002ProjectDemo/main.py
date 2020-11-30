import streamlit as st 
import pandas as pd
from PIL import Image
import numpy as np
import webbrowser
import plotly.graph_objects as go

from user import User
from mock_investment import Mock_investment
from streamlit_wang import Transfer
from simnectz_william import retrieval_stock_info, main_portfolio

from stock_portfolio import main_func_for_stock_portfolio

class Functionality(object):
    def __init__(self):
        self.user = User()
        self.mock = Mock_investment()
        self.T = Transfer()
        self.main_page()
    
    def main_page(self):
        st.sidebar.markdown("# Service We Provide")
        option = st.sidebar.selectbox("",["Select your Option", "Login your own account", "Create your new account", 
                                          "View your account", "Transfer", "Stock Exploration","Concept Education", 
                                          "Historical Performance", "Analyst Recommendations", "Mock Training", "Mock Investment", "Real Investment"
                                          ])

        if option == "Select your Option":
            self.landing_page()
        elif option == "Login your own account":
            self.login()
        elif option == "Create your new account":
            self.create_account()
        elif option == "View your account":
            self.view_account()
        elif option == "Transfer":
            self.T.transfering()
        elif option == "Stock Exploration":
            webbrowser.open_new_tab('https://stock-prediction-dashboard.herokuapp.com')
        elif option == "Concept Education":
            self.concept()
        elif option == "Historical Performance":
            main_func_for_stock_portfolio()
        elif option == "Analyst Recommendations":
            retrieval_stock_info()
        elif option == "Mock Training":
            self.mock.mock_invest()
        elif option == "Mock Investment":
            main_portfolio()
        elif option == "Real Investment":
            self.mock.invest()
                 
    def landing_page(self):
        st.image(Image.open('landing_page.png'))
    
    def login(self):
        st.title("EDUVESTMENT")
        st.selectbox("Please enter your username",[self.user.fetch_info('username')])
        st.selectbox("Please enter your password",['*' * len(self.user.fetch_info('password'))])
        st.checkbox('Remember me', value=True)
        login = st.button("LOGIN")
        if login:
            st.write('Login Successfully')
            st.balloons()
    
    def create_account(self):
        st.title("Create Your Account")
        st.write("## Please fill in all the infomation to open your account!")
        st.text_input("Enter your first name:")
        st.text_input("Enter your last name:")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:")
        st.text_input("Enter your password again:")
        st.selectbox("Choose your gender:", ['--', 'Male', 'Female'])
        st.selectbox("Enter your HK Identity Card Number:",["--", "M622850(2)"])
        st.selectbox("Enter your residence address:",["--", "The Chinese University of Hong Kong, Shatin, N.T., Hong Kong"])
        st.selectbox("Enter your phone number:",["--", "65732398"])
        st.selectbox("Enter your email address",["--", "1155108765@link.cuhk.edu.hk"])
        bank_name = st.selectbox("Enter your registered bank name:",["--", "Hang Seng"])
        account_number = st.selectbox("Enter your bank account:",["--", "753 087934 776"])

        if st.button("Open Account!"):
            st.balloons()
            st.write('Your account has been created successfully!')
            st.write('Please remember your username and password to login your account.')
            self.user.edit_info('username', username)
            self.user.edit_info('password', password)
            self.user.edit_info('account_number', account_number)
            self.user.edit_info('bank_name', bank_name)
            self.user.edit_info('balance', 100000)
            self.user.edit_info('deposit', 21000)
            self.user.edit_info('fund', 32000)
            self.user.edit_info('bond', 5000)
            self.user.edit_info('stock', 27000)
            self.user.edit_info('foreign_exchange', 15000)
            self.user.edit_info('option', 0)

            self.user.edit_info('balance_i', 8590)
            self.user.edit_info('deposit_i', 630)
            self.user.edit_info('fund_i', 1920)
            self.user.edit_info('bond_i', 520)
            self.user.edit_info('stock_i', 4320)
            self.user.edit_info('foreign_exchange_i', 1200)
            self.user.edit_info('option_i', 0)

            self.user.edit_info('virtual', 50000)

    def view_account(self):
        st.title("Here is your basic account information:")
        account_title = self.user.fetch_info('account_number') + '[' + self.user.fetch_info('bank_name') + ']'
        account_value = st.selectbox("choose your account:",[account_title, "add more account"])
        if account_value != "--":
            account_name = ['deposit', 'fund', 'bond', 'stock', 'foreign exchange', 'option']
            st.write("Your account balance: HKD %.2f" % self.user.fetch_info('balance'))
            st.write("## Quick Transfer to Funds:")
            p1 = st.checkbox("SPDR Portfolio S&P 500 Growth ETF (SPYG)   ")
            if p1:
                st.write("Issuer: Direxion")
                st.write("Category: Large Cap Growth Equities")
                st.write("Anualized Return: 5.3%")
                st.write("Expense Ratio: 0.35%")
            st.checkbox("iShares MSCI New Zealand ETF (ENZL)")
            st.checkbox("Global X Silver Miners ETF (SIL)")
            st.checkbox("Sprott Gold Miners ETF (SGDM)")
            ETF_return = st.button("Make an order")
            if ETF_return:
                st.text_input("Money amount you would like to transfer")
                ETF_return = st.button("Send the order")

            st.write("## Your Account Details:")
            st.write("Amount in deposit: HKD %.2f" % self.user.fetch_info('deposit'))
            st.write("Amount in fund: HKD %.2f" % self.user.fetch_info('fund'))
            st.write("Amount in bond: HKD %.2f" % self.user.fetch_info('bond'))
            st.write("Amount in stock: HKD %.2f" % self.user.fetch_info('stock'))
            st.write("Amount in foreign exchange: HKD %.2f" % self.user.fetch_info('foreign_exchange'))
            st.write("Amount in option: HKD %.2f" % self.user.fetch_info('option'))
            account_list = [self.user.fetch_info('deposit'), self.user.fetch_info('fund'), self.user.fetch_info('bond'),
                            self.user.fetch_info('stock'), self.user.fetch_info('foreign_exchange'), self.user.fetch_info('option')]
            self.plot_pie_chat(account_list, account_name, 'Resource Allocation')

            st.write("Total interst earned: HKD %.2f" % self.user.fetch_info('balance_i'))
            st.write("Interst earned from deposit: HKD %.2f" % self.user.fetch_info('deposit_i'))
            st.write("Interst earned from fund: HKD %.2f" % self.user.fetch_info('fund_i'))
            st.write("Interst earned from bond: HKD %.2f" % self.user.fetch_info('bond_i'))
            st.write("Interst earned from stock: HKD %.2f" % self.user.fetch_info('stock_i'))
            st.write("Interst earned from foreign exchange: HKD %.2f" % self.user.fetch_info('foreign_exchange_i'))
            st.write("Interst earned from option: HKD %.2f" % self.user.fetch_info('option_i'))
            interest_list = [self.user.fetch_info('deposit_i'), self.user.fetch_info('fund_i'), self.user.fetch_info('bond_i'),
                            self.user.fetch_info('stock_i'), self.user.fetch_info('foreign_exchange_i'), self.user.fetch_info('option_i')]
            self.plot_pie_chat(interest_list, account_name, 'Interest Earned')
    
    def plot_pie_chat(self, weights, checked, sentence):
        w = np.array(weights)
        s = np.array(checked)

        pie = go.Figure(data = [go.Pie(labels = s[w > 0], values = w[w > 0])])
        pie.update_layout(title = sentence)
        st.plotly_chart(pie)

    def concept(self):
        st.title("Expore more concept in stock market")
        st.write("## Concept 1: What is a market cap?")
        a1 = st.button("Check Answer")
        a2 = st.button("See Examples")
        if a1:
            st.write("The full phrase is “market capitalization,” which is the total value of the company.")
            st.write("When investors talk about “market caps,” they’re simply referring to how big a company is.")
            st.write("You arrive at the value by multiplying the number of shares it has on the stock market by the price per share.")
            
        if a2:
            st.write("For example, a big company like Apple (AAPL) is considered a large-cap stock.")
            st.write("As of today, Apple has 4,519,180,000 shares outstanding on the public markets. Their stock price is at $209.12. If you multiply those two numbers together, you arrive at a market capitalization of $945 billion. Wow.")
            st.write("A small cap stock is a small company, such as GoPro (GPRO). As of today, their market cap is only $553 million.")
        
        st.write("## Concept 2: What are a stock’s sector and industry?")
        a3 = st.button("Stock Sector")
        a4 = st.button("Stock Industry")
        st.write("## Concept 3: What is an index?")
        a5 = st.button("Index Explaination")
        a6 = st.button("See Example")
        st.write("## Concept 4: What is an investing style?")
        a7 = st.button("Check Concept")
        a8 = st.button("More Examples")
        st.write("## Concept 5: How are stocks different from other investments?")
        a9 = st.button("Comparison")
        a10 = st.button("Main differences")
        st.write("## Concept 6: What is a bull market vs. a bear market?")

        a11 = st.button("Bull Market")
        if a11:
            st.write("When people talk about a bull market, they generally mean an environment in which stock prices are going up and are expected to keep going up. These are the good times when stocks keep grinding higher and higher.")
        a12 = st.button("Bear Market")
        if a12:
            st.write("On the other hand, a bear market is defined as a 20%+ decline in market prices over a two-month period. Typically a bear market will see 20%+ declines across several major indexes, such as the S&P 500, Dow Jones Industrial Average (DJIA), and Nasdaq.")
        
        st.write("## Concept 7: What does it mean to beat the market?")
        a13 = st.button("Check your answer")
        st.write("## Concept 8: What is short ratio")
        a15 = st.button("Short Ratio")
        a16 = st.button("Exercises")
        st.write("## Concept 9: What can we learn from close price?")
        a17 = st.button("Close Price")
        a18 = st.button("More Concepts")
        st.write("## Concept 9: What are some common strategy?")
        a19 = st.button("Strategies")
        a20 = st.button("Some Examples")

    def education_list(self):
        if option == "Stocks Exploration":
            webbrowser.open_new_tab('https://stock-prediction-dashboard.herokuapp.com')
        elif option == "Historical Performance":
            main_func_for_stock_portfolio()

if __name__ == "__main__":
    # command for running: streamlit run [filename].py
    Demo = Functionality()
