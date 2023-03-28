#!/usr/bin/env python3

"""Module containing the prody_anm class and the command line interface."""
import argparse
import prody
from pathlib import Path
from biobb_common.tools import file_utils as fu
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools.file_utils import launchlogger

class ProdyANM(BiobbObject):
    """
    | biobb_flexdyn ProdyANM
    | Wrapper of the ANM tool from the Prody package.
    | Generate an ensemble of structures using the Prody Anisotropic Network Model (ANM), for coarse-grained NMA.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output multi-model PDB file with the generated ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/prody/prody_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **selection** (*str*) - (calpha) Atoms selection (Prody syntax: http://prody.csb.pitt.edu/manual/reference/atomic/select.html)
            * **cutoff** (*float*) - (15.0) Cutoff distance (Å) for pairwise interactions, minimum is 4.0 Å
            * **gamma** (*float*) - (1.0) Spring constant
            * **rmsd** (*float*) - (1.0) Average RMSD that the conformations will have with respect to the initial conformation
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_flexdyn.flexdyn.prody_anm import prody_anm
            prop = {
                'num_structs' : 20,
                'rmsd' : 4.0
            }
            prody_anm(  input_pdb_path='/path/to/structure.pdb',
                        output_pdb_path='/path/to/output.pdb',
                        properties=prop)

    Info:
        * wrapped_software:
            * name: Prody 
            * version: >=2.2.0
            * license: MIT
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

        self.num_structs = properties.get('num_structs', 500)
        self.selection = properties.get('selection', 'calpha')
        self.cutoff = properties.get('cutoff', 15.0)
        self.gamma = properties.get('gamma', 1.0)
        self.rmsd = properties.get('rmsd', 1.0)

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self):
        """Launches the execution of the FlexDyn ConcoordDist module."""

        # Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()

        prot = prody.parsePDB(self.stage_io_dict["in"]["input_pdb_path"],)

        # http://prody.csb.pitt.edu/manual/reference/atomic/select.html
        prot_sel = prot.select(self.selection)

        enm = prody.ANM('BioBB_flexdyn Prody ANM ensemble generator')

        enm.buildHessian(prot_sel, cutoff=self.cutoff, gamma=self.gamma)

        enm.calcModes()

        bb_enm, bb_atoms = prody.extendModel(enm, prot_sel, prot_sel)

        ensemble = prody.sampleModes(bb_enm[:3], bb_atoms, n_confs=self.num_structs, rmsd=self.rmsd)

        nmastruct = bb_atoms.copy()
        nmastruct.addCoordset(ensemble)
                
        prody.writePDB(self.stage_io_dict["out"]["output_pdb_path"], nmastruct)

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code

def prody_anm(input_pdb_path: str, output_pdb_path: str, 
            properties: dict = None, **kwargs) -> int:
    """Create :class:`ProdyANM <flexdyn.prody_anm.ProdyANM>`flexdyn.prody_anm.ProdyANM class and
    execute :meth:`launch() <flexdyn.prody_anm.ProdyANM.launch>` method"""

    return ProdyANM(    input_pdb_path=input_pdb_path,
                        output_pdb_path=output_pdb_path,
                        properties=properties).launch()

def main():
    parser = argparse.ArgumentParser(description='Generate an ensemble of structures using the Prody Anisotropic Network Model (ANM), for coarse-grained NMA.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input structure file. Accepted formats: pdb')
    required_args.add_argument('--output_pdb_path', required=True, help='Output pdb file. Accepted formats: pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call
    prody_anm(  input_pdb_path=args.input_pdb_path,
                output_pdb_path=args.output_pdb_path,
                properties=properties)

if __name__ == '__main__':
    main()
