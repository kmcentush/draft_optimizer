import streamlit as st

from draft_optimizer.app._pages import draft, settings

# Set page layout
st.set_page_config(page_title="Draft Optimizer", layout="wide")

# Specify pages
page = st.sidebar.radio("Page", ["Draft", "Settings"], index=1)

if page == "Draft":
    draft.display()
elif page == "Settings":
    settings.display()
