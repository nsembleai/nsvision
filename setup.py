from setuptools import setup
from nsvision import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License",
    "Topic :: Utilities",
]

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
    description="nsvision - Computer Vision Wrapper built on top of PIL, cv2 and Numpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nsemble/nsvision",
    author="Nsemble.ai",
    author_email="admin@nsemble.ai",
    license="MIT",
    packages=["nsvision", "nsvision.tools","nsvision.xml","nsvision.s3bucket","nsvision.image_augmentation",],
    install_requires=[
        'numpy==1.18.3',
        'Pillow==8.1.1'
    ],
    classifiers=classifiers,
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
    },
)
