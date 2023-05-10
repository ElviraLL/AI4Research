from paper import Paper
import logging
import requests


class PdfPaper(Paper):
    def __init__(self, url, save_folder='',  pdf_input_path=""):
        super().__init__(url=url, save_folder=save_folder,  pdf_input_path=pdf_input_path)

    def fetch(self):
        """
        Fetch the paper from the url or local path.
        """
        if self.url.lower().endswith("pdf"):
            self.fetch_from_pdf_url()
        else:
            raise ValueError("The input path is not a pdf file.")
            return

    def fetch_from_pdf_url(self):
        """
        Fetch the paper from the given url, the url directly give you the pdf file, not the abs pages.
        We don't need to parse the title and abstract from the pdf file.
        """
        logging.info(f"Fetching paper from URL: %s", self.url)
        # Download the PDF to a temporary file
        with requests.get(self.url) as r:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(r.content)
                temp_pdf_path = temp_file.name

        # Extract the title from the PDF metadata
        with open(temp_pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            metadata = pdf_reader.getDocumentInfo()
            self.title = metadata.get('/Title', 'Untitled')

        # Replace invalid characters in the title
        valid_filename = re.sub(r'[\\/:"*?<>|\s]+', "_", self.title)
        self.save_folder = self.save_folder / valid_filename
        self.save_folder.mkdir(parents=True, exist_ok=True)

        # Update save_path with the title
        self.pdf_path = self.save_folder/"{valid_filename}.pdf"

        # Move the temporary PDF file to the final destination
        os.rename(temp_pdf_path, self.pdf_path)

        logging.info(f"Downloaded paper to %s", self.pdf_path)