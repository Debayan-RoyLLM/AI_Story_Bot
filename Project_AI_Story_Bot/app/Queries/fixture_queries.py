"""
app.repository.fixture_repo
======================================
This module contains the queries for  sportmonk
"""

from sqlalchemy import text

Fixture_query = text("""
        SELECT MAX(f.id) AS fixture_id
        FROM history2.fixtures f
        JOIN history2.leagues l ON l.id = f.league_id
        JOIN history2.countries c ON c.id = l.country_id
        WHERE c.id = :country_id
        AND l.id = :league_id
    """)

#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

Info_query = text("""
        SELECT scoreboard,
               team__name,
               team_id,
               batsman__fullname,
               batsman_id,
               batsman_two_on_creeze_id,
               bowler__fullname,
               bowler__id,
               ball
        FROM history2.fixtures__balls
        WHERE fixture_id = :fixture_id
        AND ball BETWEEN :over - 0.001 AND :over + 0.001 AND scoreboard = 'S1'

    """)

#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

Player2_name = text("""
                SELECT fullname from history2.players where id=:batsman2_id
                 """)

#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

Second_Team= text("""
        SELECT scoreboard, team__name, team_id, batsman__fullname, batsman_id, batsman_two_on_creeze_id, bowler__fullname, bowler__id, ball
        FROM history2.fixtures__balls
        WHERE fixture_id = :fixture_id
          AND ball BETWEEN :over - 0.001 AND :over + 0.001
          AND scoreboard = 'S2'
    """)

#----------------------------------------------------------------------#
#----------------------------------------------------------------------#




'''
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

get_current_run_ball  = text("""
                select ball, score__runs from history2.fixtire__balls 
                where fixture_id = :fixture_id and team_id=:batting_team_id
                 """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

def get_bowling_team_ids(db, fixture_id: int, player_ids: list[int]):
    query = text("""
        SELECT player_id, team_id
        FROM history2.fixtures__bowling
        WHERE fixture_id = :fixture_id
          AND player_id = ANY(:player_ids)
    """)
    return db.execute(
        query,
        {"fixture_id": fixture_id, "player_ids": player_ids}
    ).fetchall()
'''