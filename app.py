import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import ast

# 今日の日付
TODAY = datetime.today()

# WebAPI(Index)
URL_INDEX = 'https://qjljun.deta.dev/'
URL_GET_ALL_DATA = URL_INDEX + 'data/'
URL_GET_DATA_BY_DATE = URL_GET_ALL_DATA + TODAY.strftime('%Y-%m-%d')

# サイドバーで選択されたページを取得
page = st.sidebar.selectbox('Choose your page', ['main', 'log'])

# メイン画面
if page == 'main':
    # 今日付のデータを取得
    response = requests.get(URL_GET_DATA_BY_DATE)
    # 取得したデータを変換(=> dict)
    today_data = ast.literal_eval(json.loads(response.text))

    # 画面項目の描画
    st.title('500円玉貯金アプリ')
    st.write((f'日付: {today_data["SAVING_DATE"]}'))
    st.write((f'今日の貯金枚数: {today_data["AMOUNT"]}枚'))
    st.write((f'今までの貯金額: ¥{today_data["TOTAL_AMOUNT"] * 500:,}'))

elif page == 'log':
    # 全データを取得
    response = requests.get(URL_GET_ALL_DATA)