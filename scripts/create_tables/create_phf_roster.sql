drop table if exists phf_roster;

create table phf_roster (
    player_name varchar(75),
    player_id float,
    jersey int,
    position varchar(6),
    date_of_birth date,
    season int,
    season_id int,
    team varchar(75),
    team_id int,
    league varchar(6),
    league_id int,
    height varchar(12),
    feet float, 
    inches float,
    home_town varchar(50),
    country varchar(50),
    college varchar(150),
    is_captain int,
    player_photo varchar(300)
);