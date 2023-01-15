from uploader.upload_phf_schedule import update_phf_schedule

def phf_upload():
    # update player standings

    game_ids = update_phf_schedule(season=2023)

    # with these game IDs, loop through and download the data for phf_games_box and player_box
    # delete from team and player stat tables
    # download team and player stats for current season
    # undecided on team rosters how often we want to update
    ##### 