import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np;
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
#     st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

#     data=pdataframe;
    groupby_symbol = dataframe.groupby('symbol')
    INDEX = 0
    ALL_DICT = {}
    for symbol in groupby_symbol.groups:
        ALL_DICT[INDEX] = {}
        ALL_DICT[INDEX]['SYMBOL'] = symbol
        symbol_df = groupby_symbol.get_group(symbol)
        groupby_symbol_transct = symbol_df.groupby('trade_type')
        symbol_buy_df = groupby_symbol_transct.get_group('buy')
        symbol_sell_df = groupby_symbol_transct.get_group('sell')

        buy_quantity = symbol_buy_df['quantity'].sum()
        buy_sum = (symbol_buy_df['price'] * symbol_buy_df['quantity']).sum()
        print("buy sum",buy_sum);
        print("buy quantity",buy_quantity);
        buy_avg = np.round(buy_sum/buy_quantity,0)
        ALL_DICT[INDEX]['BUY_QUANTITY'] = buy_quantity
        ALL_DICT[INDEX]['BUY_AVG'] = buy_avg

        sell_quantity = symbol_sell_df['quantity'].sum()
        sell_sum = (symbol_sell_df['price'] * symbol_sell_df['quantity']).sum()
        sell_avg = np.round(sell_sum/sell_quantity,0)
        ALL_DICT[INDEX]['SELL_QUANTITY'] = sell_quantity
        ALL_DICT[INDEX]['SELL_AVG'] = sell_avg
        INDEX+=1

    df = pd.DataFrame.from_dict(ALL_DICT,orient='index')
