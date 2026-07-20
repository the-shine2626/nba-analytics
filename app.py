import streamlit as st
import requests
import pandas as pd

import streamlit as st
import requests
import pandas as pd

st.title("🏀 NBA Analytics Dashboard")
st.subheader("Live Team Standings")

CURRENT_TEAMS = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","LA Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]

with st.spinner("Loading NBA data..."):
    url = "https://api.balldontlie.io/v1/teams"
    headers = {"Authorization": "d7796659-7085-488f-8a23-4f312f94c57a"}
    response = requests.get(url, headers=headers)
    teams = response.json()["data"]
    df = pd.DataFrame(teams)

df = df[df["full_name"].isin(CURRENT_TEAMS)]
df_clean = df[["full_name","conference","division","city","abbreviation"]].copy()
df_clean.columns = ["Team","Conference","Division","City","Abbr"]
df_clean = df_clean.drop_duplicates(subset=["Team"]).sort_values("Team").reset_index(drop=True)
conf = st.selectbox("Filter by Conference", ["All", "East", "West"])
if conf == "East":
    df_clean = df_clean[df_clean["Conference"] == "East"]
elif conf == "West":
    df_clean = df_clean[df_clean["Conference"] == "West"]

st.dataframe(df_clean, use_container_width=True)
st.subheader("Teams by Division")
st.bar_chart(df_clean["Division"].value_counts())