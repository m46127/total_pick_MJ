# main.py
import streamlit as st
from streamlit_option_menu import option_menu

# メニューの選択肢を定義
menu_options = ["トップページ", "pick", "pdf_pick"]

# サイドバーでオプションメニューを表示
selected_option = option_menu("メインメニュー", menu_options, icons=['house', 'upload', 'file-pdf'], menu_icon="cast", default_index=0)

# 選択肢に応じて表示するページを変更
if selected_option == "トップページ":
    st.title("トップページ")
    st.write("ようこそ！")

elif selected_option == "pick":
    # pick.py の内容をインポートして実行
    from pick import pick_page
    pick_page()

elif selected_option == "pdf_pick":
    # pdf_pick.py の内容をインポートして実行
    from pdf_pick import pdf_pick_page
    pdf_pick_page()

