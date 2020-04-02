from setuptools import setup

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
    version="0.0.1",
    python_requires=">=3.6",
    description="nsvision - Computer Vision Wrapper built on top of PIL, cv2 and Numpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nsemble/nsvision",
    author="Nsemble.ai",
    author_email="admin@nsemble.ai",
    license="MIT",
    packages=["nsvision"],
    classifiers=classifiers,
    scripts=["bin/split_data"],
)