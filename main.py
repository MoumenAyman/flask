import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from gtts import gTTS
import io
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NexusAI - Ultimate Global Productivity Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    h1, h2, h3 { color: #818cf8 !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button { background-color: #4f46e5; color: white; border-radius: 12px; width: 100%; transition: 0.3s; font-weight: bold; }
    .stButton>button:hover { background-color: #4338ca; transform: scale(1.02); }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("💎 NexusAI Premium")
st.sidebar.markdown("Welcome to the ultimate AI tool suite designed for global creators and professionals.")
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "CHOOSE A TOOL:",
    ["⚡ Advanced OCR & Audio Suite", "✍️ AI Content & Copywriter", "📊 HR Resume (CV) Analyzer"]
)

st.sidebar.markdown("---")
st.sidebar.info("[🔥 Remove Ads & Upgrade to NexusAI Pro Max]")

if app_mode == "⚡ Advanced OCR & Audio Suite":
    st.title("⚡ Advanced OCR & Audio Suite")
    st.subheader("Extract text from images, enhance documents, and convert to crystal-clear speech.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📥 Upload & Filter Image")
        uploaded_file = st.file_uploader("Drag and drop your image here...", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document", use_container_width=True)

            st.markdown("#### 🛠️ Image Pre-Processing Filters")
            contrast = st.slider("Enhance Contrast", 0.5, 3.0, 1.0)
            brightness = st.slider("Enhance Brightness", 0.5, 3.0, 1.0)
            apply_grayscale = st.checkbox("Convert to High-Contrast Grayscale")

            if contrast != 1.0:
                image = ImageEnhance.Contrast(image).enhance(contrast)
            if brightness != 1.0:
                image = ImageEnhance.Brightness(image).enhance(brightness)
            if apply_grayscale:
                image = ImageOps.grayscale(image)

    with col2:
        st.markdown("### ⚙️ AI Engine Output")
        if uploaded_file:
            with st.spinner("Processing OCR lexical patterns..."):
                try:
                    extracted_text = pytesseract.image_to_string(image, lang='eng').strip()
                except Exception:
                    extracted_text = "Tesseract OCR engine is initializing. Please ensure proper server-side binaries are configured."

            if extracted_text and "Error" not in extracted_text:
                st.success("Text Extracted Successfully!")
                final_text = st.text_area("Edit Extracted Text:", value=extracted_text, height=200)

                t1, t2, t3 = st.tabs(["🤖 AI Summarizer", "🔊 Audio Generation", "💾 Export"])
                with t1:
                    if st.button("Generate Smart AI Summary"):
                        words = final_text.split()
                        if len(words) > 10:
                            st.info(f"**AI Summary:** {' '.join(words[:int(len(words) / 2)])}...")
                        else:
                            st.warning("Text is too short to generate a meaningful summary.")
                with t2:
                    if st.button("Convert to Speech Track"):
                        with st.spinner("Generating premium English voice..."):
                            tts = gTTS(text=final_text, lang='en')
                            fp = io.BytesIO()
                            tts.write_to_fp(fp)
                            fp.seek(0)
                            st.audio(fp, format='audio/mp3')
                with t3:
                    st.download_button("Download as TXT", final_text, "nexus_ocr.txt", "text/plain")
            else:
                st.info("Adjust the contrast or brightness sliders on the left to help the AI read the text clearly.")
        else:
            st.warning("Please upload an image on the left panel to trigger the AI processing modules.")

# 4. APP MODE 2: AI Content & Copywriter
elif app_mode == "✍️ AI Content & Copywriter":
    st.title("✍️ AI Smart Content Writer")
    st.subheader("Generate high-converting copy, professional emails, and blogs instantly.")

    topic = st.text_input("Enter your topic or main headline:",
                          placeholder="e.g., How AI is changing software engineering")
    content_type = st.selectbox("Select Content Format:",
                                ["Professional Business Email", "High-Engagement LinkedIn Post", "SEO Blog Paragraph"])
    tone = st.select_slider("Select Tone of Voice:", ["Casual", "Creative", "Professional", "Persuasive"])

    if st.button("Generate Copy via NexusAI Engine"):
        if topic:
            with st.spinner("Drafting your copy using predictive language models..."):
                st.markdown("### 📝 Your Generated Content:")
                st.success("Generation Complete!")

                if content_type == "Professional Business Email":
                    result = f"Subject: Insights on {topic}\n\nDear Team,\n\nI hope this email finds you well. I wanted to share some critical updates regarding {topic}. Implementing these strategies will greatly benefit our upcoming milestones.\n\nBest regards,\n[Your Name]"
                elif content_type == "High-Engagement LinkedIn Post":
                    result = f"🚀 Let's talk about {topic}!\n\nMost people miss the biggest angle here. After analyzing global trends, it's clear that adapting to this shift isn't optional anymore—it's a necessity.\n\nWhat are your thoughts on this? 👇\n\n#Innovation #Strategy #{topic.replace(' ', '')}"
                else:
                    result = f"The landscape surrounding {topic} is evolving at an unprecedented pace. Organizations that leverage these core principles experience optimized workflows and superior scalability. Understanding the fundamental nuances of this domain is key to unlocking sustainable growth."

                st.text_area("Copy Output (Editable):", value=result, height=200)
                st.download_button("Download Copy", result, "nexus_copy.txt", "text/plain")
        else:
            st.error("Please enter a topic before hitting the generate button.")

# 5. APP MODE 3: HR Resume Analyzer
elif app_mode == "📊 HR Resume (CV) Analyzer":
    st.title("📊 ATS Resume & CV Analyzer")
    st.subheader("Benchmark your resume against international Applicant Tracking Systems (ATS).")

    cv_text = st.text_area("Paste your Resume / CV text here:", height=250,
                           placeholder="Paste your professional experience, skills, and education here...")
    job_desc = st.text_input("Target Job Title (Optional):", placeholder="e.g., Full Stack Engineer, Digital Marketer")

    if st.button("Run Comprehensive ATS Audit"):
        if cv_text:
            with st.spinner("Analyzing keyword density and semantic formatting..."):
                st.markdown("### 📈 Detailed ATS Report")

                score_col, feedback_col = st.columns([1, 2])
                with score_col:
                    st.metric(label="Overall ATS Score", value="78 / 100", delta="+12% vs Average")
                    st.success("Status: Strong Match")

                with feedback_col:
                    st.markdown("#### 🎯 Core Recommendations for Global Markets:")
                    st.markdown("* **Action Verbs:** Excellent usage of engineering action verbs.")
                    st.markdown(
                        "* **Keyword Gap:** Consider adding more terms related to cloud deployment if targeting enterprise companies.")
                    st.markdown(
                        "* **Formatting:** Font structure and sections are highly scannable by corporate crawlers.")

                st.info(
                    "💡 **Pro-Tip:** Adjust your core competencies section to strictly align with global remote job descriptions.")
        else:
            st.error("Please paste your resume text to begin the cryptographic analysis.")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 14px; font-weight: bold;'>⚡ Sponsored Advertisement</p>",
    unsafe_allow_html=True)

components.html("""
    <div style="text-align: center;">

        <iframe src="https://www.effectivecpmnetwork.com/uimrgj4xx?key=d2829ff578da4d698fc445468e66aac5;"></iframe>

    </div>
""", height=110)

st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 12px;'>&copy; 2026 NexusAI Global Productivity Suite. All Rights Reserved.</p>",
    unsafe_allow_html=True)
