import numpy as np

def phf_get_season_id(season: int):

    if season == 2023:
        return 4667
    elif season == 2022:
        return 3372
    elif season == 2021:
        return 2779
    elif season == 2020:
        return 1950
    elif season == 2019:
        return 2047
    elif season == 2018:
        return 2046
    elif season == 2017:
        return 2045
    elif season == 2016:
        return 246
    else:
        return np.nan