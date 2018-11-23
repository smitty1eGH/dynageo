from setuptools import setup

setup(
    name="dynageo",
    version="0.1",
    py_modules=["dynageo"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        dynageo=dynageo:main
    """,
)
