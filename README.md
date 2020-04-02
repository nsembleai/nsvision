# nsvision
nsvision - Computer Vision Wrapper built on top of PIL, cv2 and Numpy

## Installation:
```bash
pip install nsvision
```

## Usage:

1. Python
```python
import nsvision as nv
```

2. Command line (split data script)

* Syntax

```bash
split_data -d path_to_data_folder -r ratio_in_tuple_string
```

* example

```bash
split_data -d "./cats_vs_dogs" -r "(70,10,10,10)"
```