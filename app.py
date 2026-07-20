import streamlit as st
import requests
import pandas as pd

st.title("NBA Analytics Dashboard")

CURRENT_TEAMS = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons","Golden State Warriors","Houston Rockets","Indiana Pacers","LA Clippers","Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks","Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder","Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers","Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"]

API_KEY = "d7796659-7085-488f-8a23-4f312f94c57a"
HEADERS = {"Authorization": API_KEY}

# ---- SECTION 1: TEAMS ----
st.header("Team Directory")
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

# ---- SECTION 2: SEASON LEADERS ----
st.header("🏆 2024-25 Season Leaders")

def get_season_leaders(sort_by, label, min_games=40):
    url = f"https://api.balldontlie.io/v1/season_averages?season=2024&per_page=100"
    r = requests.get(url, headers=HEADERS)
    data = r.json().get("data", [])
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df[df["games_played"] >= min_games]
    df = df.sort_values(sort_by, ascending=False).head(10)

    # Get player names
    player_ids = df["player_id"].tolist()
    names = []
    for pid in player_ids:
        pr = requests.get(f"https://api.balldontlie.io/v1/players/{pid}", headers=HEADERS)
        p = pr.json()
        names.append(p.get("first_name","") + " " + p.get("last_name",""))
    df["Player"] = names
    return df[["Player", sort_by, "games_played"]].rename(columns={sort_by: label, "games_played": "Games"})

col1, col2 = st.columns(2)

with col1:
    with st.spinner("Loading scoring leaders..."):
        df_pts = get_season_leaders("pts", "PPG")
    if df_pts is not None:
        st.subheader("Top Scorers (PPG)")
        st.dataframe(df_pts.reset_index(drop=True), use_container_width=True)

with col2:
    with st.spinner("Loading assists leaders..."):
        df_ast = get_season_leaders("ast", "APG")
    if df_ast is not None:
        st.subheader(" Top Assists (APG)")
        st.dataframe(df_ast.reset_index(drop=True), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    with st.spinner("Loading steals leaders..."):
        df_stl = get_season_leaders("stl", "SPG")
    if df_stl is not None:
        st.subheader("Top Steals (SPG)")
        st.dataframe(df_stl.reset_index(drop=True), use_container_width=True)

with col4:
    with st.spinner("Loading blocks leaders..."):
        df_blk = get_season_leaders("blk", "BPG")
    if df_blk is not None:
        st.subheader(" Top Blocks (BPG)")
        st.dataframe(df_blk.reset_index(drop=True), use_container_width=True)

st.subheader(" Top 3-Point Shooters (3P%)")
with st.spinner("Loading 3PT leaders..."):
    df_3pt = get_season_leaders("fg3_pct", "3P%", min_games=40)
if df_3pt is not None:
    df_3pt["3P%"] = (df_3pt["3P%"] * 100).round(1).astype(str) + "%"
    st.dataframe(df_3pt.reset_index(drop=True), use_container_width=True)