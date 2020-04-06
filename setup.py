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
    packages=["nsvision"],
    install_requires=[
        'numpy==1.18.2',
        'Pillow==7.0.0'
    ],
    classifiers=classifiers,
    scripts=["bin/split_data","bin/rename_files","bin/tumor_data_extractor"],
)
