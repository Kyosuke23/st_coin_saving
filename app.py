import streamlit as st
import logic

# 描画開始
st.title('500円玉貯金')
st.write(logic.TODAY)
logic.define_global_var()
logic.show_input_area()
logic.show_log_table()