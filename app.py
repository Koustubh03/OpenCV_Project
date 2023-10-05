import io

import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageChops
import numpy as np

# Function to apply selected filter
def apply_edges_filter(image):
    pass


def apply_filter(image, filter_name, filter_params=None):
    if filter_name == 'Original':
        return image
    elif filter_name == 'Grayscale':
        return ImageOps.grayscale(image)
    elif filter_name == 'Sepia':
        return apply_sepia_filter(image)
    elif filter_name == 'Invert':
        return ImageOps.invert(image)
    elif filter_name == 'Blur':
        return apply_blur_filter(image, filter_params['blur_radius'])
    elif filter_name == 'Edges':
        return apply_edges_filter(image)
    elif filter_name == 'Emboss':
        return apply_emboss_filter(image)
    elif filter_name == 'Sharpen':
        return apply_sharpen_filter(image, filter_params['sharpen_factor'])
    elif filter_name == '3D':
        return apply_3d_filter(image, filter_params['intensity'])
    elif filter_name == 'Blur Gallery':
        return apply_blur_gallery_filter(image, filter_params['blur_intensity'])
    elif filter_name == 'Distort':
        return apply_distort_filter(image, filter_params['distort_intensity'])
    elif filter_name == 'Noise':
        return apply_noise_filter(image, filter_params['noise_intensity'])
    elif filter_name == 'Pixelate':
        return apply_pixelate_filter(image, filter_params['pixelate_intensity'])
    elif filter_name == 'Render':
        return apply_render_filter(image, filter_params['render_intensity'])
    elif filter_name == 'Stylize':
        return apply_stylize_filter(image, filter_params['stylize_intensity'])
    elif filter_name == 'Opacity':
        return apply_opacity_filter(image, filter_params['opacity'])
    elif filter_name == 'Adjust All':
        return adjust_image_properties(image, filter_params['brightness'], filter_params['contrast'], filter_params['saturation'])

# Function to apply the Sepia filter
def apply_sepia_filter(image):
    width, height = image.size
    sepia_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            r = min(255, gray + 100)
            g = min(255, gray + 50)
            b = min(255, gray)
            sepia_image.putpixel((x, y), (r, g, b))

    return sepia_image

# Function to apply the Blur filter
def apply_blur_filter(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius=radius))

# Function to apply the Emboss filter
def apply_emboss_filter(image):
    return image.filter(ImageFilter.EMBOSS)

# Function to apply the Sharpen filter
def apply_sharpen_filter(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

# Function to apply the 3D filter
def apply_3d_filter(image, intensity):
    depth = ImageEnhance.Color(image).enhance(0.2)
    return ImageChops.screen(image, depth)

# Function to apply the Blur Gallery filter
def apply_blur_gallery_filter(image, intensity):
    return image.filter(ImageFilter.BoxBlur(intensity))

# Function to apply the Distort filter
def apply_distort_filter(image, intensity):
    width, height = image.size
    distorted_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            x_distort = int(x + intensity * np.sin(2 * np.pi * y / 128.0))
            y_distort = int(y + intensity * np.cos(2 * np.pi * x / 128.0))

            if 0 <= x_distort < width and 0 <= y_distort < height:
                distorted_image.putpixel((x, y), image.getpixel((x_distort, y_distort)))
            else:
                distorted_image.putpixel((x, y), (0, 0, 0))

    return distorted_image

# Function to apply the Noise filter
def apply_noise_filter(image, intensity):
    noisy = Image.new('RGB', image.size)
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = image.getpixel((x, y))
            noise = np.random.randint(-intensity, intensity + 1, 3)
            r, g, b = np.clip([r, g, b] + noise, 0, 255)
            noisy.putpixel((x, y), (r, g, b))
    return noisy

# Function to apply the Pixelate filter
def apply_pixelate_filter(image, pixel_size):
    return image.resize(
        (image.width // pixel_size, image.height // pixel_size),
        resample=Image.BILINEAR,
    ).resize(
        (image.width, image.height),
        resample=Image.NEAREST,
    )

# Function to apply the Render filter
def apply_render_filter(image, intensity):
    return image.point(lambda p: p * intensity)

# Function to apply the Stylize filter
def apply_stylize_filter(image, intensity):
    return ImageOps.posterize(image, int(8 * intensity))

# Function to apply the Opacity filter
def apply_opacity_filter(image, opacity):
    return Image.blend(image.convert("RGBA"), Image.new("RGBA", image.size, (255, 255, 255, int(255 * opacity))), opacity)

# Function to adjust brightness
def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)  # factor < 1 darkens, factor > 1 brightens

# Function to adjust contrast
def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)  # factor < 1 reduces contrast, factor > 1 increases contrast

# Function to adjust saturation
def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)  # factor < 1 desaturates, factor > 1 saturates

# Function to adjust brightness, contrast, and saturation combined
def adjust_image_properties(image, brightness, contrast, saturation):
    image = adjust_brightness(image, brightness)
    image = adjust_contrast(image, contrast)
    image = adjust_saturation(image, saturation)
    return image

# Streamlit app
st.title('Image Filter App')
st.sidebar.header('Settings')

# Upload an image
uploaded_image = st.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

# uploaded_image = st.file_uploader('Upload an image', type=['jpg', 'png', 'jpeg'])

if uploaded_image is not None:
    try:
        # Use PIL to open the uploaded image
        image = Image.open(uploaded_image)

        if image is not None:
            # Display the original image
            st.image(image, use_column_width=True, caption='Original Image')

            # Choose a filter
            filter_name = st.selectbox('Select a filter', ['Original', 'Grayscale', 'Sepia', 'Invert', 'Blur', 'Edges', 'Emboss', 'Sharpen', '3D', 'Blur Gallery', 'Distort', 'Noise', 'Pixelate', 'Render', 'Stylize', 'Opacity', 'Adjust All'])

            filter_params = {}

            if filter_name in ['Brightness', 'Contrast', 'Saturation']:
                filter_params['brightness'] = st.slider('Brightness', 0.5, 2.0, 1.0)
                filter_params['contrast'] = st.slider('Contrast', 0.5, 2.0, 1.0)
                filter_params['saturation'] = st.slider('Saturation', 0.5, 2.0, 1.0)
            elif filter_name == 'Blur':
                filter_params['blur_radius'] = st.slider('Blur Radius', 0, 10, 2)
            elif filter_name == 'Sharpen':
                filter_params['sharpen_factor'] = st.slider('Sharpen Factor', 0.5, 2.0, 1.0)
            elif filter_name == '3D':
                filter_params['intensity'] = st.slider('3D Intensity', 0.1, 2.0, 1.0)
            elif filter_name == 'Blur Gallery':
                filter_params['blur_intensity'] = st.slider('Blur Intensity', 0, 10, 2)
            elif filter_name == 'Distort':
                filter_params['distort_intensity'] = st.slider('Distort Intensity', 0, 100, 20)
            elif filter_name == 'Noise':
                filter_params['noise_intensity'] = st.slider('Noise Intensity', 0, 50, 10)
            elif filter_name == 'Pixelate':
                filter_params['pixelate_intensity'] = st.slider('Pixelate Intensity', 2, 20, 5)
            elif filter_name == 'Render':
                filter_params['render_intensity'] = st.slider('Render Intensity', 0.1, 2.0, 1.0)
            elif filter_name == 'Stylize':
                filter_params['stylize_intensity'] = st.slider('Stylize Intensity', 0.1, 2.0, 1.0)
            elif filter_name == 'Opacity':
                filter_params['opacity'] = st.slider('Opacity', 0.0, 1.0, 1.0)

            if st.button('Apply Filter'):
                filtered_image = apply_filter(image, filter_name, filter_params)
                st.image(filtered_image, use_column_width=True, caption=f'{filter_name} Filtered Image')

                # Add a download button for the filtered image
                filtered_image_bytes = io.BytesIO()
                filtered_image.save(filtered_image_bytes, format='PNG')
                st.download_button('Download Filtered Image', filtered_image_bytes.getvalue(), 'filtered_image.png', 'image/png')

        else:
            st.warning('Invalid image format. Please upload a valid image file.')
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')