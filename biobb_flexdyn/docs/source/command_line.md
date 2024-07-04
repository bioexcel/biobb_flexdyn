# BioBB FLEXDYN Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Imod_imc
Wrapper of the imc tool
### Get help
Command:
```python
imod_imc -h
```
    usage: imod_imc [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --input_dat_path INPUT_DAT_PATH --output_traj_path OUTPUT_TRAJ_PATH
    
    Compute a Monte-Carlo IC-NMA based conformational ensemble using the imc tool from the iMODS package.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file. Accepted formats: pdb
      --input_dat_path INPUT_DAT_PATH
                            Input evecs file. Accepted formats: dat
      --output_traj_path OUTPUT_TRAJ_PATH
                            Output traj file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure_cleaned.pdb). Accepted formats: PDB
* **input_dat_path** (*string*): Input dat with normal modes. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/imod_imode_evecs.dat). Accepted formats: DAT, TXT
* **output_traj_path** (*string*): Output multi-model PDB file with the generated ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imc_output.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **num_structs** (*integer*): (500) Number of structures to be generated.
* **num_modes** (*integer*): (5) Number of eigenvectors to be employed.
* **amplitude** (*integer*): (1) Amplitude linear factor to scale motion.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imc.yml)
```python
properties:
  amplitude: 6.0
  num_modes: 10
  num_structs: 10

```
#### Command line
```python
imod_imc --config config_imod_imc.yml --input_pdb_path structure_cleaned.pdb --input_dat_path imod_imode_evecs.dat --output_traj_path imod_imc_output.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imc.json)
```python
{
  "properties": {
    "num_structs": 10,
    "num_modes": 10,
    "amplitude": 6.0
  }
}
```
#### Command line
```python
imod_imc --config config_imod_imc.json --input_pdb_path structure_cleaned.pdb --input_dat_path imod_imode_evecs.dat --output_traj_path imod_imc_output.pdb
```

## Imod_imode
Wrapper of the imode tool
### Get help
Command:
```python
imod_imode -h
```
    usage: imod_imode [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --output_dat_path OUTPUT_DAT_PATH
    
    Compute the normal modes of a macromolecule using the imode tool from the iMODS package.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file. Accepted formats: pdb
      --output_dat_path OUTPUT_DAT_PATH
                            Output evecs dat file. Accepted formats: dat.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb). Accepted formats: PDB
* **output_dat_path** (*string*): Output dat with normal modes. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imode_evecs.dat). Accepted formats: DAT, TXT
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **cg** (*integer*): (2) Coarse-Grained model. .
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imode.yml)
```python
properties:
  cg: 2

```
#### Command line
```python
imod_imode --config config_imod_imode.yml --input_pdb_path structure.pdb --output_dat_path imod_imode_evecs.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imode.json)
```python
{
  "properties": {
    "cg": 2
  }
}
```
#### Command line
```python
imod_imode --config config_imod_imode.json --input_pdb_path structure.pdb --output_dat_path imod_imode_evecs.dat
```

## Nolb_nma
Wrapper of the NOLB tool
### Get help
Command:
```python
nolb_nma -h
```
    usage: nolb_nma [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --output_pdb_path OUTPUT_PDB_PATH
    
    Generate an ensemble of structures using the NOLB (NOn-Linear rigid Block) NMA tool.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file. Accepted formats: pdb
      --output_pdb_path OUTPUT_PDB_PATH
                            Output pdb file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output multi-model PDB file with the generated ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/nolb_output.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **num_structs** (*integer*): (500) Number of structures to be generated.
* **cutoff** (*number*): (5.0) This options specifies the interaction cutoff distance for the elastic network models (in angstroms), 5 by default. The Hessian matrix is constructed according to this interaction distance. Some artifacts should be expected for too short distances (< 5 Å)..
* **rmsd** (*number*): (1.0) Maximum RMSd for decoy generation..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_nolb_nma.yml)
```python
properties:
  num_structs: 20

```
#### Command line
```python
nolb_nma --config config_nolb_nma.yml --input_pdb_path structure.pdb --output_pdb_path nolb_output.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_nolb_nma.json)
```python
{
  "properties": {
    "num_structs": 20
  }
}
```
#### Command line
```python
nolb_nma --config config_nolb_nma.json --input_pdb_path structure.pdb --output_pdb_path nolb_output.pdb
```

## Concoord_disco
Wrapper of the Disco tool from the Concoord package.
### Get help
Command:
```python
concoord_disco -h
```
    usage: concoord_disco [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --input_dat_path INPUT_DAT_PATH --output_traj_path OUTPUT_TRAJ_PATH --output_rmsd_path OUTPUT_RMSD_PATH --output_bfactor_path OUTPUT_BFACTOR_PATH
    
    Structure generation based on a set of geometric constraints extracted with the Concoord Dist tool.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file in PDB format. Accepted formats: pdb
      --input_dat_path INPUT_DAT_PATH
                            Input dat with structure interpretation and bond definitions. Accepted formats: dat, txt
      --output_traj_path OUTPUT_TRAJ_PATH
                            Output trajectory file. Accepted formats: pdb, gro, xtc.
      --output_rmsd_path OUTPUT_RMSD_PATH
                            Output RMSd file. Accepted formats: dat.
      --output_bfactor_path OUTPUT_BFACTOR_PATH
                            Output B-factor file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input structure file in PDB format. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb). Accepted formats: PDB
* **input_dat_path** (*string*): Input dat with structure interpretation and bond definitions. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/dist.dat). Accepted formats: DAT, TXT
* **output_traj_path** (*string*): Output trajectory file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_trj.pdb). Accepted formats: PDB, XTC, GRO
* **output_rmsd_path** (*string*): Output rmsd file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_rmsd.dat). Accepted formats: DAT
* **output_bfactor_path** (*string*): Output B-factor file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/disco_bfactor.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (disco) Concoord disco binary path to be used..
* **vdw** (*integer*): (1) Select a set of Van der Waals parameters. .
* **num_structs** (*integer*): (500) Number of structures to be generated.
* **num_iterations** (*integer*): (2500) Maximum number of iterations per structure.
* **chirality_check** (*integer*): (2) Chirality check. .
* **bs** (*integer*): (0) Number of rounds of triangular bound smoothing (default 0), (if >= 6, tetragonal BS is activated).
* **nofit** (*boolean*): (False) Do not fit generated structures to reference.
* **seed** (*integer*): (741265) Initial random seed.
* **violation** (*number*): (1.0) Maximal acceptable sum of violations (nm).
* **convergence** (*integer*): (50) Consider convergence failed after this number of non-productive iterations.
* **trials** (*integer*): (25) Maximum number of trials per run.
* **damp** (*integer*): (1) Damping factor for distance corrections. .
* **dyn** (*integer*): (1) Number of rounds to dynamically set tolerances.
* **bump** (*boolean*): (False) Do extra bump check.
* **pairlist_freq** (*integer*): (10) Pairlist update frequency in steps (only valid together with bump).
* **cutoff** (*number*): (0.5) Cut-off radius for pairlist (nm) (only valid together with bump).
* **ref** (*boolean*): (False) Use input coordinates instead of random starting coordinates.
* **scale** (*integer*): (1) Pre-scale coordinates with this factor.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_concoord_disco.yml)
```python
properties:
  num_structs: 20
  vdw: 4

```
#### Command line
```python
concoord_disco --config config_concoord_disco.yml --input_pdb_path structure.pdb --input_dat_path dist.dat --output_traj_path disco_trj.pdb --output_rmsd_path disco_rmsd.dat --output_bfactor_path disco_bfactor.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_concoord_disco.json)
```python
{
  "properties": {
    "vdw": 4,
    "num_structs": 20
  }
}
```
#### Command line
```python
concoord_disco --config config_concoord_disco.json --input_pdb_path structure.pdb --input_dat_path dist.dat --output_traj_path disco_trj.pdb --output_rmsd_path disco_rmsd.dat --output_bfactor_path disco_bfactor.pdb
```

## Concoord_dist
Wrapper of the Dist tool from the Concoord package.
### Get help
Command:
```python
concoord_dist -h
```
    usage: concoord_dist [-h] [--config CONFIG] --input_structure_path INPUT_STRUCTURE_PATH --output_pdb_path OUTPUT_PDB_PATH --output_gro_path OUTPUT_GRO_PATH --output_dat_path OUTPUT_DAT_PATH
    
    Structure interpretation and bond definitions from a PDB/GRO file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file. Accepted formats: pdb, gro.
      --output_pdb_path OUTPUT_PDB_PATH
                            Output pdb file. Accepted formats: pdb.
      --output_gro_path OUTPUT_GRO_PATH
                            Output gro file. Accepted formats: gro.
      --output_dat_path OUTPUT_DAT_PATH
                            Output dat file with structure interpretation and bond definitions. Accepted formats: dat, txt.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb). Accepted formats: PDB, GRO
* **output_pdb_path** (*string*): Output pdb file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.pdb). Accepted formats: PDB
* **output_gro_path** (*string*): Output gro file. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.gro). Accepted formats: GRO
* **output_dat_path** (*string*): Output dat with structure interpretation and bond definitions. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/dist.dat). Accepted formats: DAT, TXT
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **binary_path** (*string*): (dist) Concoord dist binary path to be used..
* **vdw** (*integer*): (1) Select a set of Van der Waals parameters. .
* **bond_angle** (*integer*): (1) Select a set of bond/angle parameters. .
* **retain_hydrogens** (*boolean*): (False) Retain hydrogen atoms.
* **nb_interactions** (*boolean*): (False) Try to find alternatives for non-bonded interactions (by default the native contacts will be preserved).
* **cutoff** (*number*): (4.0) cut-off radius (Angstroms) for non-bonded interacting pairs (the cut-off distances are additional to the sum of VDW radii).
* **min_distances** (*integer*): (50) Minimum number of distances to be defined for each atom.
* **damp** (*number*): (1.0) Multiply each distance margin by this value.
* **fixed_atoms** (*boolean*): (False) Interpret zero occupancy as atoms to keep fixed.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_concoord_dist.yml)
```python
properties:
  bond_angle: 1
  vdw: 1

```
#### Command line
```python
concoord_dist --config config_concoord_dist.yml --input_structure_path structure.pdb --output_pdb_path dist.pdb --output_gro_path dist.gro --output_dat_path dist.dat
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_concoord_dist.json)
```python
{
  "properties": {
    "vdw": 1,
    "bond_angle": 1
  }
}
```
#### Command line
```python
concoord_dist --config config_concoord_dist.json --input_structure_path structure.pdb --output_pdb_path dist.pdb --output_gro_path dist.gro --output_dat_path dist.dat
```

## Imod_imove
Wrapper of the imove tool
### Get help
Command:
```python
imod_imove -h
```
    usage: imod_imove [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --input_dat_path INPUT_DAT_PATH --output_pdb_path OUTPUT_PDB_PATH
    
    Animate the normal modes of a macromolecule using the imove tool from the iMODS package.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file. Accepted formats: pdb
      --input_dat_path INPUT_DAT_PATH
                            Input evecs file. Accepted formats: dat
      --output_pdb_path OUTPUT_PDB_PATH
                            Output pdb file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure_cleaned.pdb). Accepted formats: PDB
* **input_dat_path** (*string*): Input dat with normal modes. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/imod_imode_evecs.dat). Accepted formats: DAT, TXT
* **output_pdb_path** (*string*): Output multi-model PDB file with the generated animation by Principal Component. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/flexdyn/imod_imove_output.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **pc** (*integer*): (1) Principal Component..
* **num_frames** (*integer*): (11) Number of frames to be generated.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imove.yml)
```python
properties:
  pc: 1

```
#### Command line
```python
imod_imove --config config_imod_imove.yml --input_pdb_path structure_cleaned.pdb --input_dat_path imod_imode_evecs.dat --output_pdb_path imod_imove_output.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_imod_imove.json)
```python
{
  "properties": {
    "pc": 1
  }
}
```
#### Command line
```python
imod_imove --config config_imod_imove.json --input_pdb_path structure_cleaned.pdb --input_dat_path imod_imode_evecs.dat --output_pdb_path imod_imove_output.pdb
```

## Prody_anm
Wrapper of the ANM tool from the Prody package.
### Get help
Command:
```python
prody_anm -h
```
    usage: prody_anm [-h] [--config CONFIG] --input_pdb_path INPUT_PDB_PATH --output_pdb_path OUTPUT_PDB_PATH
    
    Generate an ensemble of structures using the Prody Anisotropic Network Model (ANM), for coarse-grained NMA.
    
    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
    
    required arguments:
      --input_pdb_path INPUT_PDB_PATH
                            Input structure file. Accepted formats: pdb
      --output_pdb_path OUTPUT_PDB_PATH
                            Output pdb file. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file. File type: input. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/data/flexdyn/structure.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output multi-model PDB file with the generated ensemble. File type: output. [Sample file](https://github.com/bioexcel/biobb_flexdyn/raw/master/biobb_flexdyn/test/reference/prody/prody_output.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **num_structs** (*integer*): (500) Number of structures to be generated.
* **selection** (*string*): (calpha) Atoms selection (Prody syntax: http://prody.csb.pitt.edu/manual/reference/atomic/select.html).
* **cutoff** (*number*): (15.0) Cutoff distance (Å) for pairwise interactions, minimum is 4.0 Å.
* **gamma** (*number*): (1.0) Spring constant.
* **rmsd** (*number*): (1.0) Average RMSD that the conformations will have with respect to the initial conformation.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_prody_anm.yml)
```python
properties:
  num_structs: 20
  rmsd: 4.0

```
#### Command line
```python
prody_anm --config config_prody_anm.yml --input_pdb_path structure.pdb --output_pdb_path prody_output.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_flexdyn/blob/master/biobb_flexdyn/test/data/config/config_prody_anm.json)
```python
{
  "properties": {
    "num_structs": 20,
    "rmsd": 4.0
  }
}
```
#### Command line
```python
prody_anm --config config_prody_anm.json --input_pdb_path structure.pdb --output_pdb_path prody_output.pdb
```
