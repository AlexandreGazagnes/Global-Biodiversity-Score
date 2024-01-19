# import subprocess
# import sys

import streamlit as st
from gbs.front.text import Text


# from gbs.etl.extract import Extract
from gbs.core.gbs import Gbs
from gbs.etl.loader import Loader

# df
df = Loader.final()

# header image
img = "./.assets/img.png"
st.image(img)


# title
st.title(Text.title)
st.write(Text.descr)


# data
st.subheader("Data")
st.table(df)

# country
st.subheader("Country")

country_name = st.selectbox(
    "Select a country",
    df["country_name"].unique()
    # , help="Select a country"
)
if country_name:
    st.table(df[df["country_name"] == country_name])
