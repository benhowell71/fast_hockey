import requests
import json
import time

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

full_url = "https://www.sdhl.se/api/site/settings"

res = requests.get(full_url)
# BeautifulSoup(res.content, 'html.parser')
data = json.loads(res.content.decode('utf-8'))
[x for x in data]