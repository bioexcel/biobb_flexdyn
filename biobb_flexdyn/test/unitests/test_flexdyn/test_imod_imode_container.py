# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.imod_imode import imod_imode
import pytest
import sys


class TestImodImodeDocker():
    def setup_class(self):
        fx.test_setup(self, 'imod_imode_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imode_docker(self):
        imod_imode(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        # assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])  # Header changing with every execution


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestImodImodeSingularity():
    def setup_class(self):
        fx.test_setup(self, 'imod_imode_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imode_singularity(self):
        imod_imode(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_dat_path'])
        # assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])  # Header changing with every execution
