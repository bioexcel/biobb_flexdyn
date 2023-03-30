from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.concoord_dist import concoord_dist

class TestConcoordDist():
    def setup_class(self):
        fx.test_setup(self, 'concoord_dist')

    def teardown_class(self):
        fx.test_teardown(self)
        #pass

    def test_concoord_dist(self):
        concoord_dist(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path'])
        #assert fx.equal(self.paths['output_gro_path'], self.paths['ref_output_gro_path'])
        #assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path']) # Header changing with every execution