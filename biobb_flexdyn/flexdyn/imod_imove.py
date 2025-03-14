#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
import argparse
from typing import Optional
import shutil
from pathlib import PurePath
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
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
            * **num_frames** (*int*) - (11) Number of frames to be generated
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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
                 properties: Optional[dict] = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pdb_path': input_pdb_path, 'input_dat_path': input_dat_path},
            'out': {'output_pdb_path': output_pdb_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'imove')

        self.pc = properties.get('pc', 1)
        self.num_frames = properties.get('num_frames', 11)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn iMOD imove module."""

        # Setup Biobb
        if self.check_restart():
            return 0
        # self.stage_files()

        # Manually creating a Sandbox to avoid issues with input parameters buffer overflow:
        #   Long strings defining a file path makes Fortran or C compiled programs crash if the string
        #   declared is shorter than the input parameter path (string) length.
        #   Generating a temporary folder and working inside this folder (sandbox) fixes this problem.
        #   The problem was found in Galaxy executions, launching Singularity containers (May 2023).

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        shutil.copy2(self.io_dict["in"]["input_pdb_path"], self.tmp_folder)
        shutil.copy2(self.io_dict["in"]["input_dat_path"], self.tmp_folder)

        # Command line
        # imove 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble.pdb 1 -c 500
        # self.cmd = [self.binary_path,
        #             str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
        #             str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
        #             str(Path(self.stage_io_dict["out"]["output_pdb_path"]).relative_to(Path.cwd())),
        #             str(self.pc)
        #             ]

        self.cmd = ['cd', self.tmp_folder, ';',
                    self.binary_path,
                    PurePath(self.io_dict["in"]["input_pdb_path"]).name,
                    PurePath(self.io_dict["in"]["input_dat_path"]).name,
                    PurePath(self.io_dict["out"]["output_pdb_path"]).name,
                    str(self.pc)
                    ]

        # Properties
        if self.num_frames:
            self.cmd.append('-c')
            self.cmd.append(str(self.num_frames))

        # Run Biobb block
        self.run_biobb()

        # Copy outputs from temporary folder to output path
        shutil.copy2(PurePath(self.tmp_folder).joinpath(PurePath(self.io_dict["out"]["output_pdb_path"]).name), PurePath(self.io_dict["out"]["output_pdb_path"]))

        # Copy files to host
        # self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            # self.stage_io_dict.get("unique_dir", "")
            self.tmp_folder
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def imod_imove(input_pdb_path: str, input_dat_path: str, output_pdb_path: str,
               properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ImodImove <flexdyn.imod_imove.ImodImove>`flexdyn.imod_imove.ImodImove class and
    execute :meth:`launch() <flexdyn.imod_imove.ImodImove.launch>` method"""

    return ImodImove(input_pdb_path=input_pdb_path,
                     input_dat_path=input_dat_path,
                     output_pdb_path=output_pdb_path,
                     properties=properties).launch()

    imod_imove.__doc__ = ImodImove.__doc__


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
    imod_imove(input_pdb_path=args.input_pdb_path,
               input_dat_path=args.input_dat_path,
               output_pdb_path=args.output_pdb_path,
               properties=properties)


if __name__ == '__main__':
    main()
