from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('nsvision/__init__.py', encoding='utf-8') as fid:
    for line in fid:
        if line.startswith('__version__'):
            __version__ = line.strip().split()[-1][1:-1]
            break

CONSOLE_SCRIPTS = [
    'split_data = nsvision.tools.split_data:main',
    'split_data_gui = nsvision.tools.split_data_gui:main',
    'rename_files = nsvision.tools.rename_files:main',
    'tumor_data_extractor = nsvision.tools.tumor_data_extractor:main',
]

setup(
    name="nsvision",
    version=__version__,
    python_requires=">=3.6",
    description="nsvision - Image data processing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nsembleai/nsvision",
    author="Nsemble.ai",
    author_email="admin@nsemble.ai",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow'
    ],
    extras_require={
          'tests': ['natsort',
                    'Pillow',
                    'pytest',
                    'pytest-xdist', # for parallel testing
                    'pytest-cov'], # for testing coverage
          'pep8': ['flake8'],
          'video': ['opencv-python'],
    },
    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
    },
)
