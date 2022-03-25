import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import ast
import pandas as pd
import numpy as np

# 今日の日付
TODAY = datetime.today()

# WebAPI(Index)
URL_INDEX = 'https://qjljun.deta.dev/'

# WebAPI(全件取得)
URL_GET_ALL_DATA = URL_INDEX + 'data/'

# WebAPI(日付による絞り込み検索)
URL_GET_DATA_BY_DATE = URL_GET_ALL_DATA + TODAY.strftime('%Y-%m-%d')

# サイドバーで選択されたページを取得
page = st.sidebar.selectbox('Choose your page', ['main', 'log'])

# メイン画面
if page == 'main1':
    # 今日付のデータを取得
    response = requests.get(URL_GET_DATA_BY_DATE)
    # 取得したデータを変換(=> dict)
    today_data = ast.literal_eval(json.loads(response.text))

    # 画面項目の描画
    st.title('500円玉貯金アプリ')
    st.write((f'日付: {today_data["SAVING_DATE"]}'))
    st.write((f'今日の貯金枚数: {today_data["AMOUNT"]}枚'))
    st.write((f'今までの貯金額: ¥{today_data["TOTAL_AMOUNT"] * 500:,}'))

elif page == 'main':
    # 1年前の日付
    DATE_PASR_1Y = TODAY + timedelta(days=-365)

    # 範囲検索のURI生成
    URL_GET_DATA_BETWEEN_DATE = URL_GET_ALL_DATA + DATE_PASR_1Y.strftime('%Y-%m-%d') + '/' + TODAY.strftime('%Y-%m-%d')
    
    # 過去1年のデータを取得
    response = requests.get(URL_GET_DATA_BETWEEN_DATE)

    # 取得したデータを変換(=> dict)
    log_date = ast.literal_eval(json.loads(response.text))

    # 画面項目の描画
    st.title('500円玉貯金ログ')

    # # データフレームの描画
    df = pd.DataFrame(log_date) # データフレーム化
    df = df.sort_values('SAVING_DATE', ascending=False) # 降順にソート
    df['TOTAL_PRICE'] = df['TOTAL_AMOUNT'] * 500 # 累計金額列を追加
    df = df[['SAVING_DATE', 'AMOUNT', 'TOTAL_AMOUNT', 'TOTAL_PRICE', 'UPDATED_AT']] # 表示列を定義
    st.dataframe(df, 800, 800)