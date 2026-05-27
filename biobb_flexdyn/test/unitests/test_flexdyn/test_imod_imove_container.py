# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.imod_imove import imod_imove
import pytest
import sys


class TestImodImoveDocker():
    def setup_class(self):
        fx.test_setup(self, 'imod_imove_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imove_docker(self):
        imod_imove(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])  # Header changing with every execution


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestImodImoveSingularity():
    def setup_class(self):
        fx.test_setup(self, 'imod_imove_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imove_singularity(self):
        imod_imove(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])  # Header changing with every execution
