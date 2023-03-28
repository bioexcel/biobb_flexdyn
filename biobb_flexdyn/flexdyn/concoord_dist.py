#!/usr/bin/env python3

"""Module containing the concoord_dist class and the command line interface."""
import argparse
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

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
            * **bond_angle** (*int*) - (1) Select a set of bond/angle parameters. Values: 1 (Concoord default parameters), 2 (Engh-Huber parameters).
            * **retain_hydrogens** (*bool*) - (False) Retain hydrogen atoms
            * **nb_interactions** (*bool*) - (False) Try to find alternatives for non-bonded interactions (by default the native contacts will be preserved)
            * **cutoff** (*float*) - (4.0) cut-off radius (Angstroms) for non-bonded interacting pairs (the cut-off distances are additional to the sum of VDW radii)
            * **min_distances** (*int*) - (50) Minimum number of distances to be defined for each atom 
            * **damp** (*float*) - (1.0) Multiply each distance margin by this value
            * **fixed_atoms** (*bool*) - (False) Interpret zero occupancy as atoms to keep fixed 
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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
    output_gro_path: str, output_dat_path: str, properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_structure_path': input_structure_path },
            'out': {    'output_pdb_path': output_pdb_path,
                        'output_gro_path': output_gro_path,
                        'output_dat_path': output_dat_path
            }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'dist')
        self.retain_hydrogens = properties.get('retain_hydrogens', False)
        self.nb_interactions = properties.get('nb_interactions', False)
        self.cutoff = properties.get('cutoff', 4.0)
        self.min_distances = properties.get('min_distances', 50)
        self.damp = properties.get('damp', 1.0)
        self.fixed_atoms = properties.get('fixed_atoms', False)

        self.vdw = properties.get('vdw', 1)
        self.bond_angle = properties.get('bond_angle', 1)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn ConcoordDist module."""

        # Set input params
        self.io_dict['in']['stdin_file_path'] = fu.create_stdin_file(f'{self.vdw}\n{self.bond_angle}\n')

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Command line
        # (concoord) OROZCO67:biobb_flexdyn hospital$ dist -p biobb_flexdyn/test/data/flexdyn/structure.pdb 
        # -op dist.pdb -og dist.gro -od dist.dat 
        # Select a set of Van der Waals parameters:
        # 1: OPLS-UA (united atoms) parameters
        # 2: OPLS-AA (all atoms) parameters
        # 3: PROLSQ repel parameters
        # 4: Yamber2 parameters
        # 5: Li et al. parameters
        # 6: OPLS-X parameters (recommended for NMR structure determination)
        # 2
        # Selected parameter set 2
        # copying /opt/anaconda3/envs/concoord/share/concoord/lib/ATOMS_oplsaa.DAT to ATOMS.DAT in current working directory
        # copying /opt/anaconda3/envs/concoord/share/concoord/lib/MARGINS_oplsaa.DAT to MARGINS.DAT in current working directory
        # Select a set of bond/angle parameters:
        # 1: Concoord default parameters
        # 2: Engh-Huber parameters
        # 1
        # Selected parameter set 1
        # copying /opt/anaconda3/envs/concoord/share/concoord/lib/BONDS.DAT.noeh to BONDS.DAT in current working directory

        self.cmd = [self.binary_path, 
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

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            self.io_dict['in'].get("stdin_file_path")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def concoord_dist(input_structure_path: str,
            output_pdb_path: str, output_gro_path: str, output_dat_path: str,
            properties: dict = None, **kwargs) -> int:
    """Create :class:`ConcoordDist <flexdyn.concoord_dist.ConcoordDist>`flexdyn.concoord_dist.ConcoordDist class and
    execute :meth:`launch() <flexdyn.concoord_dist.ConcoordDist.launch>` method"""

    return ConcoordDist(    input_structure_path=input_structure_path,
                            output_pdb_path=output_pdb_path,
                            output_gro_path=output_gro_path,
                            output_dat_path=output_dat_path,
                            properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Structure interpretation and bond definitions from a PDB/GRO file.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_structure_path', required=True, help='Input structure file. Accepted formats: pdb, gro.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output pdb file. Accepted formats: pdb.')
    required_args.add_argument('--output_gro_path', required=True, help='Output gro file. Accepted formats: gro.')
    required_args.add_argument('--output_dat_path', required=True, help='Output dat file with structure interpretation and bond definitions. Accepted formats: dat, txt.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    concoord_dist(  input_structure_path=args.input_structure_path,
                    output_pdb_path=args.output_pdb_path,
                    output_gro_path=args.output_gro_path,
                    output_dat_path=args.output_dat_path,
                    properties=properties)

if __name__ == '__main__':
    main()
