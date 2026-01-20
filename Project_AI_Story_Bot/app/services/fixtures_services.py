from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import csv
from app.db.database import get_db
from app.functions.fixtures_functions import (
    get_latest_fixture, get_info, get_player2_name,second_team_name
    ,get_batting_team_id, get_current_run,bowling_team_total, bowling_team_id,
    get_current_player_run, get_current_player2_run, get_bowler_wickets, get_last_two_balls,get_team_wickets)


router = APIRouter(prefix="/fixtures", tags = ["Fixtures"])

def ball_to_over(ball_no: int) -> float:
    over = (ball_no - 1) // 6
    ball = (ball_no - 1) % 6 + 1
    return over + ball / 10

@router.get("/latest")
def latest_fixture(country_id: int, league_id: int, db: Session = Depends(get_db)):

    fixture_id = get_latest_fixture(db, country_id, league_id)
    if not fixture_id:
        return {"message": "No fixture found"}

    csv_file = "narratives.csv"
    rows = []

    total_balls_to_simulate = 1 # 2 overs

    for ball_no in range(1, total_balls_to_simulate + 1):

        over = ball_to_over(ball_no)
        data = get_info(db, fixture_id, over)
        if not data:
            continue

        non_striker_id = data[0]["non_striker_id"]
        batsman_id = data[0]["batsman_id"]

        player2_name = get_player2_name(db, non_striker_id)
        second_team = second_team_name(db, fixture_id, over)
        bowler_id = second_team[0]["bowler_id"]

        batting_team_id = get_batting_team_id(db, fixture_id, batsman_id)

        _bowling_team_id = bowling_team_id(db, fixture_id, bowler_id)
        batting_team_run = get_current_run(db, fixture_id, batting_team_id)

        Target_Score = bowling_team_total(db, fixture_id, _bowling_team_id)
        live_score = batting_team_run[0].score__runs
        
        wickets_bowler = get_bowler_wickets(db, fixture_id, bowler_id, over)    
        current_ball = second_team[0]["current_ball"]
        current_over = int(current_ball)
        balls_bowled = int((current_ball - current_over) * 10)
        total_balls = current_over * 6 + balls_bowled
        balls_remaining = 120 - total_balls

        data0 = data[0]

        batsman_runs, batsman_balls, strike_rate = get_current_player_run(
            db, fixture_id, batsman_id, current_ball
        )

        batsman2_runs, batsman2_balls = get_current_player2_run(
            db, fixture_id, non_striker_id, current_ball
        )

        runs_required = Target_Score - live_score
        required_run_rate = round((runs_required / balls_remaining) * 6, 2)

        overs_bowled = total_balls / 6
        current_run_rate = round(live_score / max(overs_bowled, 0.1), 2)
        team_wicket = get_team_wickets(db, fixture_id, batting_team_id, current_ball)

        wickets_in_hand = 10 - team_wicket

        last_two = get_last_two_balls(db, fixture_id, batting_team_id, current_ball)

        narrative = (
            f"{data0['batsman']} and {player2_name} are batting for {data0['team_name']} with "
            f"{runs_required} runs required off {balls_remaining} balls.\n"
            f"{data0['batsman']} is on {batsman_runs} off {batsman_balls} balls with a strike rate of {strike_rate}, "
            f"while {player2_name} is on {batsman2_runs} from {batsman2_balls} balls.\n"
            f"The bowler, {data0['bowler']}, has taken {wickets_bowler} wickets already in this match.\n"
            f"The required run rate is {required_run_rate}, while the current run rate is {current_run_rate}.\n"
            f"There are {wickets_in_hand} wickets in hand. "
            f"The last two balls were {last_two['second_last_ball']},{last_two['last_ball']}."
        )

        rows.append([fixture_id, over, narrative])

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fixture_id", "over", "narrative"])
        writer.writerows(rows)

    return {
        "fixture_id": fixture_id,
        "overs_simulated": 2,
        "rows_written": len(rows)
    }
