#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
import os
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexDyn iMOD imode module."""

        # Command line
        # imode_gcc  1ake_backbone.pdb -m 0 -o 1ake_backbone: writes 1ake_backbone_ic.evec (and its .log and _model.pdb)
        # -o is the output path without its extension: no fixed names next to the output without sandbox
        out_file_prefix = str(Path(self.stage_io_dict["out"]["output_dat_path"]).with_suffix(''))
        self.cmd = [self.binary_path,
                    self.stage_io_dict["in"]["input_pdb_path"],
                    '-o', out_file_prefix,
                    '-m', str(self.cg)
                    ]

        # Run Biobb block
        self.run_biobb()

        # The eigenvectors file is the output
        os.replace(Path(self.stage_io_dict["unique_dir"], out_file_prefix + "_ic.evec"), self.sandbox_file("output_dat_path"))


imod_imode = launcher(ImodImode)

if __name__ == '__main__':
    ImodImode.main()
