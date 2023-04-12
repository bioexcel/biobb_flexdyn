#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
import argparse
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger


class ImodImc(BiobbObject):
    """
    | biobb_flexdyn imod_imc
    | Wrapper of the imc tool
    | Compute a Monte-Carlo IC-NMA based conformational ensemble using the imc tool from the iMODS package.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure_cleaned.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_dat_path (str): Input dat with normal modes. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/imod_imode_evecs.dat>`_. Accepted formats: dat (edam:format_1637), txt (edam:format_2330).
        output_traj_path (str): Output multi-model PDB file with the generated ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imc_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **num_modes** (*int*) - (5) Number of eigenvectors to be employed
            * **amplitude** (*int*) - (1) Amplitude linear factor to scale motion
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.imod_imc import imod_imc
            prop = {
                'num_structs' : 500
            }
            imod_imc(   input_pdb_path='/path/to/structure.pdb',
                          input_dat_path='/path/to/input_evecs.dat',
                          output_traj_path='/path/to/output_ensemble.pdb',
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
    def __init__(self, input_pdb_path: str, input_dat_path: str, output_traj_path: str,
                 properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pdb_path': input_pdb_path, 'input_dat_path': input_dat_path},
            'out': {'output_traj_path': output_traj_path}
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'imc')

        self.num_structs = properties.get('num_structs', 500)
        self.num_modes = properties.get('num_modes', 5)
        self.amplitude = properties.get('amplitude', 1.0)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn iMOD imc module."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Output temporary file
        out_file_prefix = Path(self.stage_io_dict.get("unique_dir")).joinpath("imod_ensemble")
        out_file = Path(self.stage_io_dict.get("unique_dir")).joinpath("imod_ensemble.pdb")

        # Command line
        # imc 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble.pdb -c 500
        self.cmd = [self.binary_path,
                    str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
                    str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
                    "-o", str(out_file_prefix)
                    ]

        # Properties
        if self.num_structs:
            self.cmd.append('-c')
            self.cmd.append(str(self.num_structs))

        if self.num_modes:
            self.cmd.append('-n')
            self.cmd.append(str(self.num_modes))

        if self.amplitude:
            self.cmd.append('-a')
            self.cmd.append(str(self.amplitude))

        # Run Biobb block
        self.run_biobb()

        # Copying generated output file to the final (user-given) file name
        shutil.copy2(out_file, self.stage_io_dict["out"]["output_traj_path"])

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def imod_imc(input_pdb_path: str, input_dat_path: str, output_traj_path: str,
             properties: dict = None, **kwargs) -> int:
    """Create :class:`ImodImc <flexdyn.imod_imc.ImodImc>`flexdyn.imod_imc.ImodImc class and
    execute :meth:`launch() <flexdyn.imod_imc.ImodImc.launch>` method"""

    return ImodImc(input_pdb_path=input_pdb_path,
                   input_dat_path=input_dat_path,
                   output_traj_path=output_traj_path,
                   properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Compute a Monte-Carlo IC-NMA based conformational ensemble using the imc tool from the iMODS package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file. Accepted formats: pdb')
    required_args.add_argument('--input_dat_path', required=True, help='Input evecs file. Accepted formats: dat')
    required_args.add_argument('--output_traj_path', required=True, help='Output traj file. Accepted formats: pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    imod_imc(input_pdb_path=args.input_pdb_path,
             input_dat_path=args.input_dat_path,
             output_traj_path=args.output_traj_path,
             properties=properties)


if __name__ == '__main__':
    main()
