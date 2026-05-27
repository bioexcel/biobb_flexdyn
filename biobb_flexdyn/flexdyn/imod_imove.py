#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
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
            * **binary_path** (*str*) - ("imove") iMODS imove binary path to be used.
            * **pc** (*int*) - (1) Principal Component.
            * **num_frames** (*int*) - (11) Number of frames to be generated
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
        self.stage_files()

        # Determine working directory (host unique_dir or container volume path)
        if self.container_path:
            working_dir = self.container_volume_path if self.container_volume_path else "/data"
        else:
            working_dir = self.stage_io_dict.get('unique_dir', '')

        # Command line
        # imove 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble.pdb 1 -c 500
        # self.cmd = [self.binary_path,
        #             str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
        #             str(Path(self.stage_io_dict["in"]["input_dat_path"]).relative_to(Path.cwd())),
        #             str(Path(self.stage_io_dict["out"]["output_pdb_path"]).relative_to(Path.cwd())),
        #             str(self.pc)
        #             ]

        self.cmd = ['cd', working_dir, ';',
                    self.binary_path,
                    PurePath(self.stage_io_dict["in"]["input_pdb_path"]).name,
                    PurePath(self.stage_io_dict["in"]["input_dat_path"]).name,
                    PurePath(self.stage_io_dict["out"]["output_pdb_path"]).name,
                    str(self.pc)
                    ]

        # Properties
        if self.num_frames:
            self.cmd.append('-c')
            self.cmd.append(str(self.num_frames))

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def imod_imove(input_pdb_path: str, input_dat_path: str, output_pdb_path: str,
               properties: Optional[dict] = None, **kwargs) -> int:
    """Create :class:`ImodImove <flexdyn.imod_imove.ImodImove>`flexdyn.imod_imove.ImodImove class and
    execute :meth:`launch() <flexdyn.imod_imove.ImodImove.launch>` method"""
    return ImodImove(**dict(locals())).launch()


imod_imove.__doc__ = ImodImove.__doc__
main = ImodImove.get_main(imod_imove, "Animate the normal modes of a macromolecule using the imove tool from the iMODS package.")

if __name__ == '__main__':
    main()
