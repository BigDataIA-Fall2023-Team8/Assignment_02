# Assignment_02

## Setup Instructions

Follow the steps below to get the project up and running:

#### 1. Clone the Repository
Clone this GitHub repository to your local machine.

#### 2. Navigate to the File
Open `Assignment_02 > QASystem > StreamlitGUI.py` in your preferred IDE. We recommend [Visual Studio Code (VSCode)](https://code.visualstudio.com/).

#### 3. Open the Integrated Terminal
Within your IDE, access the integrated terminal.
* Open the integrated terminal for the folder and run the comman > streamlit run StreamlitGUI.py

## Link to the app:
-----------------

#### [OCRSystem](https://ocrsystem.streamlit.app/)

## Link to the Replication of Notebooks
-----------------
#### [Replicating the 3 Notebooks](https://colab.research.google.com/drive/1qDuPLMXII3JL0Dr5mn0AO3IApohYkv1I?usp=sharing)

## Project Flow
-----------------

#### User Interface

- The user interacts with a Streamlit web application.
- On the left-hand side, there is a navigation pane with different options.

#### Option Selection

- The user selects an option from the navigation pane.
- For this description, we focus on two specific options: "OCR" and "Q/A System."

#### OCR Option

- After selecting the "OCR" option, the user is presented with the choice to upload a PDF file or provide a PDF URL link.

#### File Upload or URL Input

- If the user chooses to upload a file, they can select and upload a PDF document.
- If they opt for a URL, they can provide a link to an online PDF document.

#### OCR Method Selection

- Following the file upload or URL input, the user is prompted to choose an OCR method. Two methods are available: "Nougat" and "PyPdf."

#### Perform OCR

- After selecting an OCR method, the user initiates the OCR process by clicking on the "Perform OCR" button.

#### Summary Generation

- The system processes the PDF document using the selected OCR method and generates a summary of the content.

#### Question Input

- The user is then able to enter any questions they have about the content of the article.

## About Code:
-----------------
#### There are two major code files, one is the frontend and second is the backend.

##### Frontend - StreamlitGUI.py
The code defines several functions, each corresponding to a section of the application:

home_section(): Provides a welcome message and introduction to the application.

ocr_qa_section(): Handles the OCR (Optical Character Recognition) process, allowing users to upload PDF files or provide PDF URL links, extract text, and perform Q&A on the extracted text.

document_summary_section(): Displays a summary of the OCR process, including time taken, characters sent and received, and the number of pages obtained.

about_section(): Offers information about the application.

##### Backend - api.py
This is the backend where the actual business logic has been coded as well as the fastapi code has been written here.

It serves as an API for performing Optical Character Recognition (OCR) on PDF documents. It allows users to submit PDFs for OCR processing using different methods, such as PyPDF (a Python PDF library) and Nougat.

OpenAI Configuration: The OpenAI API key is set to use OpenAI services for answering questions.

get_answer_from_model Function: This function sends a text prompt to the OpenAI engine (ChatGPT3.5Turboi) and retrieves an answer. The prompt is constructed by combining a user's question with a context from a document.

perform_pypdf_ocr Function: This function performs OCR on a PDF using the PyPDF2 library. It extracts text from each page of the PDF and provides a summary of the operation, including time taken, character counts, and page counts.

perform_nougat_ocr Function: This function sends a PDF to an external Nougat OCR API for text extraction. It handles making the HTTP request, timing the operation, and parsing the response. It also provides a summary of the operation.

handle_ocr_request Endpoint: This FastAPI route handles OCR requests. It accepts a URL or an uploaded PDF file, specifies the OCR method (either "PyPDF" or "Nougat"), and then performs OCR using the chosen method. It records the time taken and returns the OCR output along with a summary.

handle_question Endpoint: This route handles questions. It accepts a question and context, constructs a prompt, sends it to the OpenAI engine, and returns the answer.

read_root Endpoint: A simple root endpoint that returns a "Hello" message when accessed.

## Structure:
-----------------
```
.
├── LICENSE
├── QASystem
│   ├── Nougat_API_Hosting.ipynb
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── Procfile
│   ├── Replicating_the_QAsystem.ipynb
│   ├── Replicating_the_QAsystem.ipynbZone.Identifier
│   ├── StreamlitGUI.py
│   ├── __pycache__
│   ├── api.py
│   ├── node_modules
│   ├── package-lock.json
│   ├── package.json
│   ├── qa_bot.png
│   └── qa_bot.pngZone.Identifier
└── README.md
```

## Additional Notes:
---------------
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.

| Name            | Percentage | Responsibilities                                 |
|-----------------|------------|-------------------------------------------------|
| Soham Deshpande | 33%        | OpenAI Config., Streamlit UI Design, Heroku Implementation |
| Tanmay Zope     | 33%        | Notebooks Replication, Architecture Diagram, OpenAI Config. |
| Anvi Jain       | 33%        | Notebooks Replication, Readme File, Technical Documentation  |



