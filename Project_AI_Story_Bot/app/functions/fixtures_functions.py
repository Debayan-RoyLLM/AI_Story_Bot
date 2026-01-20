from sqlalchemy.orm import Session

from app.Queries.fixture_queries import (
    Fixture_query, Info_query, Player2_name
    , Second_Team, Batting_Team_id, get_current_run_ball, get_bowling_team_total,
    get_bowling_team_id, get_current_run_ball_player1, bowler_wickets, last_two_balls)

def get_latest_fixture(
    db: Session,
    country_id: int,
    league_id: int
):
    result = db.execute(
        Fixture_query,
        {
            "country_id": country_id,
            "league_id": league_id
        }
    ).fetchone()

    return result.fixture_id


def get_info( db: Session, fixture_id: int, over: float):
    
    result = db.execute(
        Info_query,
        {
            "fixture_id": fixture_id,
            "over":over
        }
    ).fetchall()

    return [
        {
            "team_name": row.team__name,
            "team_id": row.team_id,
            "batsman": row.batsman__fullname,
            "batsman_id": row.batsman_id,
            "non_striker_id": row.batsman_two_on_creeze_id,
            "bowler": row.bowler__fullname,
            "bowler_id": row.bowler__id,
            "ball": row.ball
        }
        for row in result
    ]

def get_player2_name(db: Session, player_id: int):
    result = db.execute(
        Player2_name,
        {
            "batsman2_id": player_id
        }
    ).fetchone()
    return result.fullname

def second_team_name(db: Session, fixture_id: int, over: float):
    result = db.execute(
        Second_Team,
        {
            "fixture_id": fixture_id,
            "over":over
        }
    ).fetchall()

    return [
        {
            "team_name": row.team__name,
            "bowler_id": row.bowler__id,
            "current_ball": row.ball
        }
        for row in result
    ]

def get_batting_team_id(db: Session, fixture_id:int, player_id: int):
    result = db.execute(
        Batting_Team_id,
        {
            "fixture_id": fixture_id,
            "player_id": player_id
        }
    ).fetchone()
    return result.team_id


def get_current_run(db: Session, fixture_id: int, batting_team_id: int):
    result = db.execute(
        get_current_run_ball,
        {
            "fixture_id": fixture_id,
            "team_id": batting_team_id
        }
    ).fetchall()
    return result

def bowling_team_id(db: Session, fixture_id:int, player_id: int):
    result = db.execute(
        get_bowling_team_id,
        {
            "fixture_id": fixture_id,
            "player_id":player_id
        }
    ).fetchone()
    return result.team_id

def bowling_team_total(db: Session, fixture_id: int, bowling_team_id: int):
    result = db.execute(
        get_bowling_team_total,
        {
            "fixture_id": fixture_id,
            "team_id": bowling_team_id
        }
    ).fetchone()
    return result.score

def get_current_player_run(db: Session, fixture_id: int, batsman_id: int):
    rows = db.execute(
        get_current_run_ball_player1,
        {
            "fixture_id": fixture_id,
            "batsman_id": batsman_id,
        }
    ).fetchall()

    balls_faced = len(rows)
    total_runs = sum(row[1] for row in rows)
    strike_rate = total_runs/balls_faced

    return total_runs, balls_faced, strike_rate

def get_current_player2_run(db: Session, fixture_id: int, batsman_id: int):
    rows = db.execute(
        get_current_run_ball_player1,
        {
            "fixture_id": fixture_id,
            "batsman_id": batsman_id
        }
    ).fetchall()

    balls_faced = len(rows)
    total_runs = sum(row[1] for row in rows)

    return total_runs, balls_faced

def get_bowler_wickets(db: Session, fixture_id: int, bowler_id: int):
    result = db.execute(
        bowler_wickets,
        {
            "fixture_id": fixture_id,
            "bowler_id": bowler_id
        }
    ).fetchone()

    return result.score__out

def get_last_two_balls(db: Session, fixture_id: int, team_id: int):
    rows = db.execute(
        last_two_balls,
        {
            "fixture_id": fixture_id,
            "team_id": team_id
        }
    ).fetchall()

    # Defaults
    second_last_run = 0
    last_run = 0

    if rows:
        # rows are in DESC order → reverse to chronological
        rows = list(reversed(rows))

        if len(rows) == 1:
            last_run = rows[0][0]
        else:
            second_last_run = rows[0][0]
            last_run = rows[1][0]

    return {
        "second_last_ball": second_last_run,
        "last_ball": last_run
    }
