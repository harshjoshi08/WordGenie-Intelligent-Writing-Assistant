import streamlit as st
import google.generativeai as genai
import time
from apikey import google_gemini_api_key

# from apikey import openai_api_key
# from openai import OpenAI

from google.api_core.exceptions import ResourceExhausted

# client = OpenAI(api_key=openai_api_key)

genai.configure(api_key=google_gemini_api_key)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    generation_config=generation_config,
    safety_settings=safety_settings
)

st.set_page_config(layout="wide")

st.title("🪄 WordGenie: Your Intelligent Writing Assistant")
st.subheader("Unleash Your Creativity with AI-Powered Writing Assistance")

# Sidebar
with st.sidebar:
    st.title("Your Writing Preferences")

    blog_title = st.text_input("Title")
    keywords = st.text_input("Keywords (comma separated)")
    num_words = st.slider("Number of Words", 100, 2000, 500, 250)
    num_images = st.slider("Number of Images", 0, 10, 3, 1)

    submit = st.button("Generate Content")

# Function to safely call Gemini
def generate_with_retry(prompt, retries=5):
    for attempt in range(retries):
        try:
            return model.generate_content(prompt)
        except ResourceExhausted as e:
            wait_time = 60  # wait 60 seconds
            st.warning(f"Quota exceeded. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
    st.error("Daily quota exceeded. Please upgrade plan or try tomorrow.")
    return None

# Run only when button clicked
if submit:

    prompt_part = f"""
    Write a blog post on the topic '{blog_title}'
    incorporating the following keywords: {keywords}.
    The blog post should be approximately {num_words} words long
    and include {num_images} relevant images.
    """

    with st.spinner("Generating blog content..."):
        response = generate_with_retry(prompt_part)

    if response:
        st.title("Your Generated Blog Post:")
        st.write(response.text)

        images = []

# By removing this comment you can enable image generation, but be mindful of the quota limits as it may lead to ResourceExhausted errors.
        # for i in range(num_images):
        #     image_response = client.images.generate(
        #         model="dall-e-3",
        #         prompt=f"Generate an image related to the blog topic '{blog_title}'",
        #         size="1024x1024",
        #         quality="standard",
        #         n=1,
        #     )
        #     images.append(image_response.data[0].url)

        # for img in images:
        #     st.image(img)
