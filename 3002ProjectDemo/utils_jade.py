import json
import requests
import pandas as pd
import numpy as np

BASIC_URL = 'https://datastudio.simnectzplatform.com/gateway/SIMNECTZ/'
TOKEN = 'eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNo8y00OwiAQhuG7zNoFkBLUpbqwadI7ADNWEn4aWozGeHchNs7yme99A9KDfJop9xc4gkTaG6XtTQrRCWEPhMKojhnDLVdKwg5sKnHNr3NCqsF1aORJZxenzRhjvKrJOtr73xr5NLk46tBkdqGlZVlToDyWYCj_hmy7Viw64ik9e6wv-HwBAAD__w.alc0ibAbJotnPxSQL2wtt9Qo8h0YYzl4WkxOK65PnGy1fK4SDmNRRVEohqOya_K7qOXJOt5Cjdm10cejK3PViA'
AUTHORIZATION = '5e46871f34a6e5748c2c4171319dbe6d3dec43c295c5949f056e3319'

HEADERS1 = {
    'token': TOKEN,
    'Authorization': AUTHORIZATION,
    'Content-Type': 'application/json'
}
HEADERS2 = {
    'token': TOKEN,
    'Authorization': AUTHORIZATION,
    'Content-Type': 'application/json'
}

def retrieval_payee_info_list(payeeCategoryId):
    call_url = BASIC_URL + 'retrieval_payee_info_list//payment/payeeInfoListRetrieval'
    input_dict = {
        'payeeCategoryId': payeeCategoryId
    }
    response = requests.post(url = call_url, data = json.dumps(input_dict), headers = HEADERS1)
    return response.json()['data']

def load_historical_price(select):
    df = pd.read_csv("stock_price.csv")
    data = df[np.intersect1d(df.columns, select)]
    return data

def input_portforlio(data,weights_new):
    weights_new = np.array(weights_new)
    folio_new = (data.iloc[:,:] * weights_new).sum(axis = 1)
    return folio_new

def retrieval_account_balace(accountNumber):
    call_url = BASIC_URL + 'term_deposit_enquiry_presentation//termDeposit/enquiry'
    input_dict = {
        "accountnumber": accountNumber,
        "tdnumber": "000000001"
    }
    response = requests.post(url = call_url, data = json.dumps(input_dict), headers = HEADERS2)
    return response.json()['data']
