import os
from main import PROJECT_PATH

import logging

from bs4 import BeautifulSoup as bs

import json
import re
from js2py import eval_js

from ..xml_parsing import generate_csv
from ..html_parsing import generate_jsons