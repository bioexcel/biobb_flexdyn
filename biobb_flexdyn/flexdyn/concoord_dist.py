#!/usr/bin/env python3

"""Module containing the concoord_dist class and the command line interface."""
from typing import Optional
import shutil
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_flexdyn.flexdyn.common import concoord_lib


class ConcoordDist(BiobbObject):
    """
    | biobb_flexdyn ConcoordDist
    | Wrapper of the Dist tool from the Concoord package.
    | Structure interpretation and bond definitions from a PDB/GRO file.

    Args:
        input_structure_path (str): Input structure file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_pdb_path (str): Output pdb file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_gro_path (str): Output gro file. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.gro>`_. Accepted formats: gro (edam:format_2033).
        output_dat_path (str): Output dat with structure interpretation and bond definitions. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("dist") Concoord dist binary path to be used.
            * **vdw** (*int*) - (1) Select a set of Van der Waals parameters. Values: 1 (OPLS-UA -united atoms- parameters), 2 (OPLS-AA -all atoms- parameters), 3 (PROLSQ repel parameters), 4 (Yamber2 parameters), 5 (Li et al. parameters), 6 (OPLS-X parameters -recommended for NMR structure determination-).
            * **concoord_lib_path** (*str*) - (None) Path to Concoord library files. If not specified will look for CONCOORDLIB conda environment variable.
            * **bond_angle** (*int*) - (1) Select a set of bond/angle parameters. Values: 1 (Concoord default parameters), 2 (Engh-Huber parameters).
            * **retain_hydrogens** (*bool*) - (False) Retain hydrogen atoms
            * **nb_interactions** (*bool*) - (False) Try to find alternatives for non-bonded interactions (by default the native contacts will be preserved)
            * **cutoff** (*float*) - (4.0) cut-off radius (Angstroms) for non-bonded interacting pairs (the cut-off distances are additional to the sum of VDW radii)
            * **min_distances** (*int*) - (50) Minimum number of distances to be defined for each atom
            * **damp** (*float*) - (1.0) Multiply each distance margin by this value
            * **fixed_atoms** (*bool*) - (False) Interpret zero occupancy as atoms to keep fixed
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - (None) Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.concoord_dist import concoord_dist
            prop = {
                'vdw' : 4,
                'bond_angle' : 1
            }
            concoord_dist(  input_structure_path='/path/to/structure.pdb',
                            output_pdb_path='/path/to/output.pdb',
                            output_gro_path='/path/to/output.gro',
                            output_dat_path='/path/to/output.dat',
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

    def __init__(self, input_structure_path: str, output_pdb_path: str,
                 output_gro_path: str, output_dat_path: str, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def prepare(self) -> None:
        """Find the CONCOORD library folder and create the stdin file with the input parameters."""
        self.concoord_lib_dir = concoord_lib(self.concoord_lib_path)
        # Set input params
        self.io_dict['in']['stdin_file_path'] = fu.create_stdin_file(f'{self.vdw}\n{self.bond_angle}\n')

    def run(self):
        """Launches the execution of the FlexDyn ConcoordDist module."""

        # Copy auxiliary file (HBONDS) to the working dir
        shutil.copy2(self.concoord_lib_dir / "HBONDS.DAT", self.stage_io_dict["unique_dir"])

        # Command line
        # dist -p structure.pdb -op dist.pdb -og dist.gro -od dist.dat
        # dist asks for the VdW parameter set and then for the bond/angle set: the stdin file of prepare() answers both

        self.cmd = [
            self.binary_path,
            "-op", self.stage_io_dict["out"]["output_pdb_path"],
            "-og", self.stage_io_dict["out"]["output_gro_path"],
            "-od", self.stage_io_dict["out"]["output_dat_path"]
        ]
        # If input structure in pdb format:
        file_extension = Path(self.stage_io_dict["in"]["input_structure_path"]).suffix
        if file_extension == ".pdb":
            self.cmd.append('-p')
            self.cmd.append(self.stage_io_dict["in"]["input_structure_path"])

        elif file_extension == ".gro":
            self.cmd.append('-g')
            self.cmd.append(self.stage_io_dict["in"]["input_structure_path"])

        else:
            fu.log("ERROR: input_structure_path ({}) must be a PDB or a GRO formatted file ({})".format(self.io_dict["in"]["input_structure_path"], file_extension), self.out_log, self.global_log)
            raise ValueError("input_structure_path ({}) must be a PDB or a GRO formatted file".format(self.io_dict["in"]["input_structure_path"]))

        if self.retain_hydrogens:
            self.cmd.append('-r')

        if self.nb_interactions:
            self.cmd.append('-nb')

        if self.fixed_atoms:
            self.cmd.append('-q')

        if self.cutoff:
            self.cmd.append('-c')
            self.cmd.append(str(self.cutoff))

        if self.min_distances:
            self.cmd.append('-m')
            self.cmd.append(str(self.min_distances))

        if self.damp:
            self.cmd.append('-damp')
            self.cmd.append(str(self.damp))

        # Add stdin input file
        self.cmd.append('<')
        self.cmd.append(self.stage_io_dict["in"]["stdin_file_path"])

        # Run Biobb block
        self.run_biobb()

        # remove temporary folder(s)
        self.tmp_files.append(self.io_dict['in'].get("stdin_file_path", ""))


concoord_dist = launcher(ConcoordDist)

if __name__ == '__main__':
    ConcoordDist.main()
