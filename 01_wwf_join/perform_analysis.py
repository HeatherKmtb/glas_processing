import logging
import os
import geopandas


from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        file = self.params['glas_file']
        out_file = self.params['out_file']
        wwf = self.params["wwf"]
        
        base_gdf = geopandas.read_file(file)
        join_gdf = geopandas.read_file(wwf)
        
        base_gdf = base_gdf.set_crs("EPSG:4326")
        print("crs set")
           
        geostats = geopandas.sjoin(base_gdf, join_gdf, how='inner', op='within',lsuffix='lefty',rsuffix='righty')
    
        geostats.to_file(out_file, driver='GPKG', crs='EPSG:4326')        
        
        

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return ["glas_file", "out_file", "wwf"]

    def outputs_present(self, **kwargs):
        # Check the output files are as expected - called with --check option
        # the function expects a tuple with the first item a list of booleans
        # specifying whether the file is OK and secondly a dict with outputs
        # as keys and any error message as the value

        # A function (self.check_files) has been provided to do the work for
        # you which takes a dict of inputs which will do the work for you in
        # most cases. The supported file types are: gdal_image, gdal_vector,
        # hdf5, file (checks present) and filesize (checks present and size > 0)

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

