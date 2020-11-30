import pandas as pd
import numpy as np
import streamlit as st
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import plotly.graph_objects as go

def display_multiple_selection_bar(snp):
    symbols = snp.columns.values
    # check_boxes = [st.sidebar.checkbox(symbol, key=symbol) for symbol in symbols]
    # checked = [symbol for symbol, checked in zip(symbols, check_boxes) if checked]
    st.write("""### Select stocks """)
    checked = st.multiselect('stocks', list(symbols), default = ['AAPL'])
    if len(checked) == 0:
        st.write(" ## ERROR: Select some stocks")
    return checked

def optimize(data):
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)
    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    weights = np.array(list(cleaned_weights.values()))
    folio = (data.iloc[:,:] * weights).sum(axis = 1)
    perf = ef.portfolio_performance(verbose = True)
    perf = np.round(perf, 2)
    return weights, folio, perf

def plotstocks(df):
    # Plot the stocks in the dataframe df
    figure = go.Figure()
    alpha = 0.3
    lw = 1
    for stock in df.columns.values:
        if stock == 'portfolio':
            alpha = 1
            lw = 3
        else:
            alpha = 0.3
            lw = 1
        figure.add_trace(go.Scatter(
            x = df.index.values, y = df[stock],
            name = stock, mode = 'lines',
            opacity = alpha, line = {'width': lw}
        ))
    figure.update_layout(height=  600, width = 800,
                         xaxis_title = 'Date',
                         yaxis_title = 'Relative growth %',
                         title = 'Relative Growth and Performance')
    figure.update_layout(xaxis = dict(rangeslider = dict(visible = True)))
    return figure

def display_performance(performance):
    st.write("## Performance according to Markowitz Model")
    st.write("### Anualized Return: ***{}%***".format(np.round(performance[0] * 100, 2)))
    st.button('Hint: What is Anualized Return?')
    st.write("### Anualized Volatility: ***{}%***".format(np.round(performance[1] * 100, 2)))
    st.button('Hint: What is Anualized Volatility?')
    st.write("### Sharpe Ratio: ***{}***".format(np.round(performance[2], 2)))
    a = st.button('Hint: What is Sharpe Ratio?')
    if a:
        st.write("Sharpe ratio is a measure of excess portfolio return over the risk-free rate relative to its standard deviation. Normally, the 90-day Treasury bill rate is taken as the proxy for risk-free rate. ")
        st.write("Sharpe ratio is the measure of risk-adjusted return of a financial portfolio. A portfolio with a higher Sharpe ratio is considered superior relative to its peers. ")

def plot_pie_chat(weights, checked):
    w = np.array(weights)
    s = np.array(checked)

    pie = go.Figure(data = [go.Pie(labels = s[w > 0], values = w[w > 0])])
    pie.update_layout(
        title = "Resource allocation"
    )
    st.plotly_chart(pie)
  
def display_slider():
    period = st.slider('rolling period', min_value = 1, max_value = 100, value = 5, step = 1)
    return period

def display_volatility_chat(data, dates, period):
    folio_daily_returns = data.pct_change().iloc[:,-1]
    rolling_volatility = data.pct_change().rolling(period).std().iloc[:,-1]
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x = dates, y = folio_daily_returns,
                              opacity = 0.6, line = {'color':'Navy','width': 1}))
    fig3.add_trace(go.Scatter(x = dates, y = rolling_volatility))
    st.write("""## Check daily return & corresponding volatility""".format(period))
    fig3.update_layout(xaxis_title = 'Date', yaxis_title = 'Returns', height = 600, width = 800)
    st.plotly_chart(fig3)
  
def display_link():
    link = '[More detailed course](https://dybfin.wustl.edu/teaching/inv/slides/invl3.html)'
    st.markdown(link, unsafe_allow_html=True)

def main_func_for_stock_portfolio():
    st.title("Check Historical Performance of any stock or portfolio")
    # input dataset
    snp = pd.read_csv('snp10.csv',index_col=0)
    # mutiple selection bar
    checked = display_multiple_selection_bar(snp)
    # fetch relative data
    data = snp[checked]
    dates = data.index.values
    # calculate portfolio parameters
    weights, folio, performance = optimize(data)
    data['portfolio'] = folio
    growth = (data / data.iloc[0,:] - 1) * 100
    # plot growth of portfolio
    st.plotly_chart(plotstocks(growth))
    # display performance
    display_performance(performance)
    # plot pie chat
    # plot_pie_chat(weights, checked)
    # display silder
    # period = display_slider()
    period = 5
    # dispaly volatility chat
    display_volatility_chat(data, dates, period)
    # show more resource
    display_link()

if __name__ == "__main__":
    # command for running: streamlit run [filename].py
    main_func_for_stock_portfolio()