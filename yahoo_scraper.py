import datetime
import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
st.title("Yahoo Finance Date Scraper﻿")

d = st.date_input(
    "Enter Date Here")


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')   

def scrape_yahoo_finance(date):
   
    print("Starting scrape")
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'
            }
    # Build URL for Yahoo Finance page for the given date
    url = f'https://finance.yahoo.com/calendar/earnings?day={date}'
    # Send request to Yahoo Finance page
    r = requests.get(url, headers=headers, timeout=5)
    print('request completed')
    # Parse HTML content using Beautiful Soup
    soup = BeautifulSoup(r.content, 'html.parser')
    print('soup created')
    # Find table containing earnings data
    table = soup.find('table', {'class': 'W(100%)'})
    # Extract table data and store in Pandas dataframe
    data = []
    df = None
    if table != None: 
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            stock_symbol = cells[0].text
            eps = cells[4].text
            surprise = cells[6].text
            if eps != '-' or surprise != '-':  
                data.append([stock_symbol, eps, surprise])
        df = pd.DataFrame(data, columns=['Stock Symbol', 'EPS', 'Surprise'])    
        df = df.drop_duplicates(subset=['Stock Symbol'])
    return df

if st.button('Scrape'):
    date_file = d.strftime('%Y_%m_%d')
    df = scrape_yahoo_finance(d)
    if df is not None:
        csv = convert_df(df)
        st.download_button(
        "Press to Download",
        csv,
        "yahoo_earnings" + date_file + ".csv",
        "text/csv",
        key='download-csv'
        )
        st.table(df)
    else:
        st.write('There is no data for this date')


       

