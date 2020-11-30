import streamlit as st # pip install streamlit
import pandas as pd
from datetime import date
from user import User

from utils_jade import retrieval_payee_info_list,load_historical_price,input_portforlio,retrieval_account_balace
from stock_portfolio_jade import display_multiple_selection_bar,optimize,plotstocks,display_performance,plot_pie_chat

class Mock_investment(object):
    def __init__(self):
        self.user = User()
        # st.sidebar.markdown("# Service We Provide")
        # self.option = st.sidebar.selectbox("",["Education", "Account Opening", "Investment","Mocking Investment", "Account Info"])

        # if self.option == "Account Opening":
        #     self.open_account()
        # elif self.option == "Account Info":
        #     self.account_info()
        # elif self.option == "Mocking Investment": # mocking investment
        #     self.mock_invest()
        # elif self.option == "Investment":
        #     self.invest()

    def open_account(self):
        st.write("## Please fill in all the infomation to open your account!")
        st.text_input("Enter your first name:")
        st.text_input("Enter your last name:")
        st.selectbox("Enter your gerder:", ['-'*5, 'Male', 'Female'])
        st.text_input("Enter your HK Identity Card Number:")
        st.text_input("Enter your residence address:")
        st.selectbox("Enter your account type:", ['-'*5, 'Deposit', 'Credit', 'Fund', 'Stock', 'Foreign Exchange'])
        status = st.button("Open Account!")
        if status:
            self.page_success()

    def page_success(self):
        st.write("## Successful in opening your account!")

    def account_info(self):
        payee_category_id = st.selectbox("Select one category", ['001', '002', '003', '004'])
        payee_info_list = retrieval_payee_info_list(payee_category_id)

        payee_name_list = ['-'*5] + [item['payeename'] for item in payee_info_list]
        payee_name = st.selectbox("Your potential payee", payee_name_list)

        if payee_name != payee_name_list[0]:
            for payee in payee_info_list:
                if payee_name == payee['payeename']:
                    detials_df = pd.json_normalize(payee)
                    break
            st.dataframe(detials_df.transpose()[0])

# newly added function: mock investing

    def mock_invest(self):
        st.title("Welcome to Mock Investment!")
        st.write("### Suppose you are helping Morty to invest: Morty can invest at any time in history! Let's see what would happen in Morty's portfolio!")
        amount = st.text_input("Enter how much you hope to invest from Morty's $100,000 saving:",10000)
        start = st.date_input("Enter when you hope Morty to invest:",date(2019,1,1))

        snp = pd.read_csv('snp10.csv',index_col=0)
        # mutiple selection bar
        checked = display_multiple_selection_bar(snp)
        # fetch relative data
        data = snp[checked]
        dates = data.index.values
        data.index = pd.to_datetime(data.index)

        weights, folio, performance = optimize(data)
        data['optimized portfolio'] = folio
        data_select = data.loc[start:]
        data_select.index = data_select.index.date
        growth = (data_select / data_select.iloc[0,:]) * 10000

        st.write("### Tell us the weights of your portfolio!")
        input_w = []
        for i in range(len(checked)):
            w = st.text_input(checked[i],round(1/len(checked),2))
            input_w.append(float(w))

        status = st.button("Performance of Morty's portfolio")
        status2 = st.button("Have a look at the optimized portfolio?")
        status3 = st.button("Make a comparison")

        if status and sum(input_w)-1 <=0.1:
            data_compute = data_select.iloc[:,:len(checked)]
            folio_new = input_portforlio(data_compute,input_w)
            data_compute['your portfolio'] = folio_new
            growth_new = (data_compute / data_compute.iloc[0,:]) * 10000
            st.plotly_chart(plotstocks(growth_new))
        elif status and sum(input_w)!=1:
            st.write("Please reset your weights: there is an error!")

        if status2:
            # plot growth of portfolio
            st.plotly_chart(plotstocks(growth))
            # display performance
            display_performance(performance)
            # plot pie chat
            plot_pie_chat(weights, checked)

        if status3 and sum(input_w)-1 <=0.1:
            data_compute = data_select.iloc[:,:len(checked)]
            folio_new = input_portforlio(data_compute,input_w)
            data_select['your portfolio'] = folio_new
            growth_new = (data_select / data_select.iloc[0,:]) * 10000
            st.plotly_chart(plotstocks(growth_new))

    def invest(self):
        st.title("Make your REAL Investment!")
        accountNumber ="HK760001001000000005100"
        # data = retrieval_account_balace(accountNumber)
        data = {'accountnumber': 'HK760001001000000005100', 'depositnumber': '000000001', 'depositamount': 10000.0, 'termperiod': '1month', 'terminterestrate': 0.002, 'maturitydate': '1572190222000', 'maturityinterest': 944.42, 'maturityamount': 10944.42, 'maturitystatus': 'D', 'currencycode': 'HKD', 'createdate': '1582289470800', 'systemdate': '1569598222000'}
        # dict ={"Account Number":accountNumber,
        #        "Deposit Amount": data['depositamount']}
        # table = pd.DataFrame.from_dict(dict,orient='index',columns=["Information"])
        # st.write("### Your Account Information")
        # st.table(table)

        st.write("### How much you would like to invest")
        amount = st.text_input("Amount for investing:",1000)

        st.write("### Tell us more about your portfolio")
        snp = pd.read_csv('snp10.csv',index_col=0)
        # mutiple selection bar
        checked = display_multiple_selection_bar(snp)
        # fetch relative data
        data = snp[checked]

        option = st.selectbox("Amount indication",["Base on weights", "Base on amount"])

        if option == "Base on weights":

            st.write("### Tell us the weights of your portfolio!")
            input_w = []
            for i in range(len(checked)):
                w = st.text_input(checked[i],round(1/len(checked),2))
                input_w.append(float(w))

            confirm = st.button("See risk & return evaluation")
            if confirm:
                st.write("See historical performance")
                data= data.iloc[:,:len(checked)]
                folio_new = input_portforlio(data,input_w)
                data['your portfolio'] = folio_new
                growth_new = (data / data.iloc[0,:]) * 1000
                st.plotly_chart(plotstocks(growth_new))

        elif option == "Base on amount":
            st.write("### Tell us the amount of each stock in your portfolio!")
            amounts = []
            for i in range(len(checked)):
                w = st.text_input(checked[i], 0)
                amounts.append(float(w))

            confirm = st.button("See risk & return evaluation")
            if confirm and sum(amounts)!=0:
                st.write("See historical performance")
                input_w = data.iloc[-1,:len(checked)]*amounts/sum(data.iloc[-1,:len(checked)]*amounts)
                data= data.iloc[:,:len(checked)]
                folio_new = input_portforlio(data,input_w)
                data['your portfolio'] = folio_new
                growth_new = (data / data.iloc[0,:]) * 1000
                st.plotly_chart(plotstocks(growth_new))


        invest = st.button("confirm the order")
        if invest:
            if int(amount) > self.user.fetch_info('deposit'):
                st.write("The order fails. Not enough money in your deposit!")
            elif int(amount) <= 0:
                st.write("Invalid investing number!")
            else:
                st.write("The order is sent successfully.")
                self.user.edit_info('stock', self.user.fetch_info('stock')+int(amount))
                self.user.edit_info('deposit', self.user.fetch_info('deposit')-int(amount))


if __name__ == "__main__":
    # command for running: streamlit run [filename].py
    Demo = Functionality()
