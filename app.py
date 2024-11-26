import os
import time
import streamlit as st  # Added Streamlit
import google.generativeai as genai

# Set up Streamlit page
st.title("Year 8 Python Programming Tutor")
st.write("This app is designed to assist with teaching an introduction to Python programming for Year 8 students.")

# Configure the Generative AI API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        st.success(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        raise

def wait_for_files_active(files):
    """Waits for the given files to be active.

    Some files uploaded to the Gemini API need to be processed before they can be
    used as prompt inputs. The status can be seen by querying the file's "state"
    field.
    """
    try:
        st.info("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                st.write("Processing...")
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        st.success("All files processed successfully!")
    except Exception as e:
        st.error(f"Error processing files: {e}")
        raise

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="learnlm-1.5-pro-experimental",
        generation_config=generation_config,
        system_instruction="Be a friendly, supportive tutor. Guide the student to meet their goals, gently\n"
        "nudging them on task if they stray. Ask guiding questions to help your students\n"
        "take incremental steps toward understanding big concepts, and ask probing\n"
        "questions to help them dig deep into those ideas. Pose just one question per\n"
        "conversation turn so you don't overwhelm the student. Wrap up this conversation\n"
        "once the student has shown evidence of understanding.\n"
        "The topic is from the Key Stage 3 Computer Science Curriculum for year 8 an Introduction to Python programming",
    )
except Exception as e:
    st.error(f"Error creating model: {e}")
    raise

# Upload files and ensure they're processed
try:
    files = [
        upload_to_gemini("Unit guide_6_Introduction to Python programming_Y8_v1.2.pdf", mime_type="application/pdf"),
    ]
    wait_for_files_active(files)
except Exception as e:
    st.error(f"File upload or processing failed: {e}")

# Start chat session
try:
    chat_session = model.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    files[0],
                    "Looking at the Unit Overview, what do you think the main goal of this unit is?",
                ],
            },
        ]
    )

    # User input
    user_input = st.text_input("Enter your question for the tutor:")
    if user_input:
        response = chat_session.send_message(user_input)
        st.subheader("AI Tutor Response")
        st.write(response.text)
except Exception as e:
    st.error(f"Error during chat session: {e}")
