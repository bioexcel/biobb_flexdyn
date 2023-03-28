#!/usr/bin/env python3

"""Module containing the concoord_disco class and the command line interface."""
import argparse, os, shutil
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class ConcoordDisco(BiobbObject):
    """
    | biobb_flexdyn ConcoordDisco
    | Wrapper of the Disco tool from the Concoord package.
    | Structure generation based on a set of geometric constraints extracted with the Concoord Dist tool.

    Args:
        input_pdb_path (str): Input structure file in PDB format. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_dat_path (str): Input dat with structure interpretation and bond definitions. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/dist.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        output_traj_path (str): Output trajectory file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_trj.pdb>`_. Accepted formats: pdb (edam:format_1476), xtc (edam:format_3875), gro (edam:format_2033).
        output_rmsd_path (str): Output rmsd file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_rmsd.dat>`_. Accepted formats: dat (edam:format_1637).
        output_bfactor_path (str): Output B-factor file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_bfactor.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("disco") Concoord disco binary path to be used.
            * **vdw** (*int*) - (1) Select a set of Van der Waals parameters. Values: 1 (OPLS-UA -united atoms- parameters), 2 (OPLS-AA -all atoms- parameters), 3 (PROLSQ repel parameters), 4 (Yamber2 parameters), 5 (Li et al. parameters), 6 (OPLS-X parameters -recommended for NMR structure determination-)
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **num_iterations** (*int*) - (2500) Maximum number of iterations per structure
            * **chirality_check** (*int*) - (2) Chirality check. Values: 0 (no chirality checks), 1 (only check afterwards), 2 (check on the fly) 
            * **bs** (*int*) - (0) Number of rounds of triangular bound smoothing (default 0), (if >= 6, tetragonal BS is activated)
            * **nofit** (*bool*) - (False) Do not fit generated structures to reference 
            * **seed** (*int*) - (741265) Initial random seed 
            * **violation** (*float*) - (1.0) Maximal acceptable sum of violations (nm)
            * **nofit** (*bool*) - (False) Do not fit generated structures to reference 
            * **convergence** (*int*) - (50) Consider convergence failed after this number of non-productive iterations
            * **trials** (*int*) - (25) Maximum number of trials per run
            * **damp** (*int*) - (1) Damping factor for distance corrections. Values: 1 (default), 2 (for cases with convergence problems)
            * **dyn** (*int*) - (1) Number of rounds to dynamically set tolerances
            * **bump** (*bool*) - (False) Do extra bump check
            * **pairlist_freq** (*int*) - (10) Pairlist update frequency in steps (only valid together with bump)
            * **cutoff** (*float*) - (0.5) Cut-off radius for pairlist (nm) (only valid together with bump)
            * **ref** (*bool*) - (False) Use input coordinates instead of random starting coordinates
            * **scale** (*int*) - (1) Pre-scale coordinates with this factor 
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.concoord_disco import concoord_disco
            prop = {
                'vdw' : 4,
                'num_structs' : 20
            }
            concoord_disco(     input_pdb_path='/path/to/dist_input.pdb',
                                input_dat_path='/path/to/dist_input.dat',
                                output_traj_path='/path/to/disco_out_traj.pdb',
                                output_rmsd_path='/path/to/disco_out_rmsd.dat',
                                output_bfactor_path='/path/to/disco_out_bfactor.pdb',
                                properties=prop)

    Info:
        * wrapped_software:
            * name: Concoord 
            * version: >=2.1.2
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pdb_path: str, input_dat_path: str, output_traj_path: str,
    output_rmsd_path: str, output_bfactor_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path,
                    'input_dat_path': input_dat_path,
             },
            'out': {    'output_traj_path': output_traj_path,
                        'output_rmsd_path': output_rmsd_path,
                        'output_bfactor_path': output_bfactor_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'disco')

        self.vdw = properties.get('vdw')
        self.num_structs = properties.get('num_structs')
        self.num_iterations = properties.get('num_iterations')
        self.chirality_check = properties.get('chirality_check')
        self.bs = properties.get('bs')
        self.nofit = properties.get('nofit')
        self.seed = properties.get('seed')
        self.violation = properties.get('violation')
        self.convergence = properties.get('convergence')
        self.trials = properties.get('trials')
        self.damp = properties.get('damp')
        self.dyn = properties.get('dyn')
        self.bump = properties.get('bump')
        self.pairlist_freq = properties.get('pairlist_freq')
        self.cutoff = properties.get('cutoff')
        self.ref = properties.get('ref')
        self.scale = properties.get('scale')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn ConcoordDisco module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Copy auxiliary files (MARGINS, ATOMS, BONDS) according to the VdW property to the working dir 
        concoord_lib = os.getenv("CONCOORDLIB")

        # MARGINS_li.DAT, MARGINS_oplsaa.DAT, MARGINS_oplsua.DAT, MARGINS_oplsx.DAT, MARGINS_repel.DAT, MARGINS_yamber2.DAT
        # 1 (OPLS-UA -united atoms- parameters), 2 (OPLS-AA -all atoms- parameters), 3 (PROLSQ repel parameters), 4 (Yamber2 parameters), 5 (Li et al. parameters), 6 (OPLS-X parameters -recommended for NMR structure determination-).
        vdw_values = ["vdw_values","oplsua","oplsaa","repel","yamber2","li","oplsx"]
        margins_file = concoord_lib + "/MARGINS_" + vdw_values[self.vdw] + ".DAT"
        atoms_file = concoord_lib + "/ATOMS_" + vdw_values[self.vdw] + ".DAT"
        bonds_file = concoord_lib + "/BONDS.DAT"
        shutil.copy2(margins_file, self.stage_io_dict.get("unique_dir"))
        shutil.copy2(margins_file, self.stage_io_dict.get("unique_dir")+"/MARGINS.DAT")
        shutil.copy2(atoms_file, self.stage_io_dict.get("unique_dir"))
        shutil.copy2(bonds_file, self.stage_io_dict.get("unique_dir"))

        # Command line
        # (concoord) OROZCO67:biobb_flexdyn hospital$ disco -d biobb_flexdyn/test/reference/flexdyn/dist.dat 
        # -p biobb_flexdyn/test/reference/flexdyn/dist.pdb  -op patata.pdb 
        self.cmd = ["cd ", self.stage_io_dict.get('unique_dir'), ";", self.binary_path, 
 #               "-p", str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
 #               "-d", str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
 #               "-or", str(Path(self.stage_io_dict["out"]["output_rmsd_path"]).relative_to(Path.cwd())),
 #               "-of", str(Path(self.stage_io_dict["out"]["output_bfactor_path"]).relative_to(Path.cwd()))
                "-p", str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))),
                "-d", str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))),
                "-or", str(Path(self.stage_io_dict["out"]["output_rmsd_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))),
                "-of", str(Path(self.stage_io_dict["out"]["output_bfactor_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir'))))
                ]

        # Output structure formats:
        file_extension = Path(self.stage_io_dict["out"]["output_traj_path"]).suffix
        if file_extension == ".pdb":
            self.cmd.append('-on') # NMR-PDB format (multi-model)
#            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path.cwd())))
            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))))
        elif file_extension == ".gro":
            self.cmd.append('-ot')
#            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path.cwd())))
            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))))
        elif file_extension == ".xtc":
            self.cmd.append('-ox')
#            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path.cwd())))
            self.cmd.append(str(Path(self.stage_io_dict["out"]["output_traj_path"]).relative_to(Path(self.stage_io_dict.get('unique_dir')))))
        else:
            fu.log("ERROR: output_traj_path ({}) must be a PDB, GRO or XTC formatted file ({})".format(self.io_dict["out"]["output_traj_path"], file_extension), self.out_log, self.global_log)
        
        # Properties
        if self.num_structs:
            self.cmd.append('-n')
            self.cmd.append(str(self.num_structs))

        if self.num_iterations:
            self.cmd.append('-i')
            self.cmd.append(str(self.num_iterations))

        if self.chirality_check:
            self.cmd.append('-c')
            self.cmd.append(str(self.chirality_check))

        if self.bs:
            self.cmd.append('-bs')
            self.cmd.append(str(self.bs))

        if self.cutoff:
            self.cmd.append('-rc')
            self.cmd.append(str(self.cutoff))

        if self.seed:
            self.cmd.append('-s')
            self.cmd.append(str(self.seed))

        if self.damp:
            self.cmd.append('-damp')
            self.cmd.append(str(self.damp))

        if self.violation:
            self.cmd.append('-viol')
            self.cmd.append(str(self.violation))

        if self.convergence:
            self.cmd.append('-con')
            self.cmd.append(str(self.convergence))

        if self.trials:
            self.cmd.append('-t')
            self.cmd.append(str(self.trials))

        if self.dyn:
            self.cmd.append('-dyn')
            self.cmd.append(str(self.dyn))

        if self.pairlist_freq:
            self.cmd.append('-l')
            self.cmd.append(str(self.pairlist_freq))

        if self.scale:
            self.cmd.append('-is')
            self.cmd.append(str(self.scale))

        if self.nofit:
            self.cmd.append('-f')

        if self.bump:
            self.cmd.append('-bump')

        if self.ref:
            self.cmd.append('-ref')

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def concoord_disco(input_pdb_path: str, input_dat_path: str,
            output_traj_path: str, output_rmsd_path: str, output_bfactor_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`ConcoordDisco <flexdyn.concoord_disco.ConcoordDisco>`flexdyn.concoord_disco.ConcoordDisco class and
    execute :meth:`launch() <flexdyn.concoord_disco.ConcoordDisco.launch>` method"""

    return ConcoordDisco(   input_pdb_path=input_pdb_path,
                            input_dat_path=input_dat_path,
                            output_traj_path=output_traj_path,
                            output_rmsd_path=output_rmsd_path,
                            output_bfactor_path=output_bfactor_path,
                            properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Structure generation based on a set of geometric constraints extracted with the Concoord Dist tool.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file in PDB format. Accepted formats: pdb')
    required_args.add_argument('--input_dat_path', required=True, help='Input dat with structure interpretation and bond definitions. Accepted formats: dat, txt')
    required_args.add_argument('--output_traj_path', required=True, help='Output trajectory file. Accepted formats: pdb, gro, xtc.')
    required_args.add_argument('--output_rmsd_path', required=True, help='Output RMSd file. Accepted formats: dat.')
    required_args.add_argument('--output_bfactor_path', required=True, help='Output B-factor file. Accepted formats: pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    concoord_disco( input_pdb_path=args.input_pdb_path,
                    input_dat_path=args.input_dat_path,
                    output_traj_path=args.output_traj_path,
                    output_rmsd_path=args.output_rmsd_path,
                    output_bfactor_path=args.output_bfactor_path,
                    properties=properties)

if __name__ == '__main__':
    main()
