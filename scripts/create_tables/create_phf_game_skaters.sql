drop table if exists phf_game_skaters;

create table phf_game_skaters (
    player_name varchar(100),
    player_id float,
    team varchar(100),
    jersey int,
    position varchar(6),
    game_id int,
    goals int,
    assists int,
    points int,
    shots int,
    shots_blocked int,
    shots_on_goal int,
    shot_pct float,
    power_play_goal int,
    short_hand_goal int,
    plus_minus int,
    faceoff_record varchar(12),
    faceoff_win_pct float,
    faceoff_won int,
    faceoff_lost int,
    blocks int,
    penalty_minutes int,
    takeaways int,
    giveaways int
);