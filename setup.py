import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_flexdyn",
    version="5.0.0",
    author="Biobb developers",
    author_email="adam.hospital@irbbarcelona.org",
    description="biobb_flexdyn is a BioBB category for studies on the conformational landscape of native proteins.",
    long_description="biobb_flexdyn allows the generation of protein conformational ensembles from 3D structures and the analysis of its molecular flexibility.",
    long_description_content_type="text/markdown",
    keywords="3D-Bioinfo ELIXIR FlexDyn Bioinformatics Workflows BioExcel Compatibility Flexibility Ensembles Protein Structure",
    url="https://github.com/bioexcel/biobb_flexdyn",
    project_urls={
        "Documentation": "http://biobb-flexdyn.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    package_data={'biobb_flexdyn': ['py.typed']},
    include_package_data=True,
    install_requires=['biobb_common==5.0.0', 'scipy>=1.13.0,<1.14.0'],
    python_requires='>=3.9,<3.12',
    entry_points={
        "console_scripts": [
            "concoord_dist = biobb_flexdyn.flexdyn.concoord_dist:main",
            "concoord_disco = biobb_flexdyn.flexdyn.concoord_disco:main",
            "imod_imode = biobb_flexdyn.flexdyn.imod_imode:main",
            "imod_imove = biobb_flexdyn.flexdyn.imod_imove:main",
            "imod_imc = biobb_flexdyn.flexdyn.imod_imc:main",
            "nolb_nma = biobb_flexdyn.flexdyn.nolb_nma:main",
            "prody_anm = biobb_flexdyn.flexdyn.prody_anm:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX"
    ],
)
