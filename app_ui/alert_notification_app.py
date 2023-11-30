"""
This script when executed runs application. 
This application script is triggered when there is a panic braking in the close vicintiy.
"""
import streamlit as st
import pandas as pd
import base64
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("assets/background-wireframe.jpg")

page_bg_img = f"""
<style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: 52%;
    background-position: center;
    background-repeat: no-repeat;
    opacity:0.7;
    background-attachment: local;
    }}
</style>
"""

col1, col2, col3 = st.columns(3)
with col1:
    # additional whitespace for centralizing the content
    print() 
with col2:
    st.markdown(page_bg_img, unsafe_allow_html=True)
    button_placeholder = st.empty()
    with stylable_container(
        key="black_button",
        css_styles=[
            """
            button {
                border: solid .3em #292746;
                border-radius: 20px;
                color: #fff;
                background-color: #292746;
                position: absolute;
                top: 40px; /* Adjust this value to your desired y-coordinate */
                left: 20px;
                # display: grid;
                # place-items: center;
            }
            """,
            """
            button:hover {
                background-color: red;
            }
            """,
        ],
    ):
     open_button = st.button(label='Proximity Brake Alert')
    
    if open_button:
        df= pd.read_csv("../panic_brake_alert.csv")
        # creating Proximity range to be updated in the map
        df['sizes'] = [10, 10, 80]
        # Color code for the markers in the map
        df['color'] = [(255, 0, 0), (0, 204, 102), (255, 0, 0, 0.5)]
        # outputs the map
        st.map(df, latitude='lat', longitude='lon', color = 'color', size="sizes",zoom = 15) 

with col3:
    # additional whitespace for centralizing the content
    print() 

