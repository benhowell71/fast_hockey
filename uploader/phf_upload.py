from uploader.updates.update_phf_schedule import update_phf_schedule
from uploader.updates.update_phf_box import update_phf_box
from uploader.updates.update_phf_game_box import update_phf_game_box

def phf_upload(season):
    # update player standings

    game_ids = update_phf_schedule(season=season)
    update_phf_box(game_ids=game_ids)
    update_phf_game_box(game_ids=game_ids)

    # with these game IDs, loop through and download the data for phf_games_box and player_box
    # delete from team and player stat tables
    # download team and player stats for current season
    # undecided on team rosters how often we want to update
    ##### 