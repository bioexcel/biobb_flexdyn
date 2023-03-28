from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.imod_imove import imod_imove

class TestImodImove():
    def setup_class(self):
        fx.test_setup(self, 'imod_imove')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_imod_imove(self):
        imod_imove(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path']) # Header changing with every execution
