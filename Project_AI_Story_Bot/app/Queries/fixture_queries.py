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

Batting_Team_id = text ("""
        select id,score,rate, team_id, ball from history2.fixtures__batting 
        where player_id = :player_id and fixture_id= :fixture_id            
        """)


#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

get_current_run_ball  = text("""
                select ball, score__runs from history2.fixtures__balls 
                where fixture_id = :fixture_id and team_id=:team_id
                 """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

get_bowling_team_id = text ("""
                select id, overs, runs, wickets, team_id 
                from history2.fixtures__bowling where fixture_id = :fixture_id 
                and player_id= :player_id
                """)


#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

get_bowling_team_total = text("""
                select score from history2.fixtures__runs 
                where team_id =:team_id and fixture_id=:fixture_id
                """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

get_current_run_ball_player1  = text("""
                select ball, score__runs from history2.fixtures__balls 
                where fixture_id = :fixture_id and batsman_id=:batsman_id
                """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

get_current_run_ball_player2  = text("""
                select ball, score__runs from history2.fixtures__balls 
                where fixture_id = :fixture_id and batsman_id=:batsman_id
                """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

bowler_wickets = text("""
                SELECT score__out
                FROM history2.fixtures__balls
                WHERE fixture_id = :fixture_id AND bowler_id = :bowler_id
                """)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

last_two_balls = text("""
                SELECT TOP 2 score__runs, ball
                FROM history2.fixtures__balls
                WHERE fixture_id = :fixture_id
                AND team_id = :team_id
                ORDER BY ball DESC
                """)