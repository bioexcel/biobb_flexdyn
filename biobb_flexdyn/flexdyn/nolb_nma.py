#!/usr/bin/env python3

"""Module containing the nolb class and the command line interface."""
from typing import Optional
import os
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher


class Nolb_nma(BiobbObject):
    """
    | biobb_flexdyn Nolb_nma
    | Wrapper of the NOLB tool
    | Generate an ensemble of structures using the NOLB (NOn-Linear rigid Block) NMA tool.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output multi-model PDB file with the generated ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/nolb_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*str*) - ("NOLB") NOLB binary path to be used.
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **cutoff** (*float*) - (5.0) This options specifies the interaction cutoff distance for the elastic network models (in angstroms), 5 by default. The Hessian matrix is constructed according to this interaction distance. Some artifacts should be expected for too short distances (< 5 Å).
            * **rmsd** (*float*) - (1.0) Maximum RMSd for decoy generation.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - (None) Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.nolb_nma import nolb_nma
            prop = {
                'num_structs' : 20
            }
            nolb_nma(   input_pdb_path='/path/to/structure.pdb',
                    output_pdb_path='/path/to/output.pdb',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: NOLB
            * version: >=1.9
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_pdb_path: str, output_pdb_path: str,
                 properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexDyn NOLB module."""

        # Command line
        # ./NOLB 1ake_monomer.pdb -s 100 --rmsd 5 -m  -o 1ake_decoys.pdb # Output: 1ake_decoys_nlb_decoys.pdb
        # NOLB removes the extension of -o (after the last dot of the path): -o is the output path
        self.cmd = [self.binary_path,
                    self.stage_io_dict["in"]["input_pdb_path"],
                    "-o", self.stage_io_dict["out"]["output_pdb_path"],
                    "-m"  # Minimizing the generated structures by default
                    ]

        # Properties
        if self.num_structs:
            self.cmd.append('-s')
            self.cmd.append(str(self.num_structs))

        if self.cutoff:
            self.cmd.append('-c')
            self.cmd.append(str(self.cutoff))

        if self.rmsd:
            self.cmd.append('--rmsd')
            self.cmd.append(str(self.rmsd))

        # --dist 1 -m --nSteps 5000 --tol 0.001
        self.cmd.append("--dist 1 --nSteps 5000 --tol 0.001")

        # Run Biobb block
        self.run_biobb()

        # The decoys file is the output
        decoys = str(Path(self.stage_io_dict["out"]["output_pdb_path"]).with_suffix('')) + "_nlb_decoys.pdb"
        os.replace(Path(self.stage_io_dict["unique_dir"], decoys), self.sandbox_file("output_pdb_path"))


nolb_nma = launcher(Nolb_nma)

if __name__ == '__main__':
    Nolb_nma.main()
