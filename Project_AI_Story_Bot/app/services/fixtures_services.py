from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.functions.fixtures_functions import (
    get_latest_fixture, get_info, get_player2_name,second_team_name
    ,get_batting_team_id, get_current_run,bowling_team_total, bowling_team_id,
    get_current_player_run, get_current_player2_run, get_bowler_wickets, get_last_two_balls)


router = APIRouter(prefix="/fixtures", tags = ["Fixtures"])

@router.get("/latest")
def latest_fixture(country_id: int, league_id: int, db: Session = Depends(get_db)):
    fixture_id = get_latest_fixture(db, country_id, league_id)

    if not fixture_id:
        return {"message": "No fixture found"}

    over = 0.1
    data = get_info(db, fixture_id, over)

    non_striker_id = data[0]["non_striker_id"]
    batsman_id = data[0]["batsman_id"]

    player2_name = get_player2_name(db, non_striker_id)
    second_team = second_team_name(db, fixture_id, over)
    bowler_id = second_team[0]["bowler_id"]
    batting_team_id = get_batting_team_id(db, fixture_id, batsman_id)
    batting_team_run = get_current_run(db, fixture_id, batting_team_id)
    _bowling_team_id = bowling_team_id(db, fixture_id, bowler_id)
    Target_Score = bowling_team_total(db, fixture_id, _bowling_team_id)
    live_score = batting_team_run[0].score__runs

    batsman_runs,batsman_balls, strike_rate  = get_current_player_run(db, fixture_id, batsman_id)
    batsman2_runs,batsman2_balls  = get_current_player2_run(db, fixture_id, non_striker_id)
    wickets_bowler = get_bowler_wickets(db, fixture_id, bowler_id)
    bowler_wickets = 0
    team_wicket = 0
    if wickets_bowler == 1:
        bowler_wickets= bowler_wickets+1
        team_wicket = team_wicket+1
    
    current_ball = second_team[0]["current_ball"]
    over = int(current_ball)
    balls_bowled = round((current_ball - over) * 10)
    total_balls = over * 6 + balls_bowled
    balls_remaining = (20 * 6) - total_balls
    data0 = data[0]

    batsman_name = data0["batsman"]
    nonstriker_name = player2_name
    team_name = data0["team_name"]
    bowler_name = data0["bowler"]

    runs_required = Target_Score - live_score
    #balls_remaining = "yet to be determined"
    batsman_sr = strike_rate
    required_run_rate = round((runs_required/balls_remaining)*6,2)

    nonstriker_runs = batsman2_runs
    nonstriker_balls = batsman2_balls

    current_run_rate = round(live_score / max(data0["ball"], 0.1), 2)

    wickets_in_hand = 10 - team_wicket
    last_two = get_last_two_balls(db, fixture_id, batting_team_id)

    second_last_ball = last_two["second_last_ball"]
    last_ball = last_two["last_ball"]

    narrative = (
    f"{batsman_name} and {nonstriker_name} are batting for {team_name} with "
    f"{runs_required} runs required off {balls_remaining} balls.\n"
    f"{batsman_name} is on {batsman_runs} off {batsman_balls} balls with a strike rate of {batsman_sr}, "
    f"while {nonstriker_name} is on {nonstriker_runs} from {nonstriker_balls} balls.\n"
    f"The bowler, {bowler_name}, has taken {bowler_wickets} wickets already in this match.\n"
    f"The required run rate is {required_run_rate}, while the current run rate is {current_run_rate}.\n"
    f"There are {wickets_in_hand} wickets in hand. The last two balls were {second_last_ball},{last_ball}."
)


    # response
    return {
        narrative
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