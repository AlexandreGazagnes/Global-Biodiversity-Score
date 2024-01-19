# import subprocess
# import sys

import streamlit as st


from gbs.front.text import Text
from gbs.etl.load import Load
from gbs.core.gbs import Gbs

# header image
img = "./.assets/img.png"
st.image(img)


# title
st.title(Text.title)
st.write(Text.descr)


# load data
df = Load.final()


st.table(df)
