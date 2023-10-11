from fastapi import FastAPI, Form, Depends
import requests
import io
import PyPDF2
from PyPDF2 import PdfReader
import openai
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["http://localhost", "http://127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = None


openai.api_key = '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'  # Again, in a real deployment, use environment variables.

def get_answer_from_model(prompt, model_name="text-davinci-002"):
    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def perform_pypdf_ocr(pdf_file):
    pdf_text = ""
    pdf_reader = PdfReader(io.BytesIO(pdf_file))
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    return pdf_text

def perform_nougat_ocr(pdf_file):
    url = "https://0728-34-125-184-65.ngrok-free.app/predict"
    files = {'file': pdf_file}
    response = requests.post(url, files=files)
    return response.text if response.status_code == 200 else None

@app.post("/perform-ocr/")
def handle_ocr_request(url: str = Form(...), ocr_method: str = Form(...)):
    try:
        response = requests.get(url)
        pdf_content = response.content

        if ocr_method == "PyPDF":
            pdf_text = perform_pypdf_ocr(pdf_content)
            return {"status": "success", "ocr_output": pdf_text}
        elif ocr_method == "Nougat":
            nougat_text = perform_nougat_ocr(io.BytesIO(pdf_content))
            return {"status": "success", "ocr_output": nougat_text}
        else:
            return {"status": "error", "message": "Invalid OCR method"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/get-answer/")
def handle_question(question: str = Form(...), context: str = Form(...)):
    prompt = f"Given the following document: {context} {question}"
    answer = get_answer_from_model(prompt)
    return {"answer": answer}

def main():
    import uvicorn

    uvicorn.run("api:app", port=8503)


if __name__ == "__main__":
    main()