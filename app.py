import streamlit as st
import requests
import pandas as pd

st.title("NBA Analytics dashboard")
st.subheader("Live team standings")

with st.spinner("Loading NBA data..."):
    url = "https://api.balldontlie.io/v1/teams"
    headers = {"Authorization": "d7796659-7085-488f-8a23-4f312f94c57a"}
    response = requests.get(url, headers=headers)
    teams = response.json()["data"]
    df = pd.DataFrame(teams)

df_clean = df[["full_name", "conference", "division", "city", "abbreviation"]].copy()
df_clean.columns = ["Team", "Conference", "Division", "City", "Abbr"]
df_clean = df_clean.sort_values("Team").reset_index(drop=True)

conf = st.selectbox("Filter by Conference", ["All", "East", "West"])
if conf == "East":
    df_clean = df_clean[df_clean["Conference"] == "East"]
elif conf == "West":
    df_clean = df_clean[df_clean["Conference"] == "West"]

st.dataframe(df_clean, use_container_width=True)
st.subheader("Teams by Division")
st.bar_chart(df_clean["Division"].value_counts())