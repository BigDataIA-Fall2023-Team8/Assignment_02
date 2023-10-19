from fastapi import FastAPI, Form, UploadFile, File
import requests
import io
import time
from PyPDF2 import PdfReader
import openai
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:8501",
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = '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'  # Replace with your OpenAI API key.

def get_answer_from_model(prompt, model_name="text-davinci-002"):
    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def perform_pypdf_ocr(pdf_file):
    start_time = time.time()
    pdf_text = []
    pdf_reader = PdfReader(io.BytesIO(pdf_file))
    initial_page_count = len(pdf_reader.pages)

    for page_num in range(initial_page_count):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        pdf_text.append(f"Page {page_num + 1}:\n{page_text}\n")

    extracted_text = '\n'.join(pdf_text)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Create a summary of the operation
    summary = {
        'Time_Taken_seconds': elapsed_time,
        'characters_sent': len(pdf_file),
        'characters_received': len(extracted_text),
        'initial_page_count': initial_page_count,
        'processed_page_count': initial_page_count  # assuming all pages are processed
    }

    #summary_str = "\n\n" + "\n".join([f"{key}: {value}" for key, value in summary.items()])
    #extracted_text += summary_str

    return extracted_text

def perform_nougat_ocr(pdf_file):
    nougat_url = "https://7ee3-35-204-119-38.ngrok-free.app/predict"  # Update as per your configuration

    # Ensure the file object is in the correct format for requests (bytes).
    if not isinstance(pdf_file, bytes):
        pdf_file = pdf_file.read()
    
    files = {'file': ("document.pdf", pdf_file)}  # Named tuple to ensure correct handling by API
    
    start_time = time.time()  # Start timing the OCR process
    
    try:
        # Send the request to the Nougat OCR API
        response = requests.post(nougat_url, files=files)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, {"error": str(e), "duration": 0, "num_pages": 0}
    
    end_time = time.time()  # End timing
    duration = end_time - start_time  # Calculate duration
    

    # Check for successful status code
    if response.status_code == 200:
        # Logic to extract page number information (adjust based on actual API response structure)
        ocr_text =  response.json()
        num_pages = ocr_text.count("Page:")  # Example logic, adjust as needed
        
        summary = {
            "Duration": duration,
            "Num of Pages": num_pages,
            "Characters sent": len(pdf_file),
            "Chars Received": len(ocr_text),
        }

        #summary_str = "\n\n" + "\n".join([f"{key}: {value}" for key, value in summary.items()])
        #ocr_text += summary_str

        return ocr_text  # Return the OCR text and the summary
        #return {"ocr_text": ocr_text, "summary": summary}
    else:
        print(f"Failed to perform OCR. Status code: {response.status_code}, Response: {response.text}")
        return None, {"error": response.text, "duration": duration, "num_pages": 0}

@app.post("/perform-ocr/")
async def handle_ocr_request(url: str = Form(None), ocr_method: str = Form(...), file: UploadFile = File(None)):
    try:
        logging.info(f"Received OCR request: url={url}, ocr_method={ocr_method}, file={file}")

        # Initialize time and content placeholders
        start_time = time.time()
        pdf_content = None

        # Retrieve PDF content
        if file:
            pdf_content = await file.read()
        elif url:
            response = requests.get(url)
            pdf_content = response.content
        else:
            return {"status": "error", "message": "Neither a URL nor a file was provided."}

        # Perform OCR
        if ocr_method == "PyPDF":
            pdf_text = perform_pypdf_ocr(pdf_content)
        elif ocr_method == "Nougat":
            pdf_text = perform_nougat_ocr(io.BytesIO(pdf_content))
        else:
            return {"status": "error", "message": "Invalid OCR method"}

        # Compute elapsed time and log
        elapsed_time = time.time() - start_time
        logging.info(f"OCR successful. Method: {ocr_method}, Time taken: {elapsed_time:.2f} s")

        return {
            "status": "success",
            "ocr_output": pdf_text,
            "summary": {
                "ocr_method": ocr_method,
                "time_taken_s": elapsed_time,
                "input_length": len(pdf_content),
                "output_length": len(pdf_text)
            }
        }

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}", exc_info=True)  # Logging the full exception details
        return {"status": "error", "message": str(e)}

@app.post("/get-answer/")
def handle_question(question: str = Form(...), context: str = Form(...)):
    prompt = f"Given the following document: {context} {question}"
    answer = get_answer_from_model(prompt)
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}


# def main():
#     import uvicorn

#     uvicorn.run("api:app", port=8504)

# if __name__ == "__main__":
#     main()

