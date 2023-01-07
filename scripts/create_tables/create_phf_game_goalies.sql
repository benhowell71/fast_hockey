drop table if exists phf_game_goalies;

create table phf_game_goalies (
    player_name varchar(100), 
    player_id float, 
    team varchar(100), 
    jersey int, 
    game_id int, 
    time_on_ice varchar(10), 
    minutes_played float, 
    shots_against int, 
    saves int, 
    goals_allowed int, 
    save_pct float, 
    penalty_minutes int, 
    goals int, 
    assists int
);