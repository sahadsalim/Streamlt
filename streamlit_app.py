import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

data = pd.read_csv("csv_practice.csv") #path folder of the data file
st.write(data) #displays the table of data
