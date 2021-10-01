import io
import numpy as np
from nsvision import image_utils
import pytest
from pathlib import Path


def test_imread(tmpdir):
    img_rgb_file = str(tmpdir / "img_utils_rgb.png")
    img_rgba_file = str(tmpdir / "img_utils_rgba.png")
    file_grayscale_8bit = str(tmpdir / "grayscale_8bit_img_utils.png")
    file_grayscale_16bit = str(tmpdir / "grayscale_16bit_img_utils.tiff")
    file_grayscale_32bit = str(tmpdir / "grayscale_32bit_img_utils.tiff")

    original_rgb_array = np.array(255 * np.random.rand(100, 100, 3), dtype=np.uint8)
    original_rgb = image_utils.get_image_from_array(
        original_rgb_array, denormalize=False
    )
    original_rgb.save(img_rgb_file)

    original_rgba_array = np.array(255 * np.random.rand(100, 100, 4), dtype=np.uint8)
    original_rgba = image_utils.get_image_from_array(
        original_rgba_array, denormalize=False
    )
    original_rgba.save(img_rgba_file)

    original_grayscale_8bit_array = np.array(
        255 * np.random.rand(100, 100, 1), dtype=np.uint8
    )
    original_grayscale_8bit = image_utils.get_image_from_array(
        original_grayscale_8bit_array, denormalize=False
    )
    original_grayscale_8bit.save(file_grayscale_8bit)

    original_grayscale_16bit_array = np.array(
        np.random.randint(-2147483648, 2147483647, (100, 100, 1)), dtype=np.int16
    )
    original_grayscale_16bit = image_utils.get_image_from_array(
        original_grayscale_16bit_array, denormalize=False, dtype="int16"
    )
    original_grayscale_16bit.save(file_grayscale_16bit)

    original_grayscale_32bit_array = np.array(
        np.random.randint(-2147483648, 2147483647, (100, 100, 1)), dtype=np.int32
    )
    original_grayscale_32bit = image_utils.get_image_from_array(
        original_grayscale_32bit_array, denormalize=False, dtype="int32"
    )
    original_grayscale_32bit.save(file_grayscale_32bit)

    # Now we need to test if loaded image is equal to original

    loaded_img = image_utils.imread(img_rgb_file)
    assert loaded_img.shape == original_rgb_array.shape
    assert np.all(loaded_img == original_rgb_array)

    loaded_img = image_utils.imread(img_rgba_file, color_mode="rgba")
    assert loaded_img.shape == original_rgba_array.shape
    assert np.all(loaded_img == original_rgba_array)

    loaded_img = image_utils.imread(img_rgb_file, color_mode="grayscale")
    assert loaded_img.shape == (
        original_rgb_array.shape[0],
        original_rgb_array.shape[1],
    )

    loaded_img = image_utils.imread(file_grayscale_8bit, color_mode="grayscale")
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_8bit_array.shape
    assert np.all(loaded_img == original_grayscale_8bit_array)

    loaded_img = image_utils.imread(
        file_grayscale_16bit, color_mode="grayscale", dtype="int16"
    )
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_16bit_array.shape
    assert np.all(loaded_img == original_grayscale_16bit_array)
    assert np.allclose(loaded_img, original_grayscale_16bit_array)

    loaded_img = image_utils.imread(
        file_grayscale_32bit, color_mode="grayscale", dtype="int32"
    )
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

    loaded_img = image_utils.imread(img_rgba_file, color_mode="rgba", resize=(100, 100))
    loaded_img_resize = image_utils.imread(
        img_rgba_file, color_mode="rgba", resize=(50, 50)
    )
    assert loaded_img.shape == original_rgba_array.shape
    assert loaded_img_resize.shape == (50, 50, 4)
    assert np.all(loaded_img == original_rgba_array)

    loaded_img = image_utils.imread(
        img_rgb_file, color_mode="grayscale", resize=(100, 100)
    )
    loaded_img_resize = image_utils.imread(
        img_rgb_file, color_mode="grayscale", resize=(50, 50)
    )
    assert loaded_img.shape == (
        original_rgba_array.shape[0],
        original_rgba_array.shape[1],
    )
    assert loaded_img_resize.shape == (50, 50)

    loaded_img = image_utils.imread(
        file_grayscale_8bit, color_mode="grayscale", resize=(100, 100)
    )
    loaded_img_resize = image_utils.imread(
        file_grayscale_8bit, color_mode="grayscale", resize=(50, 50)
    )
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_8bit_array.shape
    assert loaded_img_resize.shape == (50, 50)
    assert np.all(loaded_img == original_grayscale_8bit_array)

    loaded_img = image_utils.imread(
        file_grayscale_16bit, color_mode="grayscale", resize=(100, 100), dtype="int16"
    )
    loaded_img_resize = image_utils.imread(
        file_grayscale_16bit, color_mode="grayscale", resize=(60, 50), dtype="int16"
    )
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_16bit_array.shape
    assert loaded_img_resize.shape == (60, 50)
    assert np.all(loaded_img == original_grayscale_16bit_array)

    loaded_img = image_utils.imread(
        file_grayscale_32bit, color_mode="grayscale", resize=(100, 100), dtype="int32"
    )
    loaded_img_resize = image_utils.imread(
        file_grayscale_32bit, color_mode="grayscale", resize=(70, 95), dtype="int32"
    )
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert loaded_img.shape == original_grayscale_32bit_array.shape
    assert loaded_img_resize.shape == (70, 95)
    assert np.all(loaded_img == original_grayscale_32bit_array)

    # Test different path type
    with open(file_grayscale_32bit, "rb") as f:
        _path = io.BytesIO(f.read())  # io.Bytesio
    loaded_img = image_utils.imread(_path, color_mode="grayscale", dtype="int32")
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert np.all(loaded_img == original_grayscale_32bit_array)

    _path = file_grayscale_32bit  # str
    loaded_img = image_utils.imread(_path, color_mode="grayscale", dtype="int32")
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert np.all(loaded_img == original_grayscale_32bit_array)

    _path = file_grayscale_32bit.encode()  # bytes
    loaded_img = image_utils.imread(_path, color_mode="grayscale", dtype="int32")
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert np.all(loaded_img == original_grayscale_32bit_array)

    _path = Path(tmpdir / "grayscale_32bit_img_utils.tiff")  # Path
    loaded_img = image_utils.imread(_path, color_mode="grayscale", dtype="int32")
    loaded_img = image_utils.expand_dims(loaded_img, axis=2)
    assert np.all(loaded_img == original_grayscale_32bit_array)

    # Check that exception is raised if interpolation not supported.

    loaded_img = image_utils.imread(img_rgb_file, interpolation="unsupported")
    with pytest.raises(ValueError):
        loaded_img = image_utils.imread(
            img_rgb_file, resize=(34, 43), interpolation="unsupported"
        )

    # Check that the aspect ratio of a square is the same

    filename_red_square = str(tmpdir / "red_square_image_utils.png")
    A = np.zeros((50, 100, 3), dtype=np.uint8)  # rectangle image 100x50
    A[20:30, 45:55, 0] = 255  # red square 10x10
    red_square_array = np.array(A)
    red_square = image_utils.get_image_from_array(red_square_array, denormalize=False)
    red_square.save(filename_red_square)

    loaded_img = image_utils.imread(
        filename_red_square, resize=(55, 45), maintain_aspect_ratio=True
    )
    assert loaded_img.shape == (55, 45, 3)

    red_channel_arr = loaded_img[:, :, 0].astype(bool)
    square_width = np.sum(np.sum(red_channel_arr, axis=0))
    square_height = np.sum(np.sum(red_channel_arr, axis=1))
    aspect_ratio_result = square_width / square_height

    # original square had 1:1 ratio
    assert aspect_ratio_result == pytest.approx(1.0)


def test_imurl():
    url = f"https://nsemble.ai/assets/images/logo.png"
    image_from_url = image_utils.imurl(url)
    import PIL

    assert isinstance(image_from_url, PIL.Image.Image)

    with pytest.raises(ValueError):
        image_from_url = image_utils.imurl("nohttp://somehost.com/image.jpg")


def test_expand_dims():
    random_rgb_array = np.array(255 * np.random.rand(100, 100, 3), dtype=np.uint8)
    random_grayscale_8bit_array = np.array(
        255 * np.random.rand(150, 150), dtype=np.uint8
    )
    array_with_added_dims = image_utils.expand_dims(random_rgb_array)
    array_with_added_dims_axis2 = image_utils.expand_dims(
        random_grayscale_8bit_array, axis=2
    )
    assert array_with_added_dims.shape == (1, 100, 100, 3)
    assert array_with_added_dims_axis2.shape == (150, 150, 1)


def test_get_image_from_array():
    rgb_array = np.array(255 * np.random.rand(100, 100, 3), dtype=np.uint8)
    image_from_array = image_utils.get_image_from_array(rgb_array, denormalize=False)
    import PIL

    assert isinstance(image_from_array, PIL.Image.Image)
    assert image_from_array.size == (rgb_array.shape[0], rgb_array.shape[1])


if __name__ == "__main__":
    pytest.main([__file__])
