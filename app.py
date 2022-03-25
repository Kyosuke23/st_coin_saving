import streamlit as st
import requests
import datetime
import json
import ast

TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
URL_INDEX = 'https://qjljun.deta.dev/'
URL_GET_ALL_DATA = 'https://qjljun.deta.dev/datas'
URL_GET_DATA_BY_DATE = 'https://qjljun.deta.dev/datas/' + TODAY

# 今日付のデータを取得
response = requests.get(URL_GET_DATA_BY_DATE)

# 取得したデータを変換(=> dict)
today_data = ast.literal_eval(json.loads(response.text))

# 画面項目の描画
st.title('500円玉貯金アプリ')
st.write((f'日付: {today_data["SAVING_DATE"]}'))
st.write((f'今日の貯金枚数: {today_data["AMOUNT"]}枚'))
st.write((f'今までの貯金額: ¥{today_data["TOTAL_AMOUNT"] * 500:,}'))