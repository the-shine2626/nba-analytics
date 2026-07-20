import streamlit as st
import requests
import pandas as pd

st.title("🏀 NBA Analytics Dashboard")

CURRENT_TEAMS = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","LA Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]

API_KEY = "d7796659-7085-488f-8a23-4f312f94c57a"
HEADERS = {"Authorization": API_KEY}

# ---- SECTION 1: TEAMS ----
st.header(" Team Directory")
with st.spinner("Loading teams..."):
    r = requests.get("https://api.balldontlie.io/v1/teams", headers=HEADERS)
    teams = r.json()["data"]
    df_teams = pd.DataFrame(teams)

df_teams = df_teams[df_teams["full_name"].isin(CURRENT_TEAMS)]
df_teams = df_teams[["full_name","conference","division","city","abbreviation"]].copy()
df_teams.columns = ["Team","Conference","Division","City","Abbr"]
df_teams = df_teams.drop_duplicates(subset=["Team"]).sort_values("Team").reset_index(drop=True)

conf = st.selectbox("Filter by Conference", ["All", "East", "West"])
df_filtered = df_teams if conf == "All" else df_teams[df_teams["Conference"] == conf]
st.dataframe(df_filtered, use_container_width=True)

# ---- SECTION 2: STAT LEADERS (hardcoded 2024-25 season) ----
st.header("🏆 2024-25 Season Leaders")
st.caption("Stats from the 2024-25 NBA season")

leaders = {
    " Top Scorers (PPG)": [
        {"Player": "Shai Gilgeous-Alexander", "PPG": 32.7, "Team": "OKC"},
        {"Player": "Giannis Antetokounmpo", "PPG": 30.4, "Team": "MIL"},
        {"Player": "Jayson Tatum", "PPG": 28.4, "Team": "BOS"},
        {"Player": "Karl-Anthony Towns", "PPG": 26.0, "Team": "NYK"},
        {"Player": "LeBron James", "PPG": 23.7, "Team": "LAL"},
    ],
    " Top Assists (APG)": [
        {"Player": "Trae Young", "APG": 11.6, "Team": "ATL"},
        {"Player": "Tyrese Haliburton", "APG": 9.2, "Team": "IND"},
        {"Player": "LaMelo Ball", "APG": 8.8, "Team": "CHA"},
        {"Player": "Shai Gilgeous-Alexander", "APG": 6.4, "Team": "OKC"},
        {"Player": "James Harden", "APG": 7.1, "Team": "LAC"},
    ],
    " Top Steals (SPG)": [
        {"Player": "Shai Gilgeous-Alexander", "SPG": 2.1, "Team": "OKC"},
        {"Player": "Dyson Daniels", "SPG": 2.9, "Team": "ATL"},
        {"Player": "De'Aaron Fox", "SPG": 1.6, "Team": "SAC"},
        {"Player": "OG Anunoby", "SPG": 1.6, "Team": "NYK"},
        {"Player": "Herb Jones", "SPG": 1.5, "Team": "NOP"},
    ],
    " Top Blocks (BPG)": [
        {"Player": "Victor Wembanyama", "BPG": 3.6, "Team": "SAS"},
        {"Player": "Brook Lopez", "BPG": 2.6, "Team": "MIL"},
        {"Player": "Walker Kessler", "BPG": 2.3, "Team": "UTA"},
        {"Player": "Jaren Jackson Jr.", "BPG": 2.5, "Team": "MEM"},
        {"Player": "Alperen Sengun", "BPG": 1.8, "Team": "HOU"},
    ],
    " Top 3PT Shooters (3P%)": [
        {"Player": "Lindy Waters III", "3P%": "51.2%", "Team": "OKC"},
        {"Player": "Malik Beasley", "3P%": "44.8%", "Team": "MIL"},
        {"Player": "Luke Kennard", "3P%": "44.2%", "Team": "MEM"},
        {"Player": "Buddy Hield", "3P%": "43.9%", "Team": "GSW"},
        {"Player": "Desmond Bane", "3P%": "43.1%", "Team": "MEM"},
    ],
}

col1, col2 = st.columns(2)
cols = [col1, col2, col1, col2, col1]

for i, (title, data) in enumerate(leaders.items()):
    with cols[i]:
        st.subheader(title)
        st.dataframe(pd.DataFrame(data), use_container_width=True)