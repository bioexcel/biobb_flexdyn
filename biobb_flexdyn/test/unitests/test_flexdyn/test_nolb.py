from biobb_common.tools import test_fixtures as fx
from biobb_flexdyn.flexdyn.nolb_nma import nolb_nma


class TestNolb_nma():
    def setup_class(self):
        fx.test_setup(self, 'nolb_nma')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_nolb_nma(self):
        nolb_nma(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        # assert fx.equal(self.paths['output_pdb_path'], self.paths['ref_output_pdb_path']) # Header changing with every execution
