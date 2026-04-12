import streamlit as st
import pandas as pd

df = pd.read_excel("file.xlsx")

st.write(df.columns)
st.stop()