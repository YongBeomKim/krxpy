import re
import json
import pandas
import requests
import datetime
from urllib import parse
from pytip import FakeAgent, date_to_string, elapsed_time
from ..tools import (
    duplicate_name, convert_code_market, dataframe_fill_nat
)