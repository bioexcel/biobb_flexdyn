#!/usr/bin/env python3

"""Module containing the concoord_disco class and the command line interface."""
from typing import Optional
import shutil
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_flexdyn.flexdyn.common import concoord_lib


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
            * **concoord_lib_path** (*str*) - (None) Path to Concoord library files. If not specified will look for CONCOORDLIB conda environment variable.
            * **num_structs** (*int*) - (None) Number of structures to be generated. If not set, CONCOORD uses 500.
            * **num_iterations** (*int*) - (None) Maximum number of iterations per structure. If not set, CONCOORD uses 2500.
            * **chirality_check** (*int*) - (None) Chirality check. If not set, CONCOORD uses 2. Values: 0 (no chirality checks), 1 (only check afterwards), 2 (check on the fly)
            * **bs** (*int*) - (None) Number of rounds of triangular bound smoothing (default 0), (if >= 6, tetragonal BS is activated). If not set, CONCOORD uses 0.
            * **nofit** (*bool*) - (False) Do not fit generated structures to reference
            * **seed** (*int*) - (None) Initial random seed. If not set, CONCOORD uses 741265.
            * **violation** (*float*) - (None) Maximal acceptable sum of violations (nm). If not set, CONCOORD uses 1.0.
            * **nofit** (*bool*) - (False) Do not fit generated structures to reference
            * **convergence** (*int*) - (None) Consider convergence failed after this number of non-productive iterations. If not set, CONCOORD uses 500.
            * **trials** (*int*) - (None) Maximum number of trials per run. If not set, CONCOORD uses 25.
            * **damp** (*int*) - (None) Damping factor for distance corrections. If not set, CONCOORD uses 1. Values: 1 (default), 2 (for cases with convergence problems)
            * **dyn** (*int*) - (None) Number of rounds to dynamically set tolerances. If not set, CONCOORD uses 0.
            * **bump** (*bool*) - (False) Do extra bump check
            * **pairlist_freq** (*int*) - (None) Pairlist update frequency in steps (only valid together with bump). If not set, CONCOORD uses 10.
            * **cutoff** (*float*) - (None) Cut-off radius for pairlist (nm) (only valid together with bump). If not set, CONCOORD uses 0.5.
            * **ref** (*bool*) - (False) Use input coordinates instead of random starting coordinates
            * **scale** (*int*) - (None) Pre-scale coordinates with this factor. If not set, CONCOORD uses 1.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("cmip/cmip:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

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
                 output_rmsd_path: str, output_bfactor_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def prepare(self) -> None:
        """Find the CONCOORD library folder and check the vdw property."""
        self.concoord_lib_dir = concoord_lib(self.concoord_lib_path)
        if self.vdw is None:
            raise ValueError("The 'vdw' property cannot be None")

    def run(self):
        """Launches the execution of the FlexDyn ConcoordDisco module."""

        # Copy auxiliary files (MARGINS, ATOMS, BONDS) according to the VdW property to the working dir
        # MARGINS_li.DAT, MARGINS_oplsaa.DAT, MARGINS_oplsua.DAT, MARGINS_oplsx.DAT, MARGINS_repel.DAT, MARGINS_yamber2.DAT
        # 1 (OPLS-UA -united atoms- parameters), 2 (OPLS-AA -all atoms- parameters), 3 (PROLSQ repel parameters), 4 (Yamber2 parameters), 5 (Li et al. parameters), 6 (OPLS-X parameters -recommended for NMR structure determination-).
        vdw_values = ["vdw_values", "oplsua", "oplsaa", "repel", "yamber2", "li", "oplsx"]
        vdw_name = vdw_values[int(self.vdw)]
        sandbox = self.stage_io_dict["unique_dir"]
        margins_file = self.concoord_lib_dir / f"MARGINS_{vdw_name}.DAT"
        shutil.copy2(margins_file, sandbox)
        shutil.copy2(margins_file, Path(sandbox, "MARGINS.DAT"))
        shutil.copy2(self.concoord_lib_dir / f"ATOMS_{vdw_name}.DAT", sandbox)
        shutil.copy2(self.concoord_lib_dir / "BONDS.DAT", sandbox)

        # Command line
        # (concoord) OROZCO67:biobb_flexdyn hospital$ disco -d biobb_flexdyn/test/reference/flexdyn/dist.dat
        # -p biobb_flexdyn/test/reference/flexdyn/dist.pdb  -op patata.pdb
        self.cmd = [self.binary_path,
                    "-p", self.stage_io_dict["in"]["input_pdb_path"],
                    "-d", self.stage_io_dict["in"]["input_dat_path"],
                    "-or", self.stage_io_dict["out"]["output_rmsd_path"],
                    "-of", self.stage_io_dict["out"]["output_bfactor_path"]
                    ]

        # Output structure formats:
        file_extension = Path(self.stage_io_dict["out"]["output_traj_path"]).suffix
        if file_extension == ".pdb":
            self.cmd.append('-on')  # NMR-PDB format (multi-model)
            self.cmd.append(self.stage_io_dict["out"]["output_traj_path"])
        elif file_extension == ".gro":
            self.cmd.append('-ot')
            self.cmd.append(self.stage_io_dict["out"]["output_traj_path"])
        elif file_extension == ".xtc":
            self.cmd.append('-ox')
            self.cmd.append(self.stage_io_dict["out"]["output_traj_path"])
        else:
            fu.log("ERROR: output_traj_path ({}) must be a PDB, GRO or XTC formatted file ({})".format(self.io_dict["out"]["output_traj_path"], file_extension), self.out_log, self.global_log)
            raise ValueError("output_traj_path ({}) must be a PDB, GRO or XTC formatted file".format(self.io_dict["out"]["output_traj_path"]))

        # Properties
        if self.num_structs:
            self.cmd.append('-n')
            self.cmd.append(str(self.num_structs))

        if self.num_iterations:
            self.cmd.append('-i')
            self.cmd.append(str(self.num_iterations))

        if self.chirality_check is not None:
            self.cmd.append('-c')
            self.cmd.append(str(self.chirality_check))

        if self.bs:
            self.cmd.append('-bs')
            self.cmd.append(str(self.bs))

        if self.cutoff:
            self.cmd.append('-rc')
            self.cmd.append(str(self.cutoff))

        if self.seed is not None:
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


concoord_disco = launcher(ConcoordDisco)

if __name__ == '__main__':
    ConcoordDisco.main()
