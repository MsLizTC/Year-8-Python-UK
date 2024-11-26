import os
import time
import streamlit as st
import google.generativeai as genai
import PyPDF2  # Library to read PDF files

# Configure API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def extract_text_from_pdf(file_path):
    """Extract text from the uploaded PDF file."""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Upload and process the file
uploaded_file_path = "Unit guide_6_Introduction to Python programming_Y8_v1.2.pdf"
file_content = extract_text_from_pdf(uploaded_file_path)

# Define model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_output_tokens": 300,  # Limit response length
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="learnlm-1.5-pro-experimental",
    generation_config=generation_config,
    system_instruction=f"You are a helpful tutor. Use the following document content for context:\n\n{file_content}",
)

# Streamlit UI
st.title("AI Tutor Chatbot")
st.write("Ask the tutor questions about the unit, and it will guide you with context from the provided document.")

# User input
user_input = st.text_input("Enter your question for the tutor:")

if user_input:
    try:
        # Send user question to AI model
        response = model.generate_prompt(prompt=user_input)
        st.subheader("AI Tutor Response")
        st.write(response.text)

        # Generate a follow-up question based on the response
        follow_up_prompt = f"Based on the following context, ask a thought-provoking question: {response.text}"
        follow_up_response = model.generate_prompt(prompt=follow_up_prompt)
        st.subheader("Follow-up Question")
        st.write(follow_up_response.text)
    except Exception as e:
        st.error(f"Error: {e}")
