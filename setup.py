import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solaxev",
    use_scm_version=True,
    author="Robin Wohlers-Reichel",
    author_email="me@robinwr.com",
    description="Solax-Evervolt inverter API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/squishykid/solax",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "aiohttp>=3.5.4, <4",
        "voluptuous>=0.11.5",
        "importlib_metadata>=3.6; python_version<'3.10'",
        "typing_extensions>=4.1.0; python_version<'3.11'",
    ],
    setup_requires=[
        "setuptools_scm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "solaxev.inverter": [
            "qvolt_hyb_g3_3p = solaxev.inverters.qvolt_hyb_g3_3p:QVOLTHYBG33P",
            "x1 = solaxev.inverters.x1:X1",
            "x1_boost = solaxev.inverters.x1_boost:X1Boost",
            "x1_g4_series = solaxev.inverters.x1_g4_series:X1G4Series",
            "x1_hybrid_gen4 = solaxev.inverters.x1_hybrid_gen4:X1HybridGen4",
            "x1_mini = solaxev.inverters.x1_mini:X1Mini",
            "x1_mini_v34 = solaxev.inverters.x1_mini_v34:X1MiniV34",
            "x1_smart = solaxev.inverters.x1_smart:X1Smart",
            "x3 = solaxev.inverters.x3:X3",
            "x3_hybrid_g4 = solaxev.inverters.x3_hybrid_g4:X3HybridG4",
            "x3_ultra = solaxev.inverters.x3_ultra:X3Ultra",
            "x3_mic_pro_g2 = solaxev.inverters.x3_mic_pro_g2:X3MicProG2",
            "x3_v34 = solaxev.inverters.x3_v34:X3V34",
            "x_hybrid = solaxev.inverters.x_hybrid:XHybrid",
            "x3_evc = solaxev.inverters.x3_evc:X3EVC",
            "evhb_i7 = solaxev.inverters.evhb_i7:EVHBI7",
        ],
    },
)
