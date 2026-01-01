from setuptools import setup, find_packages

setup(
    name="megasena-analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "pyarrow>=12.0.0",
        "typer>=0.9.0",
    ],
    python_requires=">=3.9",
)
