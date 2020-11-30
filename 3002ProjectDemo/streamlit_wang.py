import streamlit as st # pip install streamlit
import pandas as pd
from utils_wang import *
from user import User

class Transfer(object):
    def __init__(self):
        self.user = User()
        # st.sidebar.markdown("# Service We Provide")
        # self.option = st.sidebar.selectbox("",["Education", "Account Opening", "Investment", "Transfer", "Payee Info"])

        # if self.option == "Account Opening":
        #     self.open_account()
        # elif self.option == "Payee Info":
        #     self.payee_info()
        # elif self.option == 'Transfer':
        #     self.transfering()

    def account_opening_success(self):
        st.write("## Successful in opening your account!")
    
    def open_account(self):
        st.write("## Please fill in all the infomation to open your account!")
        st.text_input("Enter your first name:")
        st.text_input("Enter your last name:")
        st.selectbox("Choose your gender:", ['-'*2, 'Male', 'Female'])
        st.text_input("Enter your HK Identity Card Number:")
        st.text_input("Enter your residence address:")
        st.text_input("Enter your phone number:")
        st.text_input("Enter your email address")
        st.text_input("Enter your residence phone number")
        st.selectbox("Choose your currency", ['-'*2, 'HKD', 'CNY'])
        if st.button("Open Account!"):
            self.account_opening_success()
    
    def payee_info(self):
        payeeCategoryList = retrieval_payee_category_list()
        try:
            if payeeCategoryList['code'] == '200':
                payeeCategoryList = payeeCategoryList['data']    
                payeeList = {}
                payeeCategoryIdList = []
                payeeNameList = []
                selectedCategoryId = '000'
                for item in payeeCategoryList:
                    payeeCategoryIdList.append(item['payeecategoryid'])
                selectedCategoryId = st.selectbox('Select a payee category ID', ['--'] + payeeCategoryIdList)
                if selectedCategoryId != '000':
                    payeeInfoList = retrieve_payee_info_list(selectedCategoryId)
                    if payeeInfoList['code'] == '200':
                        df = pd.json_normalize(payeeInfoList['data'])
                        st.write(df)
                        df_t = df.transpose()
                        for i in range(len(df_t.columns)):
                            payeeList[df_t[i]['payeename']] = i
                            payeeNameList.append(df_t[i]['payeename'])
                        payee = '0'
                        payee = st.selectbox('Select the payee to make a payment', ['--'] + payeeNameList)
                        if payee != '--':
                            self.makePayment(df, payee, payeeList)
        except:
            pass
        '''
        payeeNameList = ['-'*5] + [item['payeename'] for item in payeeInfoList]
        payeeName = st.selectbox("Your potential payee", payeeNameList)
        
        if payeeName != payeeNameList[0]:
            for payee in payeeInfoList:
                if payeeName == payee['payeename']:
                    details_df = pd.json_normalize(payee)
                    break
            st.dataframe(details_df.transpose()[0])
        '''

    def makePayment(self, df, payeeName, payeeList):
        transactionCurrency = '000'
        paymentAmount = -1
        remarks = None
        st.write('## You are making a payment to ' + payeeName)
        transactionCurrency = st.selectbox('Select the payment currency', ['HKD', 'CNY'])
        # paymentEffectiveDay = st.text_input('Input the payment effective day', '1607854449000')
        paymentEffectiveDay = 1607854449000
        payeeNumber = 202002272222
        customerAccountType = 'CRED'
        customerAccountNumber = 5000010000721728
        payeeId = 'G123456'
        paymentAmount = st.text_input("Input your payment amount")
        remarks = st.text_input('Input your remarks')     
        if transactionCurrency != '000' and paymentAmount != -1 and remarks != None:                
            if st.button('Confirm!'):
                self.user.edit_info('deposit', self.user.fetch_info('deposit')-int(paymentAmount))
                p = PaymentModel(transactionCurrency, paymentEffectiveDay, payeeNumber, customerAccountType, customerAccountNumber, payeeId, paymentAmount, remarks)
                r = bill_payment_transaction_Payment_Service(p)
                if r['code'] == '200':
                    st.write('## ' + r['msg'])
                else:
                    st.write('## Payment fails, please retry')

    def transfering(self):
        outAccount = '0'
        inAccount = '0'
        amount = -1
        st.title("Quick Transfer and Payment")
        st.write('## Please Fill In Transfer Details')
        outAccount = st.text_input('Transfer from', self.user.fetch_info('account_number'))
        inAccount = st.text_input('Transfer to')
        # st.write("## Search for your Payee")
        self.payee_info()
        # amount = st.text_input('Transfer amount')
        # if st.button('Confirm'):
        #     if outAccount != '0' and inAccount != '0' and amount != -1:
        #         amount = int(amount)
        #         r = transfer(inAccount, amount, outAccount)
        #         if r['code'] == '200':
        #             st.write('## Success')
        #         else:
        #             st.write('## Transfer fails, please try again')


if __name__ == "__main__":
    # command for running: streamlit run [filename].py
    Demo = Functionality()
