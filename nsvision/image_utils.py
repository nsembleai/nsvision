from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from io import BytesIO
from warnings import warn
from re import sub
from base64 import b64encode,b64decode

# Specify which functions to be imported to be used with nv as nv.__functionname__()
# Functions included in __all__ will be imported on calling "from nsvision.image_utils import *"
# While creating a new function, don't forget to mention below incase you want to use with nv as nv.new_func()
__all__ = [
    "imread","imurl", "load_image_as_object", # image reading functions
    "expand_dims","reduce_dims", # functions having numpy array operations 
    "imshow","get_image_from_array", # functions retriving / displaying images
    "imsave", # functions writing image  
    "base64_to_bytes","image_to_base64", # functions performing base64 operations
]


try:
    import requests as request_image
except ImportError:
    request_image = None
try:
    from PIL import Image as pilimage
    from numpy import asarray as toarray
    from numpy import expand_dims as expand
    from numpy import squeeze
    from numpy import max as npmax
    from numpy import min as npmin
except ImportError:
    raise ImportError('Could not import PIL.Image. or Numpy '
        'This library requires PIL >= 7.0.0 and numpy >= 1.18.1')


interpolation_methods = {
        'nearest': pilimage.NEAREST,
        'bilinear': pilimage.BILINEAR,
        'bicubic': pilimage.BICUBIC,
        'hamming': pilimage.HAMMING,
        'box': pilimage.BOX,
        'lanczos': pilimage.LANCZOS
}


def imread(image_path,resize=None,color_mode = None,interpolation='nearest',dtype='float32',return_original = False,normalize=False):
    """Converts a PIL Image instance to a Ndarray optimised for model.
    Parameters
    ----------
        image_path: Image Path or bytes.
        resize: (width,height) tuple
        color_mode: default is None
            you can also use color_mode as `rgb` or `rgba` or `grayscale`
        interpolation:
            Interpolation method used to resample the image if the
            target size is different from that of the loaded image.
            Supported methods are "nearest", "bilinear", and "bicubic".
            If PIL version 1.1.3 or newer is installed, "lanczos" is also
            supported. If PIL version 3.4.0 or newer is installed, "box" and
            "hamming" are also supported.
            Default: "nearest".
        dtype: Dtype to use for the returned array.
            Default: float32

        return_original: Returns original image array along with resized image array.
            Default: False
            Note: This parameter only works with resize parameter

        normalize: Returns normalized image if set to True
            Default: False
    # Returns
        A 3D Numpy array.
    # Raises
        ValueError: if invalid `image_path` or `resize` or `color_mode` or `interpolation` or `dtype` is passed.
        ValueError: if return_original is True and resize is None
    """
    image = pilimage.open(image_path)
    if color_mode is not None:
        if color_mode == 'grayscale':
            if image.mode not in ('L', 'I;16', 'I'):
                image = image.convert('L')
        elif color_mode == 'rgba':
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
        elif color_mode == 'rgb':
            if image.mode != 'RGB':
                image = image.convert('RGB')
        else:
            raise ValueError('color_mode must be "grayscale", "rgb", or "rgba"')
        
    if resize is not None:
        if not isinstance(resize,tuple):
            raise TypeError(f'resize must be tuple of (width,height) but got {resize} of type {type(resize)} instead')

        if len(resize) != 2:
            raise ValueError(f'Tuple with (width,height) required but got {resize} instead.')

        original_image_array = toarray(image,dtype=dtype)
        if image.size != resize:
            if interpolation not in interpolation_methods:
                raise ValueError(f'Invalid interpolation, currently supported interpolations:{interpolation_methods.keys()}')
            resample = interpolation_methods.get(interpolation)
            image = image.resize(resize, resample)
    
    image_array = toarray(image,dtype=dtype)

    if normalize:
        image_array /= 255.
    
    if return_original:
        if resize is None:
            raise ValueError("return_original parameter only works with resize parameter")
        return original_image_array , image_array
    
    return image_array


def load_image_as_object(image_path,color_mode=None,interpolation='nearest',resize=None):
    """Loads image as PIL object
    image_path: path or bytes like object
    Parameters
    ----------
        image_path: Image Path or bytes.
        resize: (width,height) tuple
        color_mode: default is None
            you can also use color_mode as `rgb` or `rgba` or `grayscale`
        interpolation:
            Interpolation method used to resample the image if the
            target size is different from that of the loaded image.
            Supported methods are "nearest", "bilinear", and "bicubic".
            If PIL version 1.1.3 or newer is installed, "lanczos" is also
            supported. If PIL version 3.4.0 or newer is installed, "box" and
            "hamming" are also supported.
            Default: "nearest".

    # Returns
        A pil image object
    # Raises
        ValueError: if invalid `image_path` or `resize` or `color_mode` or `interpolation` is passed.    
    """
    image = pilimage.open(image_path)
    if color_mode is not None:
        if color_mode == 'grayscale':
            if image.mode not in ('L', 'I;16', 'I'):
                image = image.convert('L')
        elif color_mode == 'rgba':
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
        elif color_mode == 'rgb':
            if image.mode != 'RGB':
                image = image.convert('RGB')
        else:
            raise ValueError('color_mode must be "grayscale", "rgb", or "rgba"')
        
    if resize is not None:
        if not isinstance(resize,tuple):
            raise TypeError(f'resize must be tuple of (width,height) but got {resize} of type {type(resize)} instead')

        if len(resize) != 2:
            raise ValueError(f'Tuple with (width,height) required but got {resize} instead.')

        if image.size != resize:
            if interpolation not in interpolation_methods:
                raise ValueError(f'Invalid interpolation, currently supported interpolations:{interpolation_methods.keys()}')
            resample = interpolation_methods.get(interpolation)
            image = image.resize(resize, resample)
    return image


def imurl(image_url, return_as_array = False , **kwargs):
    """
    Read image from url and convert to bytes or ndarray
    
    Paramters
    ---------
    image_url: http / https url of image
    
    return_as_array: Convert image directly to numpy array
        default: False
    
    kwargs:
        Keyword arguments of imread can be passed for image modification:
        Example:
            imurl(image_url,to_array=True,resize=(224,224),color_mode = 'rgb',dtype='float32')
            
        Note: kwargs only works with return_as_array = True
        
    Returns:
    --------
        PIL Image by default:
        if return_as_array is True:
            image will be returned as numpy array.
        
        Additional params like resize, color_mode, dtype , return_original can also be passed inorder to refine the image

    Raises:
    -------
        ImportError if requests library is not installed    
    """
    if request_image is None:
        raise ImportError('requests library is required from reading image from url '
                         'Install it using pip install requests')
    
    
    if not image_url.startswith('http'):
        raise ValueError(f'invalid url found. Required http or https url but got {image_url} instead')
        
        
    image_response = request_image.get(image_url)
    imbytes = BytesIO(image_response.content)
    
    if return_as_array:
        return imread(imbytes,**kwargs)
    
    image = pilimage.open(imbytes)
    
    return image


def expand_dims(array,axis=0,normalize=False):
    """Expand the shape of an array.

    Insert a new axis that will appear at the `axis` position in the expanded
    array shape.

    Parameters
    ----------
    array : numpy array.
    axis : int or tuple of ints
    Position in the expanded axes where the new axis is placed
    normalize: 
        True : return normalized image
        False : return just image array with expanded dimensions 
    """
    array = expand(array,axis=axis)
    if normalize:
        array /= 255.
    return array


def get_image_from_array(img_array, denormalize=True, dtype='float32' ,is_cv2_image = False):
    """Converts numpy image array to a PIL Image instance.
    Parameters
    ----------
        img: Input Numpy image array.
        denormalize: Revert back normalized image to unnormalized form
            Default: True.
        dtype: Dtype to use.
            Default: "float32".
        is_cv2_image: Set to True if image is loaded using cv2
            Default: False
    Returns
    -------
        A PIL Image.
    Raises
    ------
        Raises TypeError if image_array is not an numpy ndarray
    """
    if not hasattr(img_array, 'ndim'):
        raise TypeError(f'Required image_array to be of type numpy.ndarray but got {type(img_array)} instead')

    if img_array.ndim != 3:
        if img_array.ndim == 2:
            """expand image dimensions only if image is 2D grayscale
            manually adding channel dimension `1` to image (only for 2D grayscale image)"""
            img_array = expand_dims(img_array,axis=2)
        else:
            raise ValueError(f'Expected array with 3 dimensions Got array with shape {img_array.shape}\n'
                'Incase you have used expand_dims for preprocessing, use nv.reduce_dims() for reducing expanded dimensions\n'
                'make sure to check the axis position while expanding or reducing dimensions.')

    if is_cv2_image: #If numpy array is cv2 image
        img_array = img_array[...,::-1] #Convert BGR to RGB

    img_array = toarray(img_array,dtype=dtype)
    # Original Numpy array x has format (height, width, channel)
    # or (channel, height, width)
    # but target PIL image has format (width, height, channel)

    if denormalize:
        img_array = img_array - npmin(img_array)
        img_max = npmax(img_array)
        if img_max != 0:
            img_array /= img_max
        img_array *= 255
    if img_array.shape[2] == 4: #RGBA Image
        return pilimage.fromarray(img_array.astype('uint8'), 'RGBA')
    elif img_array.shape[2] == 3: #RGB image
        return pilimage.fromarray(img_array.astype('uint8'), 'RGB')
    elif img_array.shape[2] == 1: # grayscale image
        if npmax(img_array) > 255:
            # 32-bit signed integer grayscale image. PIL mode "I"
            return pilimage.fromarray(img_array[:, :, 0].astype('int32'), 'I')
        return pilimage.fromarray(img_array[:, :, 0].astype('uint8'), 'L')
    else:
        raise ValueError(f'Channel {img_array.shape[2]} not supported')


def imshow(image,is_cv2_image=False):
    """
    Displays image in new window
    Parameters
    image: PIL or CV2 image array
    is_cv2_image: If image_array is processed using cv2
    """
    if hasattr(image,'show'):
        image.show()
    else:
        get_image_from_array(image,is_cv2_image=is_cv2_image).show()


def imsave(path,image,file_format = None ,is_cv2_image=False,denormalize=True,**kwargs):
    """
    Write image array or instance to a file.
    Parameters
    ----------
    path: Location for writing image file
    image: image array
    file_format: file_format for image
    is_cv2_image: Set to True if image is loaded using cv2 
        Default: False
    denormalize: Set to True if image was normalized during preprocessing
        Default: True
    kwargs:
        other keyword args if required by PIL
    """
    if hasattr(image,'save'): 
        image.save(path,file_format=file_format,**kwargs)
    else:
        image = get_image_from_array(image, denormalize=denormalize , is_cv2_image=is_cv2_image)
        if image.mode == 'RGBA' and (file_format == 'jpg' or file_format == 'jpeg'):
            warn('JPG format does not support RGBA images, converting to RGB.')
            image = image.convert('RGB')
        image.save(path, format=file_format, **kwargs)


def reduce_dims(array,axis=0):
    """
    Reduce array dimensions at given axis
    Note: If trying on image array please check if expand_dims 
          is used by you during image preprocessing and axis too.

    Parameters
    ----------
    array: numpy nd array
    axis : int or tuple of ints
    Position in the expanded axes where the new axis is placed.
    default: 0
    """
    return squeeze(array,axis=axis)


def base64_to_bytes(base64_encoded_image):
    """
    Convert base64 image data to PIL image

    Parameters
    ----------
    base64_encoded_image: base64 encoded image

    Returns
    -------
    Decoded image as Bytes Array
    """
    image_data = sub('^data:image/.+;base64,', '', base64_encoded_image)
    return BytesIO(b64decode(image_data))


def image_to_base64(image,file_format='PNG'):
    """
    Convert image from array to base64 string
    Parameters
    ----------
    image: path or pil image object

    file_format: file format of image
    
    Returns
    -------
    base64 encoded image as string
    """
    if isinstance(image,str):
        image = load_image_as_object(image)

    buffered = BytesIO()
    image.save(buffered, format=file_format)
    return u"data:image/png;base64," + b64encode(buffered.getvalue()).decode("ascii")