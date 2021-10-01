# nsvision
nsvision is the image data pre and post processing and data augmentation library. It provides utilities for working with image data.

nsvision is compatible with Python 3.6+ and is distributed under the MIT license.

nsvision can be imported as
```python3
import nsvision as nv
```

# Functions
## imread
Read input image from path or url, returns preprocessed image as numpy array

Reading from path
```python
image_array = nv.imread("image_path", resize = (224,224), color_mode='rgb')

#function returns image as numpy array
```
Parameters:
```
image_path: Image Path.
resize: (width,height) tuple
color_mode: default is None
    you can also use color_mode as `rgb` or `rgba` or `grayscale`
interpolation:
    Interpolation method used to resample the image if the
    target size is different from that of the loaded image.
    Supported methods are "nearest", "bilinear", and "bicubic".
    Default: "nearest".
dtype: Dtype to use for the returned array.
normalize: Returns scaled image array if set to True. 
           Useful for preprocessing for image classification
    Default: False
return_original: Returns original image array along with resized image array.
    Default: False
    Note: This parameter only works with resize parameter
```
Returns:
```
A 3D Numpy array.
```
Raises:
```
ValueError: if invalid `image_path` or `resize` or `color_mode` or `interpolation` or `dtype` is passed.
ValueError: if return_original is True and resize is None
```
<br>

## imurl
Reading image from url <br>
`requires requests library`
```python
#Get image from url
image = nv.imurl('https://example.com/example_image.jpeg')

#Get image array from url
url = 'https://example.com/example_image.jpeg'
image_array = nv.imurl(url,return_as_array=True,resize=(150,150), color_mode = 'rgb')
```
Parameters:
```
image_url: http / https url of image
    
return_as_array: Convert image directly to numpy array
    	default: False
    
kwargs:
    Keyword arguments of imread can be passed for image modification:
    Example:
        imurl(image_url,to_array=True,resize=(224,224),color_mode = 'rgb',dtype='float32')
        
Note: kwargs only works with return_as_array = True
```
Returns:
```
PIL Image by default:

if return_as_array is True:
    image will be returned as numpy array.

Additional params like resize, color_mode, dtype , return_original can also be passed inorder to refine the image
```
Raises:
```
ValueError: if url format is incorrect
```
<br>

## imshow
Display image using PIL show function
```python
#displaying a regular image
nv.imshow(image_array)

#displaying image read from cv2 function
nv.imshow(image_array , is_cv2_image = True)
#setting is_cv2_image = True , will display image read from cv2.imread()
```
Parameters:
```
image: PIL or CV2 image array
is_cv2_image: If image_array is processed using cv2
```
<br>

## imsave
Save image array using PIL object's save method

```python
#saving regular image
nv.imsave('path_to_write_image' , image_array , file_format='png')

#saving image read from cv2 library
nv.imsave('path_to_write_image' , image_array , file_format='png', is_cv2_image = True)
```
Parameters:
```
path: Location for writing image file
image: image array
file_format: file format for saving file
is_cv2_image: Set to True if image is loaded using cv2 
    Default: False
denormalize: Set to True if image was normalized during preprocessing
    Default: True
kwargs:
    other keyword args if required by PIL
```
<br>

## expand_dims
expand numpy image array as per axis position
```python
#expand image dimensions as per axis position
expanded_image = nv.expand_dims(image_array, axis = 0)

#expand image and normalize
expanded_normalized_image = nv.expand_dims(image_array,normalize = True)
```
Parameters:
```
array : numpy array.
axis : int or tuple of ints
    Position in the expanded axes where the new axis is placed

normalize: 
    True : return normalized image
    False : return just image array with expanded dimensions 
```
Returns:
```
A Numpy array with expanded dimensions.
(optional) expanded normalized array if normalize is true
```    
<br>

## reduce_dims
Reduce Array Dimensions as per axis position
```python
reduced_image = nv.reduce_dims(image_array, axis = 0)
```
Parameters:
```
array: numpy nd array
axis : int or tuple of ints
    Position in the expanded axes where the new axis is placed.
    default: axis = 0
```
Returns:
```
A Numpy array with reduced dimensions.
```
<br>

## get_image_from_array
Converts numpy image array to a PIL Image instance.
```
image = nv.get_image_from_array(image_array)
```
Parameters:
```
img: Input Numpy image array.
denormalize: Revert back normalized image to unnormalized form
    Default: True.
dtype: Dtype to use.
    Default: "float32".
is_cv2_image: Set to True if image is loaded using cv2
    Default: False
```
Returns:
```
A PIL image
```
Raises
```
TypeError if image_array is not an numpy ndarray
```        
<br>

## split_image_data
Images splitter using directly in jupyter notebook
```python
from nsvision import classifier

classifier.split_image_data(
    data_dir = "images/cats_vs_dogs",
    ratio=(40,30,20,10))

#splits images from given folder as per train, val , test and QA.
#Mostly helpful for image classification problems
```
Parameters:
```
data_dir: Path to images
ratio: ratio for split
```
<br>

## image_to_base64
Encode image as base64 string
Mostly useful for sending image from api
```python
base64_encoded_image = nv.image_to_base64(pil_image,file_format='PNG')
```
Parameters:
```
image: image path or PIL image instance 
    Incase image is numpy array, convert to image object using nv.get_image_from_array(array)

file_format: file format of image
```
Returns:
```
Base64 encoded image string
```
<br>

## base64_to_bytes
Decode base64 image string and return as bytes
```python
decoded_image_bytes = nv.base64_to_bytes(base64_encoded_image)
#decode base64 image string and convert to bytes. 
#Later on you can use nv.imread(decoded_image_bytes)
```
Parameters:
```
base64_encoded_image: base64 encoded image
```
Returns:
```
bytes object of decoded base64 image string
```
<br>

# License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

