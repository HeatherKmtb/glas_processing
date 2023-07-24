import logging
import os
import geopandas
import rsgislib.vectorutils


from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        file = self.params['glas_file']
        out_file = self.params['out_file']
        basename = self.params['basename']

        
        #rsgislib.vectorutils.reproj_vec_lyr_gp(vec_file = file, vec_lyr = basename, 
                  #  epsg_code = 4326, out_vec_file = out_file, out_vec_lyr = basename, 
                   # out_format = 'GPKG')
        

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return ["glas_file", "out_file", "basename"]

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

