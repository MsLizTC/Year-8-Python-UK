import os
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
    system_instruction="Be a friendly, supportive tutor. Guide the student to meet their goals, gently\n"
                        "nudging them on task if they stray. Ask guiding questions to help your students\n"
                        "take incremental steps toward understanding big concepts, and ask probing\n"
                        "questions to help them dig deep into those ideas. Pose just one question per\n"
                        "conversation turn so you don't overwhelm the student. Wrap up this conversation\n"
                        "once the student has shown evidence of understanding.\n"
                        "The topic is from the Key Stage 3 Computer Science Curriculum for year 8 an Introduction to Python programming.",
)

# Initialize chat session in session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    "Let's begin! What's the difference between an algorithm and a programme?",
                ],
            },
        ]
    )

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit UI
st.title("Year 8 Python AI Tutor Chatbot")
st.write("Ask the tutor questions about the unit, and it will guide you with content from the provided document.")
st.write("Example questions:")
st.markdown("- What should I focus on when learning Python programming?\n- What's the difference between an algorithm and a programme?")

# Display previous conversation history
for turn in st.session_state.conversation_history:
    if turn["role"] == "user":
        st.subheader("You:")
    else:
        st.subheader("AI Tutor Response:")
    st.write(turn["text"])

# Handle user input
user_input = st.text_input("Enter your question or response for the tutor:")

if user_input:
    try:
        # Send user question to AI model
        response = st.session_state.chat_session.send_message(user_input)

        # Add the user input and AI response to the conversation history
        st.session_state.conversation_history.append({"role": "user", "text": user_input})
        st.session_state.conversation_history.append({"role": "model", "text": response.text})

        # Display AI response
        st.subheader("AI Tutor Response")
        st.write(response.text)

        # Generate a Socratic question based on the response
        socratic_prompt = f"Based on the student's answer: {response.text}, ask a Socratic question to deepen their understanding."
        socratic_response = st.session_state.chat_session.send_message(socratic_prompt)

        # Add Socratic question to the conversation history
        st.session_state.conversation_history.append({"role": "model", "text": socratic_response.text})

        # Display Socratic follow-up question
        st.subheader("Follow-up Question")
        st.write(socratic_response.text)
    except Exception as e:
        st.error(f"Error: {e}")
