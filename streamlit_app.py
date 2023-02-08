import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np;
st.header('P/L Tracker')
st.markdown('''##### <span style="color:gray">Calculate the P/L percentale from tradebook csv</span>
        ''', unsafe_allow_html=True)
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
    st.write(df)
    
    
    df[df['BUY_QUANTITY'] != df['SELL_QUANTITY']] # Open Positions
    df[df['BUY_QUANTITY'] == df['SELL_QUANTITY']] # Closed Positions
    closed_pos = df[df['BUY_QUANTITY'] == df['SELL_QUANTITY']]
    buy_amt = (df['BUY_QUANTITY']*df['BUY_AVG']).sum()
    sell_amt = (df['SELL_QUANTITY']*df['SELL_AVG']).sum()
    print(((sell_amt - buy_amt)/buy_amt)*100)
    st.title('Todays Profit percentage')
    st.write('profit percentage is ',((sell_amt - buy_amt)/buy_amt)*100)
    
    ##########################################
    ##  Style and Formatting                ##
    ##########################################

    # CSS for tables

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>   """

    center_heading_text = """
        <style>
            .col_heading   {text-align: center !important}
        </style>          """

    center_row_text = """
        <style>
            td  {text-align: center !important}
        </style>      """

    # Inject CSS with Markdown

    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.markdown(center_heading_text, unsafe_allow_html=True) 
    st.markdown(center_row_text, unsafe_allow_html=True) 

    # More Table Styling

    def color_surplusvalue(val):
        if str(val) == '0':
            color = 'azure'
        elif str(val)[0] == '-':
            color = 'lightpink'
        else:
            color = 'lightgreen'
        return 'background-color: %s' % color

    heading_properties = [('font-size', '16px'),('text-align', 'center'),
                          ('color', 'black'),  ('font-weight', 'bold'),
                          ('background', 'mediumturquoise'),('border', '1.2px solid')]

    cell_properties = [('font-size', '16px'),('text-align', 'center')]

    dfstyle = [{"selector": "th", "props": heading_properties},
                   {"selector": "td", "props": cell_properties}]

    # Expander Styling

    st.markdown(
        """
    <style>
    .streamlit-expanderHeader {
     #   font-weight: bold;
        background: aliceblue;
        font-size: 18px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


    styler_player = (df
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle)
                   .applymap(color_surplusvalue))
    st.table(styler_player)
