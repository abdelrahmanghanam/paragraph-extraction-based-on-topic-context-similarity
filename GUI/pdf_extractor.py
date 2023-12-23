import fitz


class PDF_Extractor:

    def extract_paragraphs(self,pdf_path):
        paragraphs = []
        pdf_document = fitz.open(pdf_path)
        # iterate through pages
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            page_text = page.get_text("text")
            # split text into lines
            lines = [line.strip() for line in page_text.split('\n')]
            # concatenate lines into paragraphs
            current_paragraph = ""
            for line in lines:
                if line:
                    current_paragraph += line + " "
                else:
                    if current_paragraph:
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = ""
            # adding the last paragraph if not empty
            if current_paragraph:
                paragraphs.append(current_paragraph.strip())

        pdf_document.close()
        return paragraphs

