import streamlit as st
import requests

st.title("Welcome to Streamlit - OCR")

# Initialize session state variables if they don't exist
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""

if 'question_prompt' not in st.session_state:
    st.session_state.question_prompt = ""

option = st.selectbox(
    "Which Package would you like to use?",
    ("Nougat", "PyPDF"),
    index=None,
    placeholder="Select OCR method...",
)
st.write('You selected:', option)

url = st.text_input('The PDF URL Link')
FASTAPI_ENDPOINT = "http://127.0.0.1:8503"

if st.button("Perform OCR"):
    if url:
        response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", data={"url": url, "ocr_method": option})
        result = response.json()

        if result["status"] == "success":
            st.write(f"OCR Output ({option}):")
            st.session_state.pdf_text = result["ocr_output"]
            st.write(st.session_state.pdf_text)

        else:
            st.error(result["message"])
    else:
        st.warning("Please enter a URL.")

# The text box for the question uses session_state
st.session_state.question_prompt = st.text_input('Write your question about the extracted text', st.session_state.question_prompt)

if st.button("Get Answer") and st.session_state.pdf_text and st.session_state.question_prompt:
    response = requests.post(f"{FASTAPI_ENDPOINT}/get-answer/",
                             data={"question": st.session_state.question_prompt, "context": st.session_state.pdf_text})
    answer_data = response.json()
    if "answer" in answer_data:
        st.write(f"Answer: {answer_data['answer']}")
    else:
        st.warning("Couldn't get an answer. Please try again.")
