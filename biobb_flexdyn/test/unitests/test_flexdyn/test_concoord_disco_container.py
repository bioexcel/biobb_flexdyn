# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.concoord_disco import concoord_disco
import pytest
import sys


class TestConcoordDiscoDocker():
    def setup_class(self):
        fx.test_setup(self, 'concoord_disco_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_concoord_disco_docker(self):
        concoord_disco(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_traj_path'])
        assert fx.not_empty(self.paths['output_rmsd_path'])
        assert fx.not_empty(self.paths['output_bfactor_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rmsd_path'], self.paths['ref_output_rmsd_path']) # Frames swap??
        # assert fx.equal(self.paths['output_bfactor_path'], self.paths['ref_output_bfactor_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestConcoordDiscoSingularity():
    def setup_class(self):
        fx.test_setup(self, 'concoord_disco_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_concoord_disco_singularity(self):
        concoord_disco(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_traj_path'])
        assert fx.not_empty(self.paths['output_rmsd_path'])
        assert fx.not_empty(self.paths['output_bfactor_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])
        # assert fx.equal(self.paths['output_rmsd_path'], self.paths['ref_output_rmsd_path']) # Frames swap??
        # assert fx.equal(self.paths['output_bfactor_path'], self.paths['ref_output_bfactor_path'])