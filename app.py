import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Currency Authenticator", page_icon="💵")

st.title("💵 Currency Authentication Web App")
st.markdown("Upload a currency image to check if it's **Genuine** or **Counterfeit**.")

uploaded_file = st.file_uploader("Upload a currency image", type=["jpg", "jpeg", "png"])

# Azure Custom Vision details
PREDICTION_KEY = "2U9z6FCjwzpt3Ch3UXWCiX3RJvi64x4r6ja1tCNdHXwOnEIdiagxJQQJ99BDACYeBjFXJ3w3AAAIACOGekcw"
PREDICTION_URL = "https://imageclassification7-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/3c9a83a0-3338-4179-8ac7-e1ee3bac892c/classify/iterations/currency-auth-v1/image"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Classify Currency"):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes = img_bytes.getvalue()

        headers = {
            "Prediction-Key": PREDICTION_KEY,
            "Content-Type": "application/octet-stream"
        }

        response = requests.post(PREDICTION_URL, headers=headers, data=img_bytes)

        if response.status_code == 200:
            predictions = response.json()["predictions"]
            st.subheader("Prediction Result:")
            for pred in predictions:
                st.write(f"**{pred['tagName']}** – {pred['probability']*100:.2f}%")
        else:
            st.error("❌ Prediction failed. Check your endpoint or key.")
