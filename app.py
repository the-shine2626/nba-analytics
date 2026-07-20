import streamlit as st
from nba_api.stats.endpoints import leaguestandings
import pandas as pd

st.title("NBA Analytics Dashboard")
st.subheader("Live Team Standings")

with st.spinner("Loading NBA data..."):
    standings = leaguestandings.LeagueStandings()
    df = standings.get_data_frames()[0]

df_clean = df[[
    "TeamName", "Conference", "WINS", "LOSSES", "WinPCT",
    "PointsPG", "OppPointsPG"
]].copy()

df_clean.columns = [
    "Team", "Conference", "Wins", "Losses", "Win %",
    "Pts Per Game", "Opp Pts Per Game"
]

df_clean = df_clean.sort_values("Win %", ascending=False).reset_index(drop=True)

conf = st.selectbox("Filter by Conference", ["All", "East", "West"])
if conf == "East":
    df_clean = df_clean[df_clean["Conference"] == "East"]
elif conf == "West":
    df_clean = df_clean[df_clean["Conference"] == "West"]

st.dataframe(df_clean, width="stretch")

st.subheader("Wins by Team")
st.bar_chart(df_clean.set_index("Team")["Wins"])