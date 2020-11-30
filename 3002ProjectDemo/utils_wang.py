# The program is designed to provide funtionalities such as account opening, deposit
# checking and payment on stock and fund purchasing.

import json
import requests


BASIC_URL ='https://datastudio.simnectzplatform.com/gateway/SIMNECTZ/'
TOKEN = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNo8y00OwiAQhuG7zNoFkBLUpbqwadI7ADNWEn4aWozGeHchNs7yme99A9KDfJop9xc4gkTaG6XtTQrRCWEPhMKojhnDLVdKwg5sKnHNr3NCqsF1aORJZxenzRhjvKrJOtr73xr5NLk46tBkdqGlZVlToDyWYCj_hmy7Viw64ik9e6wv-HwBAAD__w.alc0ibAbJotnPxSQL2wtt9Qo8h0YYzl4WkxOK65PnGy1fK4SDmNRRVEohqOya_K7qOXJOt5Cjdm10cejK3PViA'
AUTHORIZATION = '5e46871f34a6e5748c2c4171319dbe6d3dec43c295c5949f056e3319'

HEADERS = {
    'Token': TOKEN,
    'Authorization': AUTHORIZATION,
    'Content-type': 'application/json'
}


class AddAcountModel:
    def __init__(self, relaccountnumber, accountType, customerNumber, currencyCode):
        self.relaccountnumber = relaccountnumber
        self.accountType = accountType
        self.customerNumber = customerNumber
        self.currencyCode = currencyCode


class CustomerMaintenanceModel:
    def __init__(self, mobilePhoneNumber, mailingAddress, customerID, residencephonenumber, emailaddress, residentialaddress):
        self.mobilePhoneNumber = mobilePhoneNumber
        self.mailingAddress = mailingAddress
        self.customerID = customerID
        self.residencephonenumber = residencephonenumber
        self.emailaddress = emailaddress
        self.residentialaddress = residentialaddress


class DepositModel:
    def __init__(self, depositAmount, accountNumber, currencycode):
        self.depositAmount = depositAmount
        self.accountNumber = accountNumber
        self.currencyCode = currencycode


class WithDrawalModel:
    def __init__(self, accountNumber, currencycode, depositAmount):
        self.depositAmount = depositAmount
        self.accountNumber = accountNumber
        self.currencyCode = currencycode


class QueryPayeeInfoModel:
    def __init__(self, payeeCategoryId):
        self.payeeCategoryId = payeeCategoryId


class SetBillPayeeModel:
    def __init__(self, payeeCategoryID, payeeNumber, payeeID):
        self.payeeCategoryID = payeeCategoryID
        self.payeeNumber = payeeNumber
        self.payeeID = payeeID


class DeleteBillPayeeModel:
    def __init__(self, payeeCategoryID, payeeNumber, payeeID):
        self.payeeCategoryID = payeeCategoryID
        self.payeeNumber = payeeNumber
        self.payeeID = payeeID


class PaymentModel:
    def __init__(self, transactionCurrency, paymentEffectiveDay, payeeNumber, customerAccountType, customerAccountNumber, payeeId, paymentAmount, remarks):
        self.transactionCurrency = transactionCurrency
        self.paymentEffectiveDay = paymentEffectiveDay
        self.payeeNumber = payeeNumber
        self.customerAccountType = customerAccountType
        self.customerAccountNumber = customerAccountNumber
        self.payeeId = payeeId
        self.paymentAmount = paymentAmount
        self.remarks = remarks


def account_opening(addAccountModel):
    call_url = BASIC_URL + 'account_opening_presentation//deposit/account/accountCreation'
    response = requests.post(url = call_url, data = json.dumps(addAccountModel.__dict__), headers = HEADERS)
    return response.json()


def deposit(depositModel):
    call_url = BASIC_URL + 'deposit_presentation//deposit/account/deposit'
    response = requests.post(url = call_url, data = json.dumps(depositModel.__dict__), headers = HEADERS)
    return response.json()


def withdrawal(withDrawalModel):
    call_url = BASIC_URL + 'withdrawal_presentation//deposit/account/withdrawal'
    input_data = {
        'depositModel': json.dumps(withDrawalModel.__dict__)
    }
    response = requests.post(url = call_url, data = json.dumps(input_data), headers = HEADERS)
    return response.json()


def transfer(transferInAccountNumber, transferAmount, transferOutAccountNumber):
    call_url = BASIC_URL + 'transfer_presentation//deposit/account/transfer'
    input_data = {
        'transferInAccountNumber': transferInAccountNumber,
        'transferAmount': transferAmount,
        'transferOutAccountNumber': transferOutAccountNumber
    }
    response = requests.post(url = call_url, data = json.dumps(input_data), headers = HEADERS)
    return response.json()


def customer_contact_info_update_presentation(customerMaintenanceModel):
    call_url = BASIC_URL + 'customer_contact_info_update_presentation//customer/contactInfoUpdate'
    response = requests.post(url = call_url, data = json.dumps(customerMaintenanceModel.__dict__), headers = HEADERS)
    return response.json()


def retrieve_customer_payee_list():
    call_url = BASIC_URL + 'retrieve_customer_payee_list//payment/customerPayeeRetrieval'
    response = requests.get(url = call_url, headers = HEADERS)
    return response.json()


def retrieval_payee_category_list():
    call_url = BASIC_URL + 'retrieve_customer_payee_list//payment/payeeCategoryList'
    response = requests.get(url = call_url, headers = HEADERS)
    return response.json()


def retrieve_payee_info_list(payeeCategoryId):
    call_url = BASIC_URL + 'retrieval_payee_info_list//payment/payeeInfoListRetrieval'
    input_data = {
        'payeeCategoryId': payeeCategoryId
    }
    response = requests.post(url = call_url, data = json.dumps(input_data), headers = HEADERS)
    return response.json()


def set_bill_payee_Payment_Servive(setBillPayeeModel):
     call_url = BASIC_URL + 'set_bill_payee///payment/billPayeeSetup'
     response = requests.post(url = call_url, data = json.dumps(setBillPayeeModel.__dict__), headers = HEADERS)
     return response.json()


def delete_bill_payee_Payment_Service(deleteBillPayeeModel):
    call_url = BASIC_URL + 'delete_bill_payee//payment/billPayeeDelete'
    response = requests.post(url = call_url, data = json.dumps(deleteBillPayeeModel.__dict__), headers = HEADERS)
    return response.json()


def bill_payment_transaction_Payment_Service(paymentModel):
    call_url = BASIC_URL + 'bill_payment_transaction//payment/paymentTransaction'
    response = requests.post(url = call_url, data = json.dumps(paymentModel.__dict__), headers = HEADERS)
    return response.json()


'''
# account opening
token = TOKEN
messageid = '006f7113e5fa48559549c4dfe74e2cd6'
clientid = 'devin'
addAcountModel = AddAcountModel(relaccountnumber = 'HK720001001000000001001', accountType = '001', customerNumber = '001000000001', currencyCode = 'HKD')

response = account_opening(token, messageid, clientid, addAcountModel)
print(response)
'''

'''
# deposit
depositModel = DepositModel(300, 'HK720001001000045591001', 'HKD')
response = deposit(depositModel)
print(response)
'''

'''
# retrieve customer payee list
response = retrieve_customer_payee_list()
print(response)
'''

'''
# retrieval payee category
response = retrieval_payee_category()
print(response)
'''

'''
# retrieve payee info list
payeeCategoryId = '001'
queryPayeeInfoModel = QueryPayeeInfoModel(payeeCategoryId)
response = retrieve_payee_info_list(queryPayeeInfoModel)
print(response)
'''

'''
# build payee list
payeeCategoryID = '001'
paymentNumber = 1
payeeID = 'G123456'
s = SetBillPayeeModel(payeeCategoryID, paymentNumber, payeeID)
response = set_bill_payee_Payment_Servive(s)
print(response)
'''

'''
# delete payee
payeeCategoryID = '001'
paymentNumber = 1
payeeID = 'G123456'
d = DeleteBillPayeeModel(payeeCategoryID, paymentNumber, payeeID)
response = delete_bill_payee_Payment_Service(d)
print(response)
'''

'''
# make a payment
transactionCurrency = 'HKD'
paymentEffectiveDay = 1607854449000
payeeNumber = 202002272222
customerAccountType = 'CRED'
customerAccountNumber = 5000010000721728
payeeId = 'G123456'
paymentAmount = 123
remarks = 'Current-PaymentTransaction'
p = PaymentModel(transactionCurrency, paymentEffectiveDay, payeeNumber, customerAccountType, customerAccountNumber, payeeId, paymentAmount, remarks)
r = bill_payment_transaction_Payment_Service(p)
print(r)
'''
