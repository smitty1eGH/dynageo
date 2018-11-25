from setuptools import setup, find_packages

setup(
    name="dynageo",
    version="0.1",
    py_modules=["dynageocli"],
    packages=find_packages(),
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        dynageo=dynageocli:main
    """,
)
