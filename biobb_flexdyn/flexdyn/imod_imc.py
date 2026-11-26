#!/usr/bin/env python3

"""Module containing the imode class and the command line interface."""
from typing import Optional
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher


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
            * **amplitude** (*float*) - (1.0) Amplitude linear factor to scale motion
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
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexDyn iMOD imc module."""

        # Command line
        # imc 1ake_backbone.pdb  1ake_backbone_evecs.dat -o 1ake_backbone.ensemble -c 500
        # imc adds .pdb to the -o name: the output path without its extension
        self.cmd = [self.binary_path,
                    self.stage_io_dict["in"]["input_pdb_path"],
                    self.stage_io_dict["in"]["input_dat_path"],
                    '-o', str(Path(self.stage_io_dict["out"]["output_traj_path"]).with_suffix(''))
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


imod_imc = launcher(ImodImc)

if __name__ == '__main__':
    ImodImc.main()
