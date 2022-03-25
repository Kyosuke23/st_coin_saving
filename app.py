from turtle import update
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
# URL_INDEX = 'https://qjljun.deta.dev/' # サーバ
URL_INDEX = 'http://127.0.0.1:8000/'   # ローカルサーバ

# WebAPI(全件取得)
URL_GET_ALL_DATA = URL_INDEX + 'data/'

# WebAPI(日付による絞り込み検索)
URL_GET_DATA_BY_DATE = URL_GET_ALL_DATA + TODAY.strftime('%Y-%m-%d')

# サイドバーで選択されたページを取得
page = st.sidebar.selectbox('Choose your page', ['main', 'log'])

# メイン画面
if page == 'main':
    # 今日付のデータを取得
    res = requests.get(URL_GET_DATA_BY_DATE)
    # 取得したデータを変換(=> dict)
    today_data = ast.literal_eval(json.loads(res.text))
    # 日付
    saving_date = today_data["SAVING_DATE"]
    # 今日の貯金枚数
    amount = today_data["AMOUNT"]
    # 今までの貯金額
    total_price = today_data["TOTAL_AMOUNT"] * 500

    st.title('500円玉貯金アプリ')
    with st.form(key='main'):
        amount: int = st.number_input('枚数', step=1)
        req = {
            'amount': amount,
            'target_date': TODAY.strftime('%Y-%m-%d'),
        }
        submit_button = st.form_submit_button(label='submit')

    if submit_button:
        # WebAPI(更新)のURLを生成
        URL_UPDATE = URL_INDEX + 'update/' + req['target_date'] + '/' + str(req['amount'])
        res = requests.post(URL_UPDATE, data= json.dumps(req))
        print('--- 送信データ ------------------------------')
        print(req)
        print('--- 受信データ ------------------------------')
        print(res.json())
        
        # 更新後のデータ
        updated_data = ast.literal_eval(json.loads(res.text))['updated_data']

        # 更新後の値で描画
        saving_date = updated_data["SAVING_DATE"]
        amount = updated_data["AMOUNT"]
        total_price = updated_data["TOTAL_AMOUNT"] * 500

    st.write((f'日付: {saving_date}'))
    st.write((f'今日の貯金枚数: {amount}枚'))
    st.write((f'今までの貯金額: ¥{total_price:,}'))
        
# ログ画面
elif page == 'log':
    # 1年前の日付
    DATE_PASR_1Y = TODAY + timedelta(days=-365)

    # 範囲検索のURI生成
    URL_GET_DATA_BETWEEN_DATE = URL_GET_ALL_DATA + DATE_PASR_1Y.strftime('%Y-%m-%d') + '/' + TODAY.strftime('%Y-%m-%d')
    
    # 過去1年のデータを取得
    res = requests.get(URL_GET_DATA_BETWEEN_DATE)

    # 取得したデータを変換(=> dict)
    log_date = ast.literal_eval(json.loads(res.text))

    # 画面項目の描画
    st.title('500円玉貯金ログ')

    # # データフレームの描画
    df = pd.DataFrame(log_date) # データフレーム化
    df = df.sort_values('SAVING_DATE', ascending=False) # 降順にソート
    df['TOTAL_PRICE'] = df['TOTAL_AMOUNT'] * 500 # 累計金額列を追加
    df = df[['SAVING_DATE', 'AMOUNT', 'TOTAL_AMOUNT', 'TOTAL_PRICE', 'UPDATED_AT']] # 表示列を定義
    st.dataframe(df, 800, 800)