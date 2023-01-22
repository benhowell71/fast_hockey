import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

def sdhl_standings(season: int) -> pd.DataFrame:

    base_url = "https://www.sdhl.se/game-stats/teams/result?ssgtUuid=qbO-5Eadc4G0L&count=25"
    full_url = "https://www.sdhl.se/game-stats/teams/result?ssgtUuid=qbO-5Eadc4G0L&count=25"

    res = requests.get(full_url)
    BeautifulSoup(res.content, 'html.parser')
    json.loads(res.content.decode('utf-8'))

    for i in np.arange(0, len(res.content)):
        res.content[i]

        time.sleep(1)