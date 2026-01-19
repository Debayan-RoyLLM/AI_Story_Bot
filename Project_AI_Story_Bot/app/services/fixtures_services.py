from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.functions.fixtures_functions import (
    get_latest_fixture, get_info, get_player2_name,second_team_name)


router = APIRouter(prefix="/fixtures", tags = ["Fixtures"])

@router.get("/latest")
def latest_fixture(country_id:int, league_id: int, db: Session = Depends(get_db)):
    fixture_id = get_latest_fixture(db, country_id, league_id)

    if not fixture_id:
        return {"message": "No fixture found"}
    
    over = 0.1
    data = get_info(db, fixture_id, over)
    non_striker_id = data[0]["non_striker_id"]
    player2_name = get_player2_name(db, non_striker_id)
    second_team = second_team_name(db, fixture_id, over)
    
    return {
        "Fixture": fixture_id,
        "data":data,
        "Player2_name": player2_name,
        "Second_Team": second_team
    }


'''
from app.repository.fixture_repo import get_max_fixture_id, get_playing_players_id_name, get_player2_name, get_second_team_name


# Balls Bowled Till Now
def calculate_total_balls(ball_current: float):
    overs = int(ball_current)
    balls = int(round((ball_current - overs) * 10))
    return overs * 6 + balls


def find_latest_fixture(country_id: int, league_id: int, db):
    if country_id <= 0 or league_id <= 0:
        raise ValueError("Invalid country_id or league_id")

    max_fixture_id = get_max_fixture_id(db, country_id, league_id)
    if not max_fixture_id:
        return {"message": "No fixtures found"}

    over = 0.1
    while over <= 20.0:

        fixture_rows = get_playing_players_id_name(
            db, max_fixture_id, round(over, 1)
        )

        if not fixture_rows:
            over = round(over + 0.1, 1)
            continue

        row = fixture_rows[0]

        # Primary data
        batsman_name = row.batsman__fullname
        batsman_id = row.batsman_id
        batsman_two_id = row.batsman_two_on_creeze_id
        bowler_name = row.bowler__fullname
        ball = round(row.ball, 1)
        batting_team = row.team__name
        scoreboard = row.scoreboard

        # Second batsman
        player2_rows = get_player2_name(db, batsman_two_id)
        batsman2_name = player2_rows[0].fullname if player2_rows else "Unknown"

        # Bowling team
        bowling_team_rows = get_second_team_name(db, max_fixture_id, ball)
        bowling_team_name = (
            bowling_team_rows[0].team__name if bowling_team_rows else "Unknown"
        )

        total_balls = calculate_total_balls(ball)

        # Narrative
        narrative = (
            f"{batsman_name} is batting with {batsman2_name} "
            f"for {batting_team}. {bowler_name} is bowling for "
            f"{bowling_team_name}. Current score: {scoreboard} off {total_balls} balls."
        )

        return {
            "country_id": country_id,
            "league_id": league_id,
            "latest_fixture_id": max_fixture_id,
            "over": ball,
            "narrative": narrative
        }

    return {"message": "No live ball data found"}
'''