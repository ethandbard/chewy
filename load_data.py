from chewy_functions import *
import numpy as np
import pandas as pd

dict = load_json("test_dump.json")

# convert to pandas dataframe
df = pd.DataFrame.from_dict(dict, orient="index")

# save df to csv
