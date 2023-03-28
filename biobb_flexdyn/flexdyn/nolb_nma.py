#!/usr/bin/env python3

"""Module containing the nolb class and the command line interface."""
import argparse
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class Nolb_nma(BiobbObject):
    """
    | biobb_flexdyn Nolb_nma
    | Wrapper of the NOLB tool 
    | Generate an ensemble of structures using the NOLB (NOn-Linear rigid Block) NMA tool.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output multi-model PDB file with the generated ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/nolb_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **cutoff** (*float*) - (5.0) This options specifies the interaction cutoff distance for the elastic network models (in angstroms), 5 by default. The Hessian matrix is constructed according to this interaction distance. Some artifacts should be expected for too short distances (< 5 Å). 
            * **rmsd** (*float*) - (1.0) Maximum RMSd for decoy generation. 
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

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
    properties: dict = None, **kwargs) -> None:

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': { 'input_pdb_path': input_pdb_path },
            'out': { 'output_pdb_path': output_pdb_path }
        }

        # Properties specific for BB
        self.properties = properties
        self.binary_path = properties.get('binary_path', 'NOLB')

        self.num_structs = properties.get('num_structs', 500)
        #self.num_modes = properties.get('num_modes', 10)
        self.cutoff = properties.get('cutoff', 5.0)
        self.rmsd = properties.get('rmsd', 1.0)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn NOLB module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        # Output temporary file
        out_file_prefix = Path(self.stage_io_dict.get("unique_dir")).joinpath("nolb_ensemble") 
        out_file = Path(self.stage_io_dict.get("unique_dir")).joinpath("nolb_ensemble_nlb_decoys.pdb") 

        # Command line
        # ./NOLB 1ake_monomer.pdb -s 100 --rmsd 5 -m  -o patata # Output: patata_nlb_decoys.pdb
        self.cmd = [self.binary_path, 
                str(Path(self.stage_io_dict["in"]["input_pdb_path"]).relative_to(Path.cwd())),
                "-o", str(out_file_prefix),
                "-m" # Minimizing the generated structures by default
                ]

        # Properties
        if self.num_structs:
            self.cmd.append('-s')
            self.cmd.append(str(self.num_structs))

        # Num modes is deactivated for the decoys generation. CHECK!
        #  * **num_modes** (*int*) - (10) Number of non-trivial modes to compute, 10 by default. If this number exceeds the size of the Hessian matrix, it will be adapted accordingly.
        #if self.num_modes:
        #    self.cmd.append('-n')
        #    self.cmd.append(str(self.num_modes))

        if self.cutoff:
            self.cmd.append('-c')
            self.cmd.append(str(self.cutoff))

        if self.rmsd:
            self.cmd.append('--rmsd')
            self.cmd.append(str(self.rmsd))

        #--dist 1 -m --nSteps 5000 --tol 0.001
        self.cmd.append("--dist 1 --nSteps 5000 --tol 0.001")

        # Run Biobb block
        self.run_biobb()

        # Copying generated output file to the final (user-given) file name
        shutil.copy2(out_file, self.stage_io_dict["out"]["output_pdb_path"])

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def nolb_nma(input_pdb_path: str, output_pdb_path: str, 
            properties: dict = None, **kwargs) -> int:
    """Create :class:`Nolb_nma <flexdyn.nolb_nma.Nolb_nma>`flexdyn.nolb_nma.Nolb_nma class and
    execute :meth:`launch() <flexdyn.nolb_nma.Nolb_nma.launch>` method"""

    return Nolb_nma(    input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generate an ensemble of structures using the NOLB (NOn-Linear rigid Block) NMA tool.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file. Accepted formats: pdb')
    required_args.add_argument('--output_pdb_path', required=True, help='Output pdb file. Accepted formats: pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    nolb_nma(   input_pdb_path=args.input_pdb_path,
            output_pdb_path=args.output_pdb_path,
            properties=properties)

if __name__ == '__main__':
    main()
