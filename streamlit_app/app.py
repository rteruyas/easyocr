import streamlit as st
import requests
import numpy as np
from PIL import Image

with st.sidebar:
    st.title('''
            Lab3
             ''')
    st.markdown('''
                    ### `docker-compose`, `easyocr`, `streamlit`, `mlflow`
                ''')
    st.markdown('')
    image = st.file_uploader(label = 'Choisissez votre image', type = ['png','jpg', 'jpeg'])

    st.markdown('')
    st.markdown('')
    st.markdown('''
                @author: Ray Teruya
                [github repository](https://github.com/rteruyas/image-to-text-easyocr)
                ''')
    
st.markdown('## Easy OCR - Extract text from images')
st.markdown('')

if image is not None:
    input_image = Image.open(image)
    st.image(input_image)
    st.markdown('')    
    with st.spinner('🤖 bip bip bip ...'):
        response = requests.post('http://fastapi:8000/extract', files={'file': image.getvalue()})
        words = response.json()
        st.success(words['message'])    
    st.balloons()
else:
    st.write('Pour telecharger une image, veuillez utiliser le menu de gauche')