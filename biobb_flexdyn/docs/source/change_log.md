# Biobb FlexDyn changelog

## [Unreleased]

## What's new in version [5.4.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v5.4.0)?

### Changes

* [UPDATE] Update to biobb_common 5.4.0.
* [FIX] `imod_imc`, `imod_imode`, `nolb_nma`: the files of the tool are named after the output instead of fixed names (`imod_ensemble.pdb`, `imods_evecs_*`, `nolb_ensemble_nlb_decoys.pdb`). Without sandbox (`disable_sandbox`) they were left in the working directory and two runs in the same folder overwrote each other; now only the side files of imode (`.log`, `_model.pdb`) stay, next to the output with its name.
* [FIX] `concoord_dist`, `concoord_disco`: when neither the `concoord_lib_path` property nor the `CONCOORDLIB` environment variable is set, the block stops before running with an error that names both, instead of failing with a missing `None/HBONDS.DAT` file and leaving the sandbox behind.
* [FIX] `concoord_dist`, `concoord_disco`: an input or output file with an unsupported extension stops the block with a `ValueError`; it logged an error and ran CONCOORD anyway.
* [FIX] `concoord_disco`: `vdw` defaults to 1 (OPLS-UA), as documented; without it the block stopped with an error.
* [FIX] `concoord_disco`: `chirality_check` 0 and `seed` 0 are passed to disco; they were ignored as if unset.
* [DOCS] `concoord_dist`, `concoord_disco`, `imod_imc`, `imod_imode`, `imod_imove`, `nolb_nma`: the documented `container_image` default is None (the blocks never used the `cmip/cmip:latest` image named there); `concoord_disco` documents `nofit` once.
* [UPDATE] Python 3.11 and 3.12 (no Python 3.13 yet: prody has no conda build for it).

## What's new in version [5.3.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.0)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1

## What's new in version [5.2.2](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.2)?

### Changes

* [UPDATE] Upgraded compatibility with python 3.12

## What's new in version [5.2.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.1)?

### Changes

* [UPDATE] Update to biobb_common 5.2.2

## What's new in version [5.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.0)?

### Changes

* [UPDATE] Update to biobb_common 5.2.0

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v5.1.0)?

### Changes

* [UPDATE] Update to biobb_common 5.1.0

## What's new in version [5.0.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v5.0.0)?

### Changes

* [FEATURE] New sandbox_path property

## What's new in version [4.2.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.2.0)?
In version 4.2.0 the dependency biobb_common has been updated to 4.2.0 version.

### New features

* Update to biobb_common 4.2.0 (general)

## What's new in version [4.1.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.1.0)?
In version 4.1.0 the dependency biobb_common has been updated to 4.1.0 version.

### New features

* Update to biobb_common 4.1.0 (general)

## What's new in version [4.0.3](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.0.3)?
In version 4.0.3 some minor bugs have been fixed.

### New features

* Minor bug fixes

## What's new in version [4.0.2](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.0.2)?
In version 4.0.2 some minor bugs have been fixed.

### New features

* Minor bug fixes

## What's new in version [4.0.1](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.0.1)?
In version 4.0.1 the imod_imc tool has been added.

### New features

* New imod_imc tool

## What's new in version [4.0.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v4.0.0)?
In version 4.0.0 the dependency biobb_common has been updated to 4.0.0 version.

### New features

* Update to biobb_common 4.0.0 (general)

## What's new in version [3.9.0](https://github.com/bioexcel/biobb_flexdyn/releases/tag/v3.9.0)?
The version 3.9.0 is the first release of biobb_flexdyn. There have been added the concoord_dist, concoord_disco, imod_imode, imod_imove, prody_anm and nolb_nma tools.

### New features

* First release
* FlexDyn module: concoord_dist, concoord_disco, imod_imode, imod_imove, prody_anm and nolb_nma tools