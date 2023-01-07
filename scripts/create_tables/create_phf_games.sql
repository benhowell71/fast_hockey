drop table if exists phf_games;

create table phf_games (
    team varchar(75), 
    game_id int, 
    winner boolean, 
    successful_power_plays float, 
    power_play_opportunities float,
    power_plays float, 
    penalty_minutes int, 
    faceoff_win_pct float, 
    blocks int,
    takeaways int, 
    giveaways int, 
    period_1_shots int, 
    period_2_shots int,
    period_3_shots int, 
    overtime_shots float, 
    shootout_made_shots float,
    shootout_missed_shotsfloat, 
    total_shots int, 
    period_1_scoring int,
    period_2_scoring int, 
    period_3_scoring int,
    overtime_scoring float, 
    shootout_made_scoring float, 
    shootout_missed_scoring float, 
    total_scoring int
);