import streamlit as st
import pandas as pd

df = pd.read_excel("Nassau Candy Distributor main sheet.xlsx")

st.write(df.columns)
st.stop()