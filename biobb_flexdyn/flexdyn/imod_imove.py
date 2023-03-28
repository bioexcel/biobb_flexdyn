#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
import argparse
import shutil
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class ImodImove(BiobbObject):
    """
    | biobb_flexdyn imod_imove
    | Wrapper of the imove tool 
    | Compute the normal modes of a macromolecule using the imove tool from the iMODS package.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure_cleaned.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_dat_path (str): Input dat with normal modes. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/imod_imode_evecs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        output_pdb_path (str): Output multi-model PDB file with the generated animation by Principal Component. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imove_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **pc** (*int*) - (1) Principal Component.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist. 

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.imod_imove import imod_imove
            prop = {
                'pc' : 1
            }
            imod_imove(   input_pdb_path='/path/to/structure.pdb',
                          input_dat_path='/path/to/input_evecs.dat',
                          output_pdb_path='/path/to/output_anim.pdb',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: iMODS 
            * version: >=1.0.4
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """
    def __init__(self, input_pdb_path: str, input_dat_path: str, output_pdb_path: str,
    properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path, 'input_dat_path': input_dat_path, },
            'out': { 'output_pdb_path': output_pdb_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'imove')

        self.pc = properties.get('pc', 1)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn iMOD imove module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Output temporary file
        out_file_prefix = Path(self.stage_io_dict.get("unique_dir")).joinpath("imods_pc") 
        out_file = Path(self.stage_io_dict.get("unique_dir")).joinpath("imods_pc_ic.pdb") 

        # Command line
        # imode_gcc  1ake_backbone.pdb -m 0 -o patata.evec
        self.cmd = [self.binary_path, 
                str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
                str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
                str(Path(self.stage_io_dict["out"]["output_pdb_path"]).relative_to(Path.cwd())),
                str(self.pc)
                ]

        # Run Biobb block
        self.run_biobb()

        # Copying generated output file to the final (user-given) file name
        #shutil.copy2(out_file, self.stage_io_dict["out"]["output_dat_path"])

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def imod_imove(input_pdb_path: str, input_dat_path: str, output_pdb_path: str, 
            properties: dict = None, **kwargs) -> int:
    """Create :class:`ImodImove <flexdyn.imod_imove.ImodImove>`flexdyn.imod_imove.ImodImove class and
    execute :meth:`launch() <flexdyn.imod_imove.ImodImove.launch>` method"""

    return ImodImove(   input_pdb_path=input_pdb_path,
                        input_dat_path=input_dat_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Animate the normal modes of a macromolecule using the imove tool from the iMODS package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file. Accepted formats: pdb')
    required_args.add_argument('--input_dat_path', required=True, help='Input evecs file. Accepted formats: dat')
    required_args.add_argument('--output_pdb_path', required=True, help='Output pdb file. Accepted formats: pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    imod_imove(  input_pdb_path=args.input_pdb_path,
            input_dat_path=args.input_dat_path,
            output_pdb_path=args.output_pdb_path,
            properties=properties)

if __name__ == '__main__':
    main()
