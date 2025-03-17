import streamlit as st
import requests
from PIL import Image
import io
import base64

def decode_image(base64_string):
    """Giải mã chuỗi base64 thành ảnh PIL."""
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

st.set_page_config(page_title='Medical Brain Image Analysis', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("Medical Brain Image Analysis")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    version = st.selectbox("Select API version", ["1", "2", "3"])
    if version == "3":
        language = st.selectbox("Select language", ["English", "Vietnamese", "French", "Russian", "Japanese", "Korean"])
    submit = st.button("Submit")

with col2:
    if submit:
        if uploaded_file is not None:
            # Đọc ảnh và gửi request đến API
            image = Image.open(uploaded_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            files = {"image": buffered.getvalue()}
            data = {"language": language} if version == "3" else {}

            api_url = f"https://a20a-2001-ee0-4b7b-e890-ecb4-f3a7-f65-9fe0.ngrok-free.app/version-{version}"
            response = requests.post(api_url, files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                st.write("### Caption:")
                st.write(result["caption"])
                
                if "mask" in result:
                    mask_image = decode_image(result['mask'])
                    col3, col4 = st.columns(2)
                    with col3:
                        st.image(uploaded_file, width=500)
                    with col4:
                        st.image(mask_image, width=500)
            else:
                st.error("Failed to get response from API")
        else:
            st.error("Please upload an image")
