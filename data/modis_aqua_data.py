from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd


@st.cache_data
def load_nasa_modis_images():
    nasa_df_pickle_path = "/Users/ashrayuddaraju/Documents/GitHub/nsa25_practice/nasa_data/nasa_data_df.pkl"
    # serialize_df_to_images(directory_path, "/home/dhan/code/misc/streamlit_tutorial/nasa_data/images")
    # serialize_df(directory_path, nasa_df_pickle_path)
    # Restore the DataFrame from the file
    restored_df = pd.read_pickle(nasa_df_pickle_path)
    restored_df['year'] = restored_df['start_date'].astype(str).str[:4].astype(int)
    restored_df['month'] = restored_df['start_date'].astype(str).str[5:7].astype(int)       
    return restored_df