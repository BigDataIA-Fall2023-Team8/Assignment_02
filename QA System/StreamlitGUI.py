import streamlit as st
import requests
import time

st.title("PDF Analyzer: OCR and Q/A System")

st.sidebar.title("Navigation")
menu = ["Home", "OCR and Q/A System", "Document Summary", "About"]
choice = st.sidebar.selectbox("Choose a section", menu)

if choice == "Home":
    st.header("Welcome to the PDF Analyzer App")
    st.write("Use this tool to extract text from PDFs and get answers from the extracted text. "
             "Navigate through the sidebar to access different functionalities.")

elif choice == "OCR and Q/A System":
    st.header("OCR and Question/Answer System")

    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = ""

    option = st.selectbox("Select OCR method", ("Nougat", "PyPDF"), placeholder="Select OCR method...")
    url = st.text_input('Provide the PDF URL Link')
    uploaded_file = st.file_uploader("Or upload a PDF file", type=["pdf"])

    FASTAPI_ENDPOINT = "http://127.0.0.1:8504"

    if st.button("Perform OCR"):
        with st.spinner('Performing OCR...'):
            start_time = time.time()
            if uploaded_file:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", files=files, data={"ocr_method": option})
            elif url:
                response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", data={"url": url, "ocr_method": option})
            else:
                st.warning("Please provide a URL or upload a file.")
                st.stop()
                
            result = response.json()
            end_time = time.time()
            
            if result["status"] == "success":
                st.success(f"OCR completed in {end_time - start_time:.2f} seconds.")
                st.session_state.pdf_text = result["ocr_output"]
                st.write("OCR Output:")
                st.write(st.session_state.pdf_text)
            

            else:
                st.error(f"OCR Failed. Response: {result}")

    if 'question_prompt' not in st.session_state:
        st.session_state.question_prompt = ""
    
    st.session_state.question_prompt = st.text_input('Question about the extracted text', st.session_state.question_prompt)
    
    if st.button("Get Answer") and st.session_state.pdf_text and st.session_state.question_prompt:
        with st.spinner('Finding answer...'):
            response = requests.post(f"{FASTAPI_ENDPOINT}/get-answer/",
                                     data={"question": st.session_state.question_prompt, "context": st.session_state.pdf_text})
            answer_data = response.json()
            if "answer" in answer_data:
                st.write(f"Answer: {answer_data['answer']}")
            else:
                st.warning("Couldn't get an answer. Please try again.")

elif choice == "Document Summary":
    st.header("Document Summary")
    st.write("Summary of the last document processed will appear here.")
    # Display the document summary after processing a document through OCR

elif choice == "About":
    st.header("About PDF Analyzer")
    st.write("This application allows users to extract text from PDF files and ask questions related to the extracted text.")

# Add more sections as per your requirements
