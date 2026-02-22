from setuptools import setup, find_packages

setup(
    name="calificar",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=1.4.0",
        "numpy>=1.22.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
)