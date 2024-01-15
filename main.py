# import subprocess
# import sys

import streamlit as st

from gbs.core.gbs import Gbs

# header image
img = "./assets/img.png"
st.image(img)


# title
st.title("Global Biodiversity Score")
st.write(
    """
GBS enables companies and financial institutions to measure their impact on biodiversity and integrate this information into their operational management policy and decision-making strategy. 
In this way, they can align themselves with international objectives and constantly evolving regulations..
"""
)
