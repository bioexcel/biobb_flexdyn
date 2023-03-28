#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
import argparse
import shutil
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class ImodImode(BiobbObject):
    """
    | biobb_flexdyn imod_imode
    | Wrapper of the imode tool 
    | Compute the normal modes of a macromolecule using the imode tool from the iMODS package.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_dat_path (str): Output dat with normal modes. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imode_evecs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **cg** (*int*) - (2) Coarse-Grained model. Values: 0 (CA), 1 (C5), 2 (Heavy atoms).
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist. 

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.imod_imode import imod_imode
            prop = {
                'cg' : 2
            }
            imod_imode(   input_pdb_path='/path/to/structure.pdb',
                    output_dat_path='/path/to/output_evecs.dat',
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
    def __init__(self, input_pdb_path: str, output_dat_path: str,
    properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path },
            'out': { 'output_dat_path': output_dat_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'imode_gcc')

        self.cg = properties.get('cg', 2)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn iMOD imode module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Output temporary file
        out_file_prefix = Path(self.stage_io_dict.get("unique_dir")).joinpath("imods_evecs") 
        out_file = Path(self.stage_io_dict.get("unique_dir")).joinpath("imods_evecs_ic.evec") 

        # Command line
        # imode_gcc  1ake_backbone.pdb -m 0 -o patata.evec
        self.cmd = [self.binary_path, 
                str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
                "-o", str(out_file_prefix),
                "-m", str(self.cg) 
                ]

        # Run Biobb block
        self.run_biobb()

        # Copying generated output file to the final (user-given) file name
        shutil.copy2(out_file, self.stage_io_dict["out"]["output_dat_path"])

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def imod_imode(input_pdb_path: str, output_dat_path: str, 
            properties: dict = None, **kwargs) -> int:
    """Create :class:`ImodImode <flexdyn.imod_imode.ImodImode>`flexdyn.imod_imode.ImodImode class and
    execute :meth:`launch() <flexdyn.imod_imode.ImodImode.launch>` method"""

    return ImodImode(    input_pdb_path=input_pdb_path,
                        output_dat_path=output_dat_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Compute the normal modes of a macromolecule using the imode tool from the iMODS package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file. Accepted formats: pdb')
    required_args.add_argument('--output_dat_path', required=True, help='Output evecs dat file. Accepted formats: dat.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    imod_imode(  input_pdb_path=args.input_pdb_path,
            output_dat_path=args.output_dat_path,
            properties=properties)

if __name__ == '__main__':
    main()
