import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_flexdyn",
    version="3.8.1",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="biobb_flexdyn is a BioBB category for studies on the conformational landscape of native proteins.",
    long_description="biobb_flexdyn allows the generation of protein conformational ensembles from 3D structures and the analysis of its molecular flexibility.",
    long_description_content_type="text/markdown",
    keywords="3D-Bioinfo ELIXIR FlexDyn Bioinformatics Workflows BioExcel Compatibility Flexibility Ensembles Protein Structure",
    url="https://github.com/bioexcel/biobb_flexdyn",
    project_urls={
        "Documentation": "http://biobb_flexdyn.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    include_package_data=True,
    install_requires=['biobb_common==3.8.1'],
    python_requires='>=3.7.*',
    entry_points={
        "console_scripts": [
            "concoord_dist = biobb_flexdyn.flexdyn.concoord_dist:main",
            "concoord_disco = biobb_flexdyn.flexdyn.concoord_disco:main",
            "webnma_run = biobb_flexdyn.flexdyn.flexdyn_webnmarun:main",
            "b2btools_run = biobb_flexdyn.flexdyn.flexdyn_b2btoolsrun:main",
            "prody_run = biobb_flexdyn.flexdyn.flexdyn_prodyrun:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
