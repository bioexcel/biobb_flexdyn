# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.imod_imc import imod_imc
import pytest
import sys


class TestImodImcDocker():
    def setup_class(self):
        fx.test_setup(self, 'imod_imc_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imc_docker(self):
        imod_imc(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])  # Header changing with every execution


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestImodImcSingularity():
    def setup_class(self):
        fx.test_setup(self, 'imod_imc_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imc_singularity(self):
        imod_imc(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])  # Header changing with every execution
