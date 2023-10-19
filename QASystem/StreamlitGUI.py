import streamlit as st
import requests
import pandas as pd

# Initialize session state variables if they don't exist
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

st.title("PDF Analyzer: OCR and Q/A System")

# Sidebar
st.sidebar.title("Navigation")
menu = ["Home", "Perform OCR", "Q/A System", "Document Summary", "About"]
choice = st.sidebar.selectbox("Choose a section", menu)

if st.sidebar.button("Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def home_section():
    st.header("Welcome to the PDF Analyzer App")
    st.write("Use this tool to extract text from PDFs and get answers from the extracted text. Navigate through the sidebar to access different functionalities.")

def perform_ocr_section():
    st.header("Perform OCR")

    FASTAPI_ENDPOINT = "https://fastapi-assignment2-4fb0a78ad873.herokuapp.com"

    input_methods = ["Upload a PDF file", "Provide a PDF URL Link"]
    input_option = st.selectbox("Select input method", input_methods)

    ocr_methods = ["Nougat", "PyPDF"]
    option = st.selectbox("Select OCR method", ocr_methods)

    uploaded_file = None
    url = None
    if input_option == "Upload a PDF file":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    else:
        url = st.text_input('Provide the PDF URL Link')

    if st.button("Perform OCR"):
        with st.spinner('Performing OCR...'):
            if uploaded_file:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", files=files, data={"ocr_method": option})
            else:
                response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", data={"url": url, "ocr_method": option})

            result = response.json()

            if "status" in result and result["status"] == "success":
                st.session_state.pdf_text = result["ocr_output"]
                st.write("OCR Output:")
                st.write(st.session_state.pdf_text)

                # Storing the summary data in st.session_state
                st.session_state.time_taken = result["summary"]["time_taken_s"]
                st.session_state.characters_sent = result["summary"]["input_length"]
                st.session_state.characters_received = result["summary"]["output_length"]
                # NOTE: Your backend doesn't seem to be returning a 'number_of_pages' key
                st.session_state.number_of_pages = result["summary"]["number_of_pages"]  # Assuming you'll add this in the backend

def qa_section():
    st.header("Question/Answer System")

    # If no text has been extracted, inform the user
    if not st.session_state.pdf_text:
        st.write("Please perform OCR on a PDF first to extract text.")
        return

    # Display previous conversation
    for item in st.session_state.conversation:
        if item["role"] == "user":
            st.write(f"You: {item['content']}")
        else:
            st.write(f"AI: {item['content']}")

    FASTAPI_ENDPOINT = "https://fastapi-assignment2-4fb0a78ad873.herokuapp.com"
    question = st.text_input('Enter your question:')
    if st.button("Get Answer"):
        st.session_state.conversation.append({"role": "user", "content": question})

        with st.spinner('Finding answer...'):
            data = {
                "question": question,
                "context": st.session_state.pdf_text
            }
            response = requests.post(f"{FASTAPI_ENDPOINT}/get-answer/", data=data)
            answer_data = response.json()

            if "answer" in answer_data:
                answer = answer_data['answer']
                st.session_state.conversation.append({"role": "ai", "content": answer})

            # Refresh the page to clear the input box and show the updated conversation
            st.experimental_rerun()

def document_summary_section():
    st.header("Document Summary")

    if 'time_taken' in st.session_state:
        summary_data = {
            "Metrics": [
                "Time taken for OCR (sec.)",
                "Characters sent for OCR",
                "Characters received after OCR",
                "Number of pages obtained"  # Uncomment if you add this in the backend
            ],
            "Values": [
                st.session_state.time_taken,
                st.session_state.characters_sent,
                st.session_state.characters_received,
                st.session_state.number_of_pages  # Uncomment if you add this in the backend
            ]
        }

        summary_df = pd.DataFrame(summary_data)

        # Use st.table() for better table formatting
        st.table(summary_df.set_index('Metrics'))

        # Optionally, add some additional descriptive text if necessary
        st.write("Note: Metrics and values are based on the most recent OCR operation.")

    else:
        st.write("Summary of the last document processed will appear here.")

def about_section():
    st.header("About PDF Analyzer")
    st.write("This application allows users to extract text from PDF files and ask questions related to the extracted text.")

# Mapping sections to functions
sections = {
    "Home": home_section,
    "Perform OCR": perform_ocr_section,
    "Q/A System": qa_section,
    "Document Summary": document_summary_section,
    "About": about_section
}

# Running the appropriate section
sections[choice]()
