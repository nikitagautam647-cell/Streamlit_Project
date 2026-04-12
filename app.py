import streamlit as st
import pandas as pd

df = pd.read_excel("nassau_data.xlsx")

st.write(df.columns.tolist())
st.stop()