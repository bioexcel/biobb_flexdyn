#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
import shutil
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
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
            * **binary_path** (*str*) - ("imc") iMODS imc binary path to be used.
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **num_modes** (*int*) - (5) Number of eigenvectors to be employed
            * **amplitude** (*int*) - (1) Amplitude linear factor to scale motion
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("cmip/cmip:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

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
                 properties: Optional[dict] = None, **kwargs) -> None:

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

        # Determine working directory (host unique_dir or container volume path)
        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get('unique_dir', '')

        # Output temporary file
        # out_file_prefix = Path(self.stage_io_dict.get("unique_dir", "")).joinpath("imod_ensemble")
        # out_file = Path(self.stage_io_dict.get("unique_dir", "")).joinpath("imod_ensemble.pdb")
        out_file_prefix = "imod_ensemble"  # Needed as imod is appending the .pdb extension
        out_file = "imod_ensemble.pdb"

        # Command line
        # imc 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble.pdb -c 500
        # self.cmd = [self.binary_path,
        #             str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
        #             str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
        #             "-o", str(out_file_prefix)
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    PurePath(self.stage_io_dict["in"]["input_pdb_path"]).name,
                    PurePath(self.stage_io_dict["in"]["input_dat_path"]).name,
                    '-o', out_file_prefix
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

        # Rename generated output file to staged output path inside the sandbox.
        # stage_io_dict output paths are container-internal when running in containers.
        generated_output = Path(self.stage_io_dict.get('unique_dir', '')).joinpath(out_file)
        staged_output = Path(self.stage_io_dict.get('unique_dir', '')).joinpath(
            Path(self.stage_io_dict["out"]["output_traj_path"]).name
        )
        shutil.copy2(generated_output, staged_output)

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def imod_imc(input_pdb_path: str, input_dat_path: str, output_traj_path: str,
             properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ImodImc <flexdyn.imod_imc.ImodImc>`flexdyn.imod_imc.ImodImc class and
    execute :meth:`launch() <flexdyn.imod_imc.ImodImc.launch>` method"""
    return ImodImc(**dict(locals())).launch()


imod_imc.__doc__ = ImodImc.__doc__
main = ImodImc.get_main(imod_imc, "Compute a Monte-Carlo IC-NMA based conformational ensemble using the imc tool from the iMODS package.")

if __name__ == '__main__':
    main()
