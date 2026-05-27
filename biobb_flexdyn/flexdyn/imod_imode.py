#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
import shutil
from pathlib import Path, PurePath
from biobb_common.generic.biobb_object import BiobbObject
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
            * **binary_path** (*str*) - ("imode_gcc") iMODS imode binary path to be used.
            * **cg** (*int*) - (2) Coarse-Grained model. Values: 0 (CA), 1 (C5), 2 (Heavy atoms).
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
                 properties: Optional[dict] = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pdb_path': input_pdb_path},
            'out': {'output_dat_path': output_dat_path}
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
        if self.check_restart():
            return 0
        self.stage_files()

        # Determine working directory (host unique_dir or container volume path)
        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get('unique_dir', '')

        # Output temporary file
        # out_file_prefix = Path(self.stage_io_dict.get("unique_dir", "")).joinpath("imods_evecs")
        # out_file = Path(self.stage_io_dict.get("unique_dir", "")).joinpath("imods_evecs_ic.evec")
        out_file_prefix = "imods_evecs"  # Needed as imod is appending the _ic.evec extension
        out_file = "imods_evecs_ic.evec"

        # Command line
        # imode_gcc  1ake_backbone.pdb -m 0 -o patata.evec
        # self.cmd = [self.binary_path,
        #             str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
        #             "-o", str(out_file_prefix),
        #             "-m", str(self.cg)
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    PurePath(self.stage_io_dict["in"]["input_pdb_path"]).name,
                    '-o', out_file_prefix,
                    '-m', str(self.cg)
                    ]

        # Run Biobb block
        self.run_biobb()

        # Rename generated output file to staged output path inside the sandbox.
        # stage_io_dict output paths are container-internal when running in containers.
        generated_output = Path(self.stage_io_dict.get('unique_dir', '')).joinpath(out_file)
        staged_output = Path(self.stage_io_dict.get('unique_dir', '')).joinpath(
            Path(self.stage_io_dict["out"]["output_dat_path"]).name
        )
        shutil.copy2(generated_output, staged_output)

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def imod_imode(input_pdb_path: str, output_dat_path: str,
               properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ImodImode <flexdyn.imod_imode.ImodImode>`flexdyn.imod_imode.ImodImode class and
    execute :meth:`launch() <flexdyn.imod_imode.ImodImode.launch>` method"""
    return ImodImode(**dict(locals())).launch()


imod_imode.__doc__ = ImodImode.__doc__
main = ImodImode.get_main(imod_imode, "Compute the normal modes of a macromolecule using the imode tool from the iMODS package.")

if __name__ == '__main__':
    main()
