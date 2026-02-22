import streamlit as st
import numpy as np
import warnings
import psycopg2
import platform
from PIL import Image
from utils import image2tensor, pred2label
import requests
import json

st.set_page_config(page_title="Bambou le fraudeur à la carte bancaire", page_icon=":guardsman:", layout="wide")

# Add a header
st.header("Bambou le fraudeur à la carte bancaire")

# Add an image to the main content area
st.image("delicieux.jpg", caption="Delicieux")