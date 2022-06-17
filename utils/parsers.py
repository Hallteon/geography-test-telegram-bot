import re

import requests
from bs4 import BeautifulSoup

from data.config import USER_AGENT

headers = {"accept": "*/*",
           "user-agent": USER_AGENT}

