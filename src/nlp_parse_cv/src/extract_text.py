import pytesseract
from pdf2image import convert_from_path
import PyPDF2

class PDFTextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        text = ''

        # Try extracting text using PyPDF2
        # try:
        #     with open(self.file_path, 'rb') as file:
        #         reader = PyPDF2.PdfFileReader(file)
        #         for page in range(reader.numPages):
        #             text += reader.getPage(page).extract_text()
        # except Exception as e:
        #     print("Error reading PDF with PyPDF2:", e)
        #     text = ''

        # Check the length of the extracted text
        # if len(text) < 300:
            # If less than 300 letters, use OCR
        pages = convert_from_path(self.file_path, 300)
        ocr_text = ''
        for page_data in pages:
            ocr_text += pytesseract.image_to_string(page_data)
        return ocr_text

        # return text


# Example usage:
path = "/Users/levietduc/Documents/Documents - Le’s MacBook Pro/Learning/MLAI/misc/cvforscan/17. VU QUANG VINH.pdf"  # Replace with your actual folder path
extractor = PDFTextExtractor(path)
text = extractor.extract_text()
print(text)