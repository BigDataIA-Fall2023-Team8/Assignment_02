# import streamlit as st
# import requests
# import pandas as pd

# st.title("PDF Analyzer: OCR and Q/A System")

# # Sidebar
# st.sidebar.title("Navigation")
# menu = ["Home", "OCR and Q/A System", "Document Summary", "About"]
# choice = st.sidebar.selectbox("Choose a section", menu)

# if st.sidebar.button("Reset Session"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.experimental_rerun()

# def home_section():
#     st.header("Welcome to the PDF Analyzer App")
#     st.write("Use this tool to extract text from PDFs and get answers from the extracted text. "
#              "Navigate through the sidebar to access different functionalities.")

# def ocr_qa_section():
#     st.header("OCR and Question/Answer System")

#     if 'pdf_text' not in st.session_state:
#         st.session_state.pdf_text = ""

#     input_methods = ["Upload a PDF file", "Provide a PDF URL Link"]
#     input_option = st.selectbox("Select input method", input_methods, index=int(st.session_state.get('input_option_index', 0)))
#     st.session_state['input_option_index'] = input_methods.index(input_option)

#     FASTAPI_ENDPOINT = "https://fastapi-assignment2-4fb0a78ad873.herokuapp.com"

#     uploaded_file = None  # Initialize uploaded_file as None

#     if input_option == "Upload a PDF file":
#         uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
#         if uploaded_file:
#             st.session_state.uploaded_file_name = uploaded_file.name
#         else:
#             st.write(f"Previously uploaded file: {st.session_state.get('uploaded_file_name', 'None')}")
#     else:
#         url = st.text_input('Provide the PDF URL Link', value=st.session_state.get('url', ''))
#         st.session_state.url = url

#     ocr_methods = ["Nougat", "PyPDF"]
#     if 'option_index' not in st.session_state:
#         st.session_state.option_index = 0
#     option = st.selectbox("Select OCR method", ocr_methods, index=st.session_state.option_index)
#     st.session_state.option_index = ocr_methods.index(option)

#     if st.button("Perform OCR") and (uploaded_file or st.session_state.url):
#         with st.spinner('Performing OCR...'):
#             if uploaded_file:
#                 uploaded_file_value = uploaded_file.getvalue()
#                 if uploaded_file_value:
#                     files = {"file": uploaded_file_value}
#                     response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", files=files, data={"ocr_method": option})
#                 else:
#                     st.warning("Please upload a PDF file.")
#                     return
#             else:
#                 if url:
#                     response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", data={"url": url, "ocr_method": option})
#                 else:
#                     st.warning("Please provide a PDF URL Link.")
#                     return

#             result = response.json()

#             if "status" in result and result["status"] == "success":
#                 st.session_state.pdf_text = result["ocr_output"]
#                 st.session_state.time_taken = result["summary"].get("time_taken_s", "N/A")
#                 st.session_state.characters_sent = result["summary"].get("input_length", "N/A")
#                 st.session_state.characters_received = result["summary"].get("output_length", "N/A")
#                 # Assuming number_of_pages needs to be added to the backend's response, you might want to adjust this accordingly
#                 st.session_state.number_of_pages = result["summary"].get("number_of_pages", "N/A")
#                 st.write("OCR Output:")
#                 st.write(st.session_state.pdf_text)

#                 # Question/Answer System
#                 if 'question_prompt' not in st.session_state:
#                     st.session_state.question_prompt = ""

#                 st.session_state.question_prompt = st.text_input('Question about the extracted text', st.session_state.question_prompt)

#                 if st.button("Get Answer") and st.session_state.pdf_text and st.session_state.question_prompt:
#                     with st.spinner('Finding answer...'):
#                         response = requests.post(f"{FASTAPI_ENDPOINT}/get-answer/",
#                                                  data={"question": st.session_state.question_prompt, "context": st.session_state.pdf_text})
#                         answer_data = response.json()
#                         if "answer" in answer_data:
#                             st.write(f"Answer: {answer_data['answer']}")
#                         else:
#                             st.warning("Couldn't get an answer. Please try again.")
#             else:
#                 st.error(f"OCR Failed. Response: {result}")


# def document_summary_section():
#     st.header("Document Summary")
    
#     if 'time_taken' in st.session_state:
#         summary_data = {
#             "Metric": ["Time taken for OCR", "Characters sent for OCR", "Characters received after OCR", "Number of pages obtained"],
#             "Value": [st.session_state.time_taken, st.session_state.characters_sent, st.session_state.characters_received, st.session_state.number_of_pages]
#         }
        
#         summary_df = pd.DataFrame(summary_data)
#         st.dataframe(summary_df.style.set_properties(**{'text-align': 'left'}))
#     else:
#         st.write("Summary of the last document processed will appear here.")

# def about_section():
#     st.header("About PDF Analyzer")
#     st.write("This application allows users to extract text from PDF files and ask questions related to the extracted text.")

# # Mapping sections to functions
# sections = {
#     "Home": home_section,
#     "OCR and Q/A System": ocr_qa_section,
#     "Document Summary": document_summary_section,
#     "About": about_section
# }

# # Running the appropriate section
# sections[choice]()

import streamlit as st
import requests
import pandas as pd

st.title("PDF Analyzer: OCR and Q/A System")

# Sidebar
st.sidebar.title("Navigation")
menu = ["Home", "OCR and Q/A System", "Document Summary", "About"]
choice = st.sidebar.selectbox("Choose a section", menu)

if st.sidebar.button("Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def split_into_chunks(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def home_section():
    st.header("Welcome to the PDF Analyzer App")
    st.write("Use this tool to extract text from PDFs and get answers from the extracted text. "
             "Navigate through the sidebar to access different functionalities.")

def ocr_qa_section():
    st.header("OCR and Question/Answer System")

    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = ""
        st.session_state.chunks = []

    input_methods = ["Upload a PDF file", "Provide a PDF URL Link"]
    input_option = st.selectbox("Select input method", input_methods, index=int(st.session_state.get('input_option_index', 0)))
    st.session_state['input_option_index'] = input_methods.index(input_option)

    FASTAPI_ENDPOINT = "https://fastapi-assignment2-4fb0a78ad873.herokuapp.com"

    uploaded_file = None

    if input_option == "Upload a PDF file":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file:
            st.session_state.uploaded_file_name = uploaded_file.name
        else:
            st.write(f"Previously uploaded file: {st.session_state.get('uploaded_file_name', 'None')}")
    else:
        url = st.text_input('Provide the PDF URL Link', value=st.session_state.get('url', ''))
        st.session_state.url = url

    ocr_methods = ["Nougat", "PyPDF"]
    option = st.selectbox("Select OCR method", ocr_methods, index=st.session_state.option_index)
    st.session_state.option_index = ocr_methods.index(option)

    if st.button("Perform OCR") and (uploaded_file or st.session_state.url):
        with st.spinner('Performing OCR...'):
            if uploaded_file:
                uploaded_file_value = uploaded_file.getvalue()
                if uploaded_file_value:
                    files = {"file": uploaded_file_value}
                    response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", files=files, data={"ocr_method": option})
            else:
                response = requests.post(f"{FASTAPI_ENDPOINT}/perform-ocr/", data={"url": st.session_state.url, "ocr_method": option})

            result = response.json()

            if "status" in result and result["status"] == "success":
                st.session_state.pdf_text = result["ocr_output"]
                st.session_state.chunks = split_into_chunks(st.session_state.pdf_text)

                # Displaying OCR Output
                st.write("OCR Output:")
                st.write(st.session_state.pdf_text)

                # Question/Answer System
                question_prompt = st.text_input('Question about the extracted text')
                if st.button("Get Answer") and question_prompt:
                    with st.spinner('Finding answer...'):
                        context_to_send = "\n".join(st.session_state.chunks[-4:])  # Sending the last 4 chunks for context
                        response = requests.post(f"{FASTAPI_ENDPOINT}/get-answer/",
                                                 data={"question": question_prompt, "context": context_to_send})
                        answer_data = response.json()
                        if "answer" in answer_data:
                            st.write(f"Answer: {answer_data['answer']}")
                        else:
                            st.warning("Couldn't get an answer. Please try again.")
            else:
                st.error(f"OCR Failed. Response: {result}")

def document_summary_section():
    st.header("Document Summary")
    
    if 'time_taken' in st.session_state:
        summary_data = {
            "Metric": ["Time taken for OCR", "Characters sent for OCR", "Characters received after OCR", "Number of pages obtained"],
            "Value": [st.session_state.time_taken, st.session_state.characters_sent, st.session_state.characters_received, st.session_state.number_of_pages]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df.style.set_properties(**{'text-align': 'left'}))
    else:
        st.write("Summary of the last document processed will appear here.")

def about_section():
    st.header("About PDF Analyzer")
    st.write("This application allows users to extract text from PDF files and ask questions related to the extracted text.")

# Mapping sections to functions
sections = {
    "Home": home_section,
    "OCR and Q/A System": ocr_qa_section,
    "Document Summary": document_summary_section,
    "About": about_section
}

# Running the appropriate section
sections[choice]()

