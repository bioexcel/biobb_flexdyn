from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.imod_imc import imod_imc


class TestImodImc():
    def setup_class(self):
        fx.test_setup(self, 'imod_imc')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_imod_imc(self):
        imod_imc(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_traj_path'])
        # assert fx.equal(self.paths['output_traj_path'], self.paths['ref_output_traj_path'])  # Header changing with every execution
