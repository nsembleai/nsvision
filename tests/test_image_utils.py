import io
import numpy as np
from nsvision import image_utils
import pytest

def test_imread(tmpdir):
    img_rgb_file = str(tmpdir / 'img_utils_rgb.png')
    img_rgba_file = str(tmpdir / 'img_utils_rgba.png')
    file_grayscale_8bit = str(tmpdir / 'grayscale_8bit_img_utils.png')
    file_grayscale_16bit = str(tmpdir / 'grayscale_16bit_img_utils.tiff')
    file_grayscale_32bit = str(tmpdir / 'grayscale_32bit_img_utils.tiff')

    original_rgb_array = np.array(255 * np.random.rand(100, 100, 3),
                                  dtype=np.uint8)
    original_rgb = image_utils.get_image_from_array(original_rgb_array, denormalize=False)
    original_rgb.save(img_rgb_file)

    original_rgba_array = np.array(255 * np.random.rand(100, 100, 4),
                                   dtype=np.uint8)
    original_rgba = image_utils.get_image_from_array(original_rgba_array, denormalize=False)
    original_rgba.save(img_rgba_file)

    original_grayscale_8bit_array = np.array(255 * np.random.rand(100, 100, 1),
                                             dtype=np.uint8)
    original_grayscale_8bit = image_utils.get_image_from_array(original_grayscale_8bit_array,
                                                 denormalize=False)
    original_grayscale_8bit.save(file_grayscale_8bit)

    original_grayscale_16bit_array = np.array(
        np.random.randint(-2147483648, 2147483647, (100, 100, 1)), dtype=np.int16
    )
    original_grayscale_16bit = image_utils.get_image_from_array(original_grayscale_16bit_array,
                                                  denormalize=False, dtype='int16')
    original_grayscale_16bit.save(file_grayscale_16bit)

    original_grayscale_32bit_array = np.array(
        np.random.randint(-2147483648, 2147483647, (100, 100, 1)), dtype=np.int32
    )
    original_grayscale_32bit = image_utils.get_image_from_array(original_grayscale_32bit_array,
                                                  denormalize=False, dtype='int32')
    original_grayscale_32bit.save(file_grayscale_32bit)

    # Now we need to test if loaded image is equal to original

    loaded_img = image_utils.imread(img_rgb_file)
    assert loaded_img.shape == original_rgb_array.shape
    assert np.all(loaded_img == original_rgb_array)

    loaded_img = image_utils.imread(img_rgba_file, color_mode='rgba')
    assert loaded_img.shape == original_rgba_array.shape
    assert np.all(loaded_img == original_rgba_array)

    loaded_img = image_utils.imread(img_rgb_file, color_mode='grayscale')
    assert loaded_img.shape == (original_rgb_array.shape[0],
                                     original_rgb_array.shape[1])

    loaded_img = image_utils.imread(file_grayscale_8bit, color_mode='grayscale')
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_8bit_array.shape
    assert np.all(loaded_img == original_grayscale_8bit_array)

    loaded_img = image_utils.imread(file_grayscale_16bit, color_mode='grayscale', dtype='int16')
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_16bit_array.shape
    assert np.all(loaded_img == original_grayscale_16bit_array)
    assert np.allclose(loaded_img, original_grayscale_16bit_array)
    
    loaded_img = image_utils.imread(file_grayscale_32bit, color_mode='grayscale', dtype='int32')
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_32bit_array.shape
    assert np.all(loaded_img == original_grayscale_32bit_array)
    assert np.allclose(loaded_img, original_grayscale_32bit_array)

    # Testing resize parameter with both original and resized version

    loaded_img = image_utils.imread(img_rgb_file, resize=(100, 100))
    loaded_img_resize = image_utils.imread(img_rgb_file, resize=(50, 50))
    assert loaded_img.shape == original_rgb_array.shape
    assert loaded_img_resize.shape == (50, 50, 3)
    assert np.all(loaded_img == original_rgb_array)

    loaded_img = image_utils.imread(img_rgba_file, color_mode='rgba',
                               resize=(100, 100))
    loaded_img_resize = image_utils.imread(img_rgba_file, color_mode='rgba',
                               resize=(50, 50))
    assert loaded_img.shape == original_rgba_array.shape
    assert loaded_img_resize.shape == (50, 50, 4)
    assert np.all(loaded_img == original_rgba_array)

    loaded_img = image_utils.imread(img_rgb_file, color_mode='grayscale',
                               resize=(100, 100))
    loaded_img_resize = image_utils.imread(img_rgb_file, color_mode='grayscale',
                               resize=(50, 50))
    assert loaded_img.shape == (original_rgba_array.shape[0],
                                     original_rgba_array.shape[1])
    assert loaded_img_resize.shape == (50, 50)

    loaded_img = image_utils.imread(file_grayscale_8bit, color_mode='grayscale',
                               resize=(100, 100))
    loaded_img_resize = image_utils.imread(file_grayscale_8bit, color_mode='grayscale',
                               resize=(50, 50))
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_8bit_array.shape
    assert loaded_img_resize.shape == (50, 50)
    assert np.all(loaded_img == original_grayscale_8bit_array)

    loaded_img = image_utils.imread(file_grayscale_16bit, color_mode='grayscale',
                               resize=(100, 100), dtype='int16')
    loaded_img_resize = image_utils.imread(file_grayscale_16bit, color_mode='grayscale',
                               resize=(60, 50), dtype='int16')
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_16bit_array.shape
    assert loaded_img_resize.shape == (60, 50)
    assert np.all(loaded_img == original_grayscale_16bit_array)

    loaded_img = image_utils.imread(file_grayscale_32bit, color_mode='grayscale',
                               resize=(100, 100), dtype='int32')
    loaded_img_resize = image_utils.imread(file_grayscale_32bit, color_mode='grayscale',
                               resize=(70, 95), dtype='int32')
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_32bit_array.shape
    assert loaded_img_resize.shape == (70, 95)
    assert np.all(loaded_img == original_grayscale_32bit_array)

if __name__ == '__main__':
    pytest.main([__file__])
