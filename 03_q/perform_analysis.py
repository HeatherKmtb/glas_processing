import logging
import os
import geopandas
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.stats import gaussian_kde

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        file = self.params['glas_file']
        out_fig_dir = self.params['out_fig_dir']
        out_csv_file = self.params['out_csv_file']

        #create df for results
        resultsa = pd.DataFrame(columns = ['Grid', 'eco', 'qout_glas', 'deg_free', 'mse',
                                           'mean_h', 'mean_cd', 'max_h'])


        hd, tl = os.path.split(file)
        shp_lyr_name = os.path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[1] 
        eco = name_comp[3]
        print(name)
        print(eco)
        
            
        final = geopandas.read_file(file)
             
        footprints = len(final['i_h100'])
        
        #regression 
        def f(x,q):
           return 1- np.exp(-q * x)
    
        x = final['i_h100'].to_numpy()
        y = final['i_cd'].to_numpy() 

        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        
        y_predict = f(x, qout)
            
        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)        

        meanh = np.mean(x)
        meancd = np.mean(y)
        maxh = np.max(x)
        
        resultsa = resultsa.append({'Grid': name, 'eco':eco, 'qout_gedi': qout, 
                                    'deg_free_g': footprints, 
                                    'mse_g': mse,
                                    'mean_h_g': meanh, 'mean_cd_g': meancd, 
                                    'max_h_g': maxh}, 
                                    ignore_index=True)

        resultsa.to_csv(out_csv_file)

        xy = np.vstack([x,y])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=10)
        plt.rcParams.update({'font.size':12}) 

        ax.set_title('Ecoregion ' + eco + 'in grid square ' + name)
        ax.set_ylabel('Canopy Density')
        ax.set_xlabel('Height - h100 (m)')
        ax.set_xlim([0, 60])
        ax.set_ylim([0,1])
        #plotting regression
        #putting x data in an order, cause that's what the code needs
        xdata = np.linspace(0, 60)
        #for each value of x calculating the corresponding y value
        ycurve = [f(t, qout) for t in xdata]
        #plotting the curve
        ax.plot(xdata, ycurve, linestyle='-', color='red')
        #adding qout, mse and deg_free to plot
        #ax.annotate('adj_r2 = ' + str(adj_r2[0]), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('MSE = ' + str(mse), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(out_fig_dir + 'fig{}_{}.png'.format(name, eco))
        plt.close 
   
        

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return ["glas_file", "out_fig_dir", "out_csv_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["output1"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["output1"]):
            os.remove(self.params["output1"])


if __name__ == "__main__":
    ProcessCmd().std_run()

