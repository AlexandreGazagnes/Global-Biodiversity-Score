# import subprocess
# import sys

import streamlit as st


from gbs.front.text import Text
from gbs.etl.load import Loader
from gbs.core.gbs import Gbs

# header image
img = "./.assets/img.png"
st.image(img)


# title
st.title(Text.title)
st.write(Text.descr)


# load data
df = Loader.final()

st.subheader("Data")
st.table(df)


# gbs
st.subheader("GBS")
country = st.selectbox("country_name", df["country_name"].unique())
if country:
    tmp = df.loc[df["country_name"] == country]
    st.table(tmp.T)
