#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexDyn iMOD imove module."""

        # Command line
        # imove 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble.pdb 1 -c 500
        self.cmd = [self.binary_path,
                    self.stage_io_dict["in"]["input_pdb_path"],
                    self.stage_io_dict["in"]["input_dat_path"],
                    self.stage_io_dict["out"]["output_pdb_path"],
                    str(self.pc)
                    ]

        # Properties
        if self.num_frames:
            self.cmd.append('-c')
            self.cmd.append(str(self.num_frames))

        # Run Biobb block
        self.run_biobb()


imod_imove = launcher(ImodImove)

if __name__ == '__main__':
    ImodImove.main()
