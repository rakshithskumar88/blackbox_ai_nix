from setuptools import setup, find_packages

setup(
    name="blackbox-ai",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyGObject>=3.42.0",
        "pycairo>=1.20.0",
    ],
    entry_points={
        'console_scripts': [
            'blackbox-ai=blackbox_ai.main:main',
        ],
    },
    python_requires='>=3.8',
)
