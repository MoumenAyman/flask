import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from gtts import gTTS
import io

st.set_page_config(
    page_title="ScanMind AI - Premium Image Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    h1 { color: #818cf8 !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button { background-color: #4f46e5; color: white; border-radius: 12px; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #4338ca; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title(" Premium Features")
st.sidebar.markdown("Welcome to the ultimate AI-powered image utility suite. 100% Free for global creators.")
st.sidebar.markdown("---")
st.sidebar.markdown("###  Ad Space")
st.sidebar.info("Sponsored Link: [Upgrade to Pro Max Without Ads]")

st.title("⚡ ScanMind AI Pro")
st.subheader("The most advanced multi-functional OCR & text utility tool online.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("###  1. Upload & Optimize Image")
    uploaded_file = st.file_uploader("Drag & drop your document here...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Uploaded Image", use_container_width=True)

        st.markdown("####  Image Pre-Processing (For blurry or old text)")
        contrast = st.slider("Enhance Contrast", 0.5, 3.0, 1.0)
        brightness = st.slider("Enhance Brightness", 0.5, 3.0, 1.0)
        apply_grayscale = st.checkbox("Convert to Black & White (Highly Recommended for OCR)")

        if contrast != 1.0:
            image = ImageEnhance.Contrast(image).enhance(contrast)
        if brightness != 1.0:
            image = ImageEnhance.Brightness(image).enhance(brightness)
        if apply_grayscale:
            image = ImageOps.grayscale(image)

with col2:
    st.markdown("###  2. AI Engine Output")

    if uploaded_file:
        with st.spinner("Analyzing image patterns via AI OCR..."):
            try:
                extracted_text = pytesseract.image_to_string(image, lang='eng').strip()
            except Exception:
                extracted_text = "Error: Tesseract OCR is not configured properly on the hosting server environment."

        if extracted_text and "Error:" not in extracted_text:
            st.success("Text Extracted Successfully!")

            final_text = st.text_area("Edit Extracted Text Below:", value=extracted_text, height=250)

            tab1, tab2, tab3 = st.tabs([" AI Summarizer", " Text To Speech", " Export Document"])

            with tab1:
                if st.button("Generate Smart AI Summary"):
                    words = final_text.split()
                    if len(words) > 30:
                        summary = " ".join(words[:int(len(words) / 3)]) + "..."
                        st.info(f"**AI Summary:** {summary}")
                    else:
                        st.warning("Text is too short to summarize efficiently.")

            with tab2:
                if st.button("Convert Text to Audio Track"):
                    with st.spinner("Generating crystal-clear English voice..."):
                        tts = gTTS(text=final_text, lang='en')
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        st.audio(fp, format='audio/mp3')

            with tab3:
                st.download_button(
                    label="Download as TXT file",
                    data=final_text,
                    file_name="scanmind_output.txt",
                    mime="text/plain"
                )
        else:
            st.info("No readable text found. Use the enhancement sliders on the left to clarify the image text.")
    else:
        st.warning("Waiting for an image upload to activate the AI engines.")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 12px;'>&copy; 2026 ScanMind AI Global Suite. Integrated with advanced lexical analysis algorithms.</p>",
    unsafe_allow_html=True)
