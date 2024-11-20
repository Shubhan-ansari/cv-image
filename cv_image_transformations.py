import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Streamlit App Title and Layout Configuration
st.set_page_config(page_title="Image Transformation App", layout="wide")
st.title("Image Transformation App")
st.sidebar.title("Navigation")

# Sidebar Navigation Options
options = ["Upload Image", "Scaling", "Rotation", "Translation", "Affine Transformation"]
selected_option = st.sidebar.radio("Select Transformation", options)

# Light/Dark Mode Toggle
theme = st.sidebar.radio("Choose Theme", ["Light Mode", "Dark Mode"], index=0)
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
        }
        .stSlider > div > div {
            color: white;
        }
        .stSlider label {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stSlider > div > div {
            color: black;
        }
        .stSlider label {
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to upload and preprocess image
def load_image(uploaded_file):
    image = np.array(Image.open(uploaded_file))
    return image

# Transformation Functions
def scale_image(image, scale_x, scale_y):
    height, width = image.shape[:2]
    scaled_image = cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
    return scaled_image

def rotate_image(image, angle):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image

def translate_image(image, shift_x, shift_y):
    height, width = image.shape[:2]
    translation_matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    translated_image = cv2.warpAffine(image, translation_matrix, (width, height))
    return translated_image

def affine_transform(image):
    height, width = image.shape[:2]
    src_points = np.float32([[50, 50], [200, 50], [50, 200]])
    dst_points = np.float32([[10, 100], [200, 50], [100, 250]])
    affine_matrix = cv2.getAffineTransform(src_points, dst_points)
    transformed_image = cv2.warpAffine(image, affine_matrix, (width, height))
    return transformed_image

# Upload Section
uploaded_files = st.sidebar.file_uploader("Upload one or more images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    st.sidebar.success("Image(s) uploaded successfully!")

    for uploaded_file in uploaded_files:
        image = load_image(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Scaling
        if selected_option == "Scaling":
            st.header("Scaling")
            scale_x = st.slider("Scale X", 0.1, 3.0, 1.0, 0.1)
            scale_y = st.slider("Scale Y", 0.1, 3.0, 1.0, 0.1)
            st.write(f"Parameters: Scale X={scale_x}, Scale Y={scale_y}")
            scaled_image = scale_image(image, scale_x, scale_y)
            st.image(scaled_image, caption="Scaled Image", use_container_width=True)
            st.download_button("Download Scaled Image", data=cv2.imencode('.jpg', scaled_image)[1].tobytes(), file_name="scaled_image.jpg")

        # Rotation
        elif selected_option == "Rotation":
            st.header("Rotation")
            angle = st.slider("Rotation Angle", -180, 180, 0, 1)
            st.write(f"Parameters: Angle={angle}°")
            rotated_image = rotate_image(image, angle)
            st.image(rotated_image, caption="Rotated Image", use_container_width=True)
            st.download_button("Download Rotated Image", data=cv2.imencode('.jpg', rotated_image)[1].tobytes(), file_name="rotated_image.jpg")

        # Translation
        elif selected_option == "Translation":
            st.header("Translation")
            shift_x = st.slider("Shift X", -200, 200, 0, 1)
            shift_y = st.slider("Shift Y", -200, 200, 0, 1)
            st.write(f"Parameters: Shift X={shift_x}, Shift Y={shift_y}")
            translated_image = translate_image(image, shift_x, shift_y)
            st.image(translated_image, caption="Translated Image", use_container_width=True)
            st.download_button("Download Translated Image", data=cv2.imencode('.jpg', translated_image)[1].tobytes(), file_name="translated_image.jpg")

        # Affine Transformation
        elif selected_option == "Affine Transformation":
            st.header("Affine Transformation")
            transformed_image = affine_transform(image)
            st.image(transformed_image, caption="Affine Transformed Image", use_container_width=True)
            st.download_button("Download Affine Transformed Image", data=cv2.imencode('.jpg', transformed_image)[1].tobytes(), file_name="affine_transformed_image.jpg")
else:
    st.warning("Please upload at least one image to proceed.")

# Footer
st.sidebar.info("Designed by Aditya Dhanwai")
