import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np;
st.set_page_config(layout="wide")


# Sidebar setup
st.sidebar.title('Sidebar')
with st.sidebar:
    upload_file = st.sidebar.file_uploader('Upload a file containing earthquake data')

    # Check if file has been uploaded
    if upload_file is not None:
        df = pd.read_csv(upload_file)
        st.session_state['df'] = df;
    for key in st.session_state.keys():
        if key=='df':
            df=st.session_state['df'];
            lf=df.head();
            st.write(lf);
def main_page():
    st.header('P/L Tracker')
    st.markdown('''##### <span style="color:gray">Calculate the P/L percentale from tradebook csv</span>
            ''', unsafe_allow_html=True);
    # tab_pl, tab_graph = st.tabs(["Pl find", "Graph plot"])
    tab1, tab2, tab3 = st.tabs(["Pl find", "Graph", "Owl"])
    with tab1:
            dataframe = pd.read_csv("data/tradebook-QVP700-FO.csv")
            st.write("Please choose the tradebook csv file")
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None or !dataframe.empty:
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
    with tab2 :
            st.header("Graphs")
def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")
    import streamlit as st
    # import pandas as pd
    # st.write("homeee")
    df=st.session_state['df']
    st.write(df)
page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    # "Page 3": page3,
}
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
# Contents of ~/my_app/pages/page_2.py
# import streamlit as st

# st.markdown("# Page 2 ❄️")
# st.sidebar.markdown("# Page 2 ❄️")