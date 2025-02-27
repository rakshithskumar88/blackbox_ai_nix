from setuptools import setup, find_packages

setup(
    name="blackbox-ai",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'blackbox_ai': ['ui/*.css'],
    },
    install_requires=[
        "PyGObject>=3.42.0",
        "keyboard>=0.13.5",
        "aiohttp>=3.8.1",
        "typing-extensions>=4.4.0",
    ],
    entry_points={
        'console_scripts': [
            'blackbox-ai=blackbox_ai.main:main',
        ],
    },
    python_requires='>=3.8',
)
