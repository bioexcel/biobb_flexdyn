#!/usr/bin/env python3

"""Module containing the prody_anm class and the command line interface."""
from typing import Optional
import prody  # type: ignore
from biobb_common.generic.biobb_object import BiobbObject, launcher


class ProdyANM(BiobbObject):
    """
    | biobb_flexdyn ProdyANM
    | Wrapper of the ANM tool from the Prody package.
    | Generate an ensemble of structures using the Prody Anisotropic Network Model (ANM), for coarse-grained NMA.

    Args:
        input_pdb_path (str): Input PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output multi-model PDB file with the generated ensemble. File type: output. `Sample file <https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/prody_output.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dict - Python dictionary object containing the tool parameters, not input/output files):
            * **num_structs** (*int*) - (500) Number of structures to be generated
            * **selection** (*str*) - ("calpha") Atoms selection (Prody syntax: http://prody.csb.pitt.edu/manual/reference/atomic/select.html)
            * **cutoff** (*float*) - (15.0) Cutoff distance (Å) for pairwise interactions, minimum is 4.0 Å
            * **gamma** (*float*) - (1.0) Spring constant
            * **rmsd** (*float*) - (1.0) Average RMSD that the conformations will have with respect to the initial conformation
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

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
                 properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

    def run(self):
        """Launches the execution of the FlexDyn ConcoordDist module."""

        prot = prody.parsePDB(self.sandbox_file("input_pdb_path"),)

        # http://prody.csb.pitt.edu/manual/reference/atomic/select.html
        prot_sel = prot.select(self.selection)  # type: ignore

        enm = prody.ANM('BioBB_flexdyn Prody ANM ensemble generator')

        enm.buildHessian(prot_sel, cutoff=self.cutoff, gamma=self.gamma)

        enm.calcModes()

        bb_enm, bb_atoms = prody.extendModel(enm, prot_sel, prot_sel)

        ensemble = prody.sampleModes(bb_enm[:3], bb_atoms, n_confs=self.num_structs, rmsd=self.rmsd)

        nmastruct = bb_atoms.copy()
        nmastruct.addCoordset(ensemble)

        prody.writePDB(self.sandbox_file("output_pdb_path"), nmastruct)


prody_anm = launcher(ProdyANM)

if __name__ == '__main__':
    ProdyANM.main()
