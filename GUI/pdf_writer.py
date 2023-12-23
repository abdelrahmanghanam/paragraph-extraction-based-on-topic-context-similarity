import aspose.pdf as pdf


class PDF_Writer:

    def write_to_pdf(self,paragraphs_with_topics):
        pdfFile = pdf.Document()
        newPage = pdfFile.pages.add()
        table = pdf.Table()
        table.default_cell_border = pdf.BorderInfo(pdf.BorderSide.ALL)
        table.default_column_width = '200'
        print("in")
        for value in paragraphs_with_topics:
            row = table.rows.add()
            row.cells.add(value['headline'])
            row.cells.add(value['paragraph'])
        newPage.paragraphs.add(table)
        pdfFile.save("result.pdf")
        print("table in PDF created successfully")
