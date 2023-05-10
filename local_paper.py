from paper import Paper
import logging

class PdfPaper(Paper):
    def __init__(self, save_folder='', pdf_input_path=""):
        super().__init__(url="", save_folder=save_folder,  pdf_input_path=pdf_input_path)

    def fetch(self):
        """
        Fetch the paper from the url or local path.
        """
        if self.pdf_input_path.lower().endswith("pdf"):
            self.pdf_path = self.pdf_input_path
            logging.info("Reading from local pdf file: %s", self.pdf_path)
        else:
            raise ValueError("The input path is not a pdf file.")
            return