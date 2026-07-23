import re
from io import BytesIO
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_source):
    """
    Extracts and normalizes text from a PDF file path or file-like object (BytesIO).
    """
    try:
        reader = PdfReader(pdf_source)
        extracted_text = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        full_text = "\n".join(extracted_text)

        # Clean non-printable / control characters and normalize whitespace
        full_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', full_text)
        full_text = re.sub(r'[ \t]+', ' ', full_text)
        full_text = re.sub(r'\n+', '\n', full_text).strip()

        return full_text
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {str(e)}")


if __name__ == "__main__":
    pdf_path = input("Enter the path of your resume PDF: ")
    resume_text = extract_text_from_pdf(pdf_path)
    print("\n===== Extracted Resume Text =====\n")
    print(resume_text[:1000])