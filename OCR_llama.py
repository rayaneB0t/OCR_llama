from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import io
import base64
import requests
from pathlib import Path


def call_groq_api(image_base64: str, prompt: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None, "Error: Missing GROQ_API_KEY environment variable"

    # Use the Meta Llama 4 Scout model (it supports images) rather than the 3.2 previews
    model = "meta-llama/llama-4-scout-17b-16e-instruct"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text",      "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}" }}
                ]
            }
        ],
        # optional: enforce JSON-mode if you want structured output
        # "response_format": {"type": "json_object"},
        "temperature": 0.1,
        "max_tokens": 1000
    }

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"], None

    except requests.exceptions.HTTPError as http_err:
        # Try to parse and show the API’s own error message
        try:
            err = http_err.response.json()
        except ValueError:
            err = http_err.response.text
        return None, f"Groq API returned {http_err.response.status_code}: {err}"

    except Exception as e:
        return None, f"Unexpected error calling Groq API: {e}"


# --- Streamlit App ---

st.set_page_config(
    page_title="Vision OCR",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header & Clear
col1, col2 = st.columns([6,1])
with col1:
    st.title("Vision OCR with Groq & Llama 4 Scout")
with col2:
    if st.button("Clear 🗑️"):
        st.session_state.pop("ocr_result", None)
        st.experimental_rerun()

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded = st.file_uploader("PNG/JPG/JPEG", type=["png","jpg","jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, use_container_width=True)

        if st.button("Extract Text 🔍"):
            with st.spinner("Running OCR…"):
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                img_b64 = base64.b64encode(buf.getvalue()).decode().replace("\n","")

                prompt = (
                    "Extract all text from the image and return it as markdown—with headings, lists or code blocks as appropriate."
                )
                result, error = call_groq_api(img_b64, prompt)
                if error:
                    st.error(error)
                else:
                    st.session_state["ocr_result"] = result

# Main
if "ocr_result" in st.session_state:
    st.markdown(st.session_state["ocr_result"])
else:
    st.info("Upload an image and click ‘Extract Text’.")

st.markdown("---")
st.caption("Powered by Groq + Meta Llama 4 Scout")
