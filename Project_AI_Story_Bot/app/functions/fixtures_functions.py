from sqlalchemy.orm import Session

from app.Queries.fixture_queries import (
    Fixture_query, Info_query, Player2_name
    , Second_Team)

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
            "team_name": row.team__name
        }
        for row in result
    ]

'''
def get_current_run(db: Session, fixture_id: int, team_id: int):
    result = db.execute(
        get_current_run,
        {
            "fixture_id": fixture_id,
            "team_id": 
        }
    )
    '''