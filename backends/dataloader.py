import os
from typing import Optional, Union, Dict, Any, List

import numpy as np
import pandas as pd
import pymongo

class DataSet(object):
    def __init__(self,file_path):
        self._path = file_path
        self.data =
