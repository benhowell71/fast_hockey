drop table if exists phf_schedule;

create table phf_schedule (
    team_name varchar(50), 
    team_id int, 
    league_id int, 
    league varchar(10), 
    season int, 
    season_id int, 
    games_played int, 
    wins int, 
    losses int,
    ties int, 
    points int, 
    regulation_wins int, 
    overtime_wins int, 
    shootout_wins int,
    goals_scored int, 
    goals_allowed int, 
    goal_differential int, 
    penalty_minutes int,
    next_game varchar(25), 
    full_team_name varchar(100), 
    team_abbr varchar(6), 
    team_nick varchar(20),
    team_location varchar(30), 
    team_color1 varchar(10), 
    team_color2 varchar(10), 
    team_logo varchar(300),
    PRIMARY KEY (team_id, season_id)
);