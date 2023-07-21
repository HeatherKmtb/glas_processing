import logging
import os
import glob
import rsgislib
import rsgislib.vectorattrs

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):

        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        glas_files = glob.glob(kwargs['glas_tiles'])

        for glas_file in glas_files:
            basename = self.get_file_basename(glas_file)
            out_file = os.path.join(kwargs['out_dir'], f'{basename}.gpkg')            

            if (not os.path.exists(out_file)):
                c_dict = dict()
                c_dict['glas_file'] = glas_file
                c_dict['out_file'] = out_file
                c_dict['wwf'] = 
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            glas_tiles="/bigdata/cci_biomass_data/WCM/1_deg/grid_files_renamed/grid",
            out_dir="/bigdata/cci_biomass_data/WCM/1_deg/eco/renamed_07.23")

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=10,  # The number of cores to use for analysis.
            db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "ProcessCmd"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/heather/pbpt_conn.txt",
        lock_file_path="./pbpt_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()

