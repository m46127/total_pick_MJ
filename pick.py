# pick.py
import streamlit as st
import pandas as pd
import numpy as np
import io
import base64

def pick_page():
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(bin_file).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
        return href

    uploaded_file_csv = st.file_uploader("CSVファイルをアップロード", type="csv")
    uploaded_file_excel = st.file_uploader("Excelファイルをアップロード", type="xlsx")

    if uploaded_file_csv is not None and uploaded_file_excel is not None:
        df = pd.read_csv(uploaded_file_csv, encoding='shift_jis')
        df.rename(columns={'同梱ID': 'Product Code', '数量': 'Quantity'}, inplace=True)
        df['Product Code'] = df['Product Code'].astype(str)
        df['Quantity'] = df['Quantity'].astype(int)
        df = df.groupby('Product Code').sum().reset_index()

        inventory_df = pd.read_excel(uploaded_file_excel, usecols='E')
        inventory_df.columns = ['LOTNo.']
        inventory_df['LOTNo.'] = inventory_df['LOTNo.'].astype(str)

        merged_df = pd.merge(inventory_df, df, left_on='LOTNo.', right_on='Product Code', how='left')
        merged_df = merged_df[['LOTNo.', 'Quantity']]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            merged_df.to_excel(writer, sheet_name='Sheet1', index=False)

        binary_excel = output.getvalue()  
        st.markdown(get_binary_file_downloader_html(binary_excel, 'Merged_YourFileNameHere.xlsx'), unsafe_allow_html=True)
