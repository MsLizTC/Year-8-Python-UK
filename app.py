import os
import time
import google.generativeai as genai
import streamlit as st

# Configure the generative AI API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the document content
file_content = "Unit guide content or extracted data here (replace with actual content)."

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="learnlm-1.5-pro-experimental",
    generation_config=generation_config,
    system_instruction=f"You are a helpful tutor. Use the following document content for context:\n\n{file_content}",
)

# Streamlit UI
st.title("Year 8 Python AI Tutor Chatbot")
st.write("Ask the tutor questions about the unit, and it will guide you with context from the provided document.")
st.write("Example questions:")
st.markdown("- What should I focus on when learning Python programming?\n- What's the difference between an algorithm and a programme?")

# Start a chat session and include an initial question in the history
chat_session = model.start_chat(
    history=[
        {
            "role": "model",
            "parts": [
                "Let's begin! What's the difference between an algorithm and a programme?",
            ],
        },
    ]
)

# Handle user input
user_input = st.text_input("Enter your question for the tutor:")

if user_input:
    try:
        # Send user question to AI model
        response = chat_session.send_message(user_input)
        st.subheader("AI Tutor Response")
        st.write(response.text)

        # Generate a follow-up question based on the response
        follow_up_prompt = f"Based on the following context, ask a thought-provoking question: {response.text}"
        follow_up_response = chat_session.send_message(follow_up_prompt)
        st.subheader("Follow-up Question")
        st.write(follow_up_response.text)
    except Exception as e:
        st.error(f"Error: {e}")
