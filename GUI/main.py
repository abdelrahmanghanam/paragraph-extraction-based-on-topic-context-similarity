import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QRadioButton, QLabel, \
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QHBoxLayout, QMessageBox, QButtonGroup
from pdf_extractor import PDF_Extractor
from paragraphs_filter import Paragraphs_Filter
from headline_generator import Headline_Generator
from pdf_writer import PDF_Writer
class SummaryWindow(QDialog):
    def __init__(self, pdf_path, selected_topic, similarity_method, topic_generation_method):
        paragraphs = PDF_Extractor().extract_paragraphs(pdf_path)
        result_paragraphs= []
        paragraphs_filter = Paragraphs_Filter()
        if similarity_method.lower() == "keyword matching":
            result_paragraphs = paragraphs_filter.extract_paragraphs_based_on_keywords(selected_topic,paragraphs)
        elif similarity_method.lower() == "scrapy":
            result_paragraphs = paragraphs_filter.extract_paragraphs_using_NLP(selected_topic, paragraphs)
        else:
            result_paragraphs = paragraphs_filter.extract_paragraphs_features_cosine_similarity(selected_topic,paragraphs)
        self.result_paragraphs_with_headline = []
        headline_generator = Headline_Generator()
        if topic_generation_method.lower() == "words occurence":
            self.result_paragraphs_with_headline = headline_generator.generate_headlines_using_word_occurence(result_paragraphs)
        else:
            self.result_paragraphs_with_headline = headline_generator.generate_headlines_using_cosine_similarity(result_paragraphs)
        super().__init__()
        self.init_ui(pdf_path, selected_topic, similarity_method, topic_generation_method)

    def init_ui(self, pdf_path, selected_topic, similarity_method, topic_generation_method):
        #create widgets
        file_path_label = QLabel(f"Selected PDF File: {pdf_path}")
        topic_label = QLabel(f"Selected Topic: {selected_topic}")
        method_label = QLabel(f"Chosen Similarity Method: {similarity_method}")
        generation_label = QLabel(f"Topic Generation Method: {topic_generation_method}")
        self.generate_pdf_button = QPushButton("Generate PDF file")

        #connections
        #connections
        self.generate_pdf_button.clicked.connect(self.generate_pdf)
        #create a table
        self.table = QTableWidget(self)

        #changed based on number of paragraphs
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.result_paragraphs_with_headline))
        self.table.setHorizontalHeaderLabels(["Topic", "Paragraph"])

        row = 0
        for value in self.result_paragraphs_with_headline:
            self.table.setItem(row, 0, QTableWidgetItem(value['headline']))
            self.table.setItem(row, 1, QTableWidgetItem(value['paragraph']))
            row += 1

        #layout
        layout = QVBoxLayout()
        layout.addWidget(file_path_label)
        layout.addWidget(topic_label)
        layout.addWidget(method_label)
        layout.addWidget(generation_label)
        layout.addWidget(self.table)
        layout.addWidget(self.generate_pdf_button)
        #set up the main layout
        self.setLayout(layout)
        #set up the main window
        self.setGeometry(400, 400, 500, 250)
        self.setWindowTitle('Summary Window')

    def generate_pdf(self):
        PDF_Writer().write_to_pdf(self.result_paragraphs_with_headline)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Success")
        msg_box.setText("PDF created successfully to file ./result.pdf")
        msg_box.exec_()
        self.close()


class PDFSummarizerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        #widgets
        self.file_path_label = QLabel("Selected PDF File: ")
        self.topic_edit = QLineEdit(self)
        self.upload_button = QPushButton("Upload PDF")
        self.summarize_button = QPushButton("Summarize")
        #create horizontal layout for the first radio group
        self.similarity_extraction_group = QRadioButton("Keyword Matching"), QRadioButton("Scrapy"), QRadioButton("BERT Model")
        self.similarity_extraction_radio_button_group = QButtonGroup(self)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(QLabel("Choose method for similarity measurement"))
        for radio_button in self.similarity_extraction_group:
            radio_layout.addWidget(radio_button)
            self.similarity_extraction_radio_button_group.addButton(radio_button)
        #create a new horizontal radio group for topic generation
        self.topic_generation_radio_group = QRadioButton("words occurence"), QRadioButton("similarity")
        self.topic_generation_radio_button_group = QButtonGroup(self)
        #create horizontal layout for the second radio group
        topic_generation_layout = QHBoxLayout()
        topic_generation_layout.addWidget(QLabel("Topic Generation"))
        for radio_button in self.topic_generation_radio_group:
            topic_generation_layout.addWidget(radio_button)
            self.topic_generation_radio_button_group.addButton(radio_button)
        #layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_path_label)
        layout.addLayout(radio_layout)
        layout.addLayout(topic_generation_layout)
        layout.addWidget(QLabel("Enter Topic:"))
        layout.addWidget(self.topic_edit)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.summarize_button)
        #connections
        self.upload_button.clicked.connect(self.upload_pdf)
        self.summarize_button.clicked.connect(self.open_summary_window)
        #set up the main layout
        self.setLayout(layout)
        #set up the main window
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('PDF Summarizer')
        #variables to store user selections
        self.selected_similarity_method = None
        self.selected_topic_generation_method = None


    def upload_pdf(self):
        selected_file, _ = QFileDialog.getOpenFileName(self, 'Open PDF File', '', 'PDF Files (*.pdf)')

        if selected_file:
            self.file_path_label.setText(f"Selected PDF File: {selected_file}")

    def open_summary_window(self):
        try:
            selected_file = self.file_path_label.text().replace("Selected PDF File: ", "")
            selected_similarity_method = [radio_button.text() for radio_button in self.similarity_extraction_group if
                                           radio_button.isChecked()][0]
            entered_topic = self.topic_edit.text()
            selected_topic_generation_method = [radio_button.text() for radio_button in self.topic_generation_radio_group if
                                                radio_button.isChecked()][0]
            #validation checks
            if not selected_file:
                self.show_error_message("Please choose a PDF file.")
            elif not entered_topic:
                self.show_error_message("Please enter a topic.")
            elif not selected_similarity_method:
                self.show_error_message("Please choose a similarity measurement method.")
            elif not selected_topic_generation_method:
                self.show_error_message("Please choose a topic generation method.")
            else:
                self.selected_similarity_method = selected_similarity_method[0]
                self.selected_topic_generation_method = selected_topic_generation_method[0]

                summary_window = SummaryWindow(selected_file,entered_topic,selected_similarity_method,selected_topic_generation_method)
                summary_window.exec_()
        except Exception as e:
            print(e)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFSummarizerGUI()
    window.show()
    sys.exit(app.exec_())
