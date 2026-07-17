from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


if __name__ == "__main__":

    pdf_path = input("Enter the path of your resume PDF: ")

    resume_text = extract_text_from_pdf(pdf_path)

    print("\n===== Extracted Resume Text =====\n")
    print(resume_text)