from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.prody_anm import prody_anm

class TestProdyANM():
    def setup_class(self):
        fx.test_setup(self, 'prody_anm')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_prody_anm(self):
        prody_anm(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path']) 
