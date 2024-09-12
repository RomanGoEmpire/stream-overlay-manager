import json
import streamlit as st
from pydantic import BaseModel


# data path
PLAYERS_DATA_PATH = "data/players.json"
COMMENTATOR_DATA_PATH = "data/commentators.json"

# overlay paths
TOURNAMENT_NAME_PATH = "overlay/tournament/tournament_name.txt"
BLACK_PATH = "overlay/black"
WHITE_PATH = "overlay/white"
COMMENTATOR_PATH = "overlay/commentator"


AMOUNT_COMMENTATORS = 4


class Player(BaseModel):
    name: str
    rank: str
    country: str


def write_player(path: str, player: Player) -> None:
    with open(f"{path}/name.txt", "w") as f:
        f.write(player.name.upper())

    with open(f"{path}/rank.txt", "w") as f:
        f.write(player.rank.upper())

    with open(f"svg/{player.country}.svg", "rb") as f:
        country_img = f.read()

    with open(f"{path}/country.svg", "wb") as f:
        f.write(country_img)


def load_json(path: str) -> list[Player]:
    with open(path) as f:
        return [Player(**p) for p in json.load(f)]


def index_players(path: str) -> int:
    with open(f"{path}/name.txt") as f:
        player = f.read().strip()
        return next(
            (i for i, p in enumerate(players) if p.name.upper() == player.upper()), 0
        )


def index_commentator(path: str) -> int:
    with open(path) as f:
        commentator = f.read().strip()
        return next(
            (
                i
                for i, p in enumerate(commentators)
                if f"{p.name} {p.rank}".upper() == commentator.upper()
            ),
            0,
        )


def commentator_selectbox(column, index: int) -> Player:
    return column.selectbox(
        f"Commentator {index}",
        options=commentators,
        index=index_commentator(f"{COMMENTATOR_PATH}/commentator_{index}.txt"),
        format_func=lambda p: f"{p.name} {p.rank}",
        key=f"commentator_{index}",
    )


players = load_json(PLAYERS_DATA_PATH)
commentators = [Player(name="", rank="", country="")] + load_json(COMMENTATOR_DATA_PATH)


st.title("Stream Overlay Manager")

with open(TOURNAMENT_NAME_PATH) as f:
    current_tournament_name = f.read().strip()
tournament_name = st.text_input("Tournament Name", current_tournament_name)

st.subheader("Commentators", divider="blue")

columns = st.columns(AMOUNT_COMMENTATORS)

selected_commentators = [
    commentator_selectbox(columns[i - 1], i)
    for i in range(1, AMOUNT_COMMENTATORS + 1, 1)
]

st.subheader("Players", divider="blue")
c1, c2 = st.columns(2)
black_player = c1.selectbox(
    "Black Player",
    options=players,
    index=index_players(BLACK_PATH),
    format_func=lambda p: f"{p.name} {p.rank}",
)
white_player = c2.selectbox(
    "White Player",
    options=players,
    index=index_players(WHITE_PATH),
    format_func=lambda p: f"{p.name} {p.rank}",
)


if st.button("Update", type="primary"):
    with open(TOURNAMENT_NAME_PATH, "w") as f:
        f.write(tournament_name)

    write_player(BLACK_PATH, black_player)
    write_player(WHITE_PATH, white_player)

    for i, commentator in enumerate(selected_commentators):
        with open(f"{COMMENTATOR_PATH}/commentator_{i+1}.txt", "w") as f:
            f.write(f"{commentator.name} {commentator.rank}".upper())

    st.rerun()
