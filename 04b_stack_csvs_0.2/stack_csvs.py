import glob
import pandas as pd

csvs = glob.glob('/bigdata/cci_biomass_data/WCM/1_deg/eco/results_0723/csvs/0.2/*.csv')
out_file = '/bigdata/cci_biomass_data/WCM/1_deg/eco/results_0723/wwf_grid_0.2.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


