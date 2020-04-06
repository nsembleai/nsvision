# nsvision
## This wrapper library is built on using PIL , cv2 and Numpy.
## We have optimised the library for reducing the code work while working on image processing for data science.

## nsvision functions:
* imread(image_path) #Reads an input image and returns 3d image array

* imshow(numpy array) #Opens up a new window and displays in new window

* imsave(path) #Save image from array to a specific path

* expand_dims(numpy_array) #expand array dimensions based on axis position

* reduce_dims(numpy_array) #reduce image dimensions based on axis position (must use if expand_dims is called on image, before displaying or saving image)

* imsave(array) #save image to location

* live_video #run this function to display live stream from webcam, you can also add your model_function as input (mostly used for object detection)

## Installation:
```bash
pip install nsvision
```

## Usage:
### Python

1. importing
```python
import nsvision as nv
```

2. Reading an image for model
```python
image_array = nv.imread("image_path", resize = (224,224), color_mode='rgb')

#function returns image as numpy array
```

3. Display image (terminal / jupyter)
```python
#displaying a regular image
nv.imshow(image_array)

#displaying image read from cv2 function
nv.imshow(image_array , is_cv2_image = True)
#setting is_cv2_image = True , will display image read from cv2.imread()
```
4. Saving an image.
```python
#saving regular image
nv.imsave('path_to_write_image' , image_array , file_format='png')

#saving image read from cv2 library
nv.imsave('path_to_write_image' , image_array , file_format='png', is_cv2_image = True)
```

5. Expand Image Dimensions
```python
#expand image dimensions as per axis position
expanded_image = nv.expand_dims(image_array, axis = 0)

#expand image and normalize
expanded_normalized_image = nv.expand_dims(image_array,normalize = True)
```

6. Reduce Image Dimensions
```python
reduced_image = nv.reduce_dims(image_array, axis = 0)
```

7. Live Video Streaming
```python
nv.live_video(source=0, color_mode = 'rgb', resize=(224,224))

#opens a window showing video from source , source 0 is webcam
```

#### Using nv.live_video() for object detection / live image classification

```python
#create your preprocessing function which accepts image_array as input and returns processed image_array

#sample preprocess function which can be used with nv.live_video()

def pre_processing_function(image_array):
    #your preprocessing steps here
    #example:
    image_array = nv.expand_dims(image_array,axis=0,normalize=True)
    prediction_boxes = model.predict(image_array)
    image_array = draw_boxes(image_array,prediction_boxes)
    
    return image_array #note your preprocessing function must return image array as output, or it will throw error.
```
### Command line (split data script)<br>
Use commandline tool for splitting data as per ratio for image classification problems

* Syntax

```bash
split_data -d path_to_data_folder -r ratio_in_tuple_string
```

* example

```bash
split_data -d "./cats_vs_dogs" -r "(70,10,10,10)"
```
This will split data inside class folder as 70% for training , 10% validiation, 10% testing and 10% for QA.

For more information about using command line tool:
```bash
split_data -h
```

### Command line (rename files script)<br>
Use commandline tool for renaming the files in a folder

* Syntax

```bash
rename_files -n common name -f folder path -i number from which renaming to be started
```

* example

```bash
rename_files -n "image_" -f "./image_folder" -i 1
```
This will rename the files in the image_folder 

For more information about using command line tool:
```bash
rename_files -h
```

### Command line (tumor data extractor script)<br>
Use commandline tool specifically for extracting and converting the mat files of brain tumor image data from the downloaded zip file using this [link](https://figshare.com/articles/brain_tumor_dataset/1512427)

* Syntax

```bash
tumor_data_extractor -b folder path of the downloaded zip folder -e extension in which mat files to be converted(default - jpg)
```

* example

```bash
tumor_data_extractor -b "./1512427.zip" -e png
```
This will convert all the .mat file in the above zip folder into the given extension file format(default .jpg)
All the converted files will be save in separate folder named brain_tumor_data in their respective tumor name folder

For more information about using command line tool:
```bash
tumor_data_extractor -h
```


