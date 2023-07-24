import glob
import pandas as pd

csvs = glob.glob('/bigdata/cci_biomass_data/WCM/1_deg/eco/results_0723/csvs/*.csv')
out_file = '/bigdata/cci_biomass_data/WCM/1_deg/eco/results_0723/wwf_grid.csv'


dfList = [pd.read_csv(c) for c in csvs]
    
df = pd.concat(dfList)  
df.to_csv(out_file)


