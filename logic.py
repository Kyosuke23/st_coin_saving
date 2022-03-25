import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import ast
import pandas as pd

# 今日の日付
TODAY = datetime.today()

# WebAPI(Index)
URL_INDEX = 'https://qjljun.deta.dev/' # サーバ
# URL_INDEX = 'http://127.0.0.1:8000/'   # ローカルサーバ

# WebAPI(全件取得)
URL_GET_ALL_DATA = URL_INDEX + 'data/'

# WebAPI(日付による絞り込み検索)
URL_GET_DATA_BY_DATE = URL_GET_ALL_DATA + TODAY.strftime('%Y-%m-%d')

def show_input_area():
    """
    入力フォーム周りの描画
    """
    # 今日付のデータを取得
    res = requests.get(URL_GET_DATA_BY_DATE)

    # 取得したデータを変換(=> dict)
    today_data = ast.literal_eval(json.loads(res.text))

    # 各項目を取得
    saving_date = today_data["SAVING_DATE"] # 日付
    amount = today_data["AMOUNT"] # 今日の貯金枚数
    total_price = today_data["TOTAL_AMOUNT"] * 500 # 今までの貯金額

    # タイトルを描画
    st.write('## 貯金額変更')

    # フォームの定義
    with st.form(key='main'):
        input_amount: int = st.number_input('枚数', step=1)
        req = {
            'amount': input_amount,
            'target_date': TODAY.strftime('%Y-%m-%d'),
        }
        submit_button = st.form_submit_button(label='submit')

    # ボタン押下時の挙動
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

    # ページ下部の情報を描画
    st.write((f'日付: {saving_date}'))
    st.write((f'今日の貯金枚数: {amount}枚'))
    st.write((f'今までの貯金額: ¥{total_price:,}'))
        
# ログ画面
def show_log_table():
    """
    ログテーブルの描画
    """
    # 1年前の日付
    DATE_PASR_1Y = TODAY + timedelta(days=-365)

    # 範囲検索のURI生成
    URL_GET_DATA_BETWEEN_DATE = URL_GET_ALL_DATA + DATE_PASR_1Y.strftime('%Y-%m-%d') + '/' + TODAY.strftime('%Y-%m-%d')
    
    # 過去1年のデータを取得
    res = requests.get(URL_GET_DATA_BETWEEN_DATE)

    # 取得したデータを変換(=> dict)
    log_date = ast.literal_eval(json.loads(res.text))

    # タイトルを描画
    st.write('## 貯金履歴')

    # データフレームの生成
    df = pd.DataFrame(log_date) # データフレーム化
    df['TOTAL_PRICE'] = df['TOTAL_AMOUNT'] * 500 # 累計金額列を追加
    df = df[['SAVING_DATE', 'AMOUNT', 'TOTAL_AMOUNT', 'TOTAL_PRICE', 'UPDATED_AT']] # 表示列を定義

    # 表示用に値を整形
    for i, data in df.iterrows():
        df.loc[i, 'TOTAL_PRICE'] = '¥' + '{:,}'.format(data['TOTAL_PRICE']) # 累計金額
        df.loc[i, 'UPDATED_AT'] = data['UPDATED_AT']['$date'] # 更新日時

    # ヘッダー名称を変更
    df = df.rename(
        columns={
            "SAVING_DATE": "日付",
            "AMOUNT": "枚数",
            "TOTAL_AMOUNT": "累計枚数",
            "TOTAL_PRICE": "累計金額",
            "UPDATED_AT": "更新日時",
        }
    )
    
    # データフレームを描画
    st.dataframe(df, 800, 400)
