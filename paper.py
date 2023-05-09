"""
A module to represent a paper.
Version: 0.1
Auther: Jingwen Liang
Date: 2023-04-21
"""
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import openai
from pathlib import Path
import logging
import re
import os
import tempfile
import fitz


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

class Paper:
    """
    A class to represent a paper.
    """
    def __init__(self,  url='', save_folder='', gpt_api_key='', pdf_input_path=""):
        if len(url) == 0 and len(pdf_input_path) == 0:
            raise ValueError("Please provide a url to fetch the paper or a path to your local paper.")
            return
        if len(url) !=0 and len(save_folder) == 0:
            raise ValueError("The save folder is empty.")
            return
        if len(gpt_api_key) == 0:
            raise ValueError("The GPT API key is empty.")
            return
        self.gpt_api_key = gpt_api_key
        self.url = url
        self.save_folder = Path(save_folder)
        self.pdf_input_path = pdf_input_path

        self.pdf_path = ""
        self.text = ""
        self.text_list = []
        self.title = ""
        self.authors = ""
        self.conference = ""
        self.model_structure_image = ""
        self.summary = ""
        self.abstract = ""
        self.language = "English"
        self.method = ""
        self.intro = ""
        self.chapter_names = []

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def fetch(self):
        if "arxiv.org/abs" in self.url:
            self.fetch_from_arxiv()
        elif self.url.lower().endswith("pdf"):
            self.fetch_from_pdf_url()
        elif self.pdf_input_path.lower().endswith("pdf"):
            self.pdf_path = self.pdf_input_path
            logging.info("Reading from local pdf file: %s", self.pdf_path)
        else:
            raise ValueError("The url of the paper is not supported.")

    def fetch_from_arxiv(self):
        """
        Fetch the paper from the arxiv abstract url. Get the paper information such as title, author, abstract, etc
        """
        logging.info(f"Fetching paper from URL:  %s", self.url)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.title = soup.find('h1', class_='title mathjax').text.replace("Title:", "").strip()
        valid_filename = re.sub(r'[\\/:"*?<>| \s]+', "_", self.title)

        author_elements = soup.find('div', {'class': 'authors'}).find_all('a')
        self.authors = ", ".join(a.get_text(strip=True) for a in author_elements)

        self.abstract = soup.find('blockquote', class_='abstract mathjax').text.replace("Abstract: ", "").strip()

        self.comments = soup.find('td', class_="tablecell comments mathjax").text.strip()
        self.conference = self.get_conferenct()
        self.save_folder = self.save_folder/valid_filename
        self.save_folder.mkdir(parents=True, exist_ok=True)
        self.pdf_path = self.save_folder / f"{valid_filename}.pdf"

        # pdf_link is extracted from the arXiv paper's abstract page using Beautiful Soup
        pdf_link = soup.find('a', class_='abs-button download-pdf')['href']

        # pdf_url is the url of the pdf file
        pdf_url = f"https://arxiv.org{pdf_link}"

        with requests.get(pdf_url) as r:
            with open(self.pdf_path, 'wb') as f:
                f.write(r.content)
        logging.info(f"Downloaded paper to %s", self.pdf_path)


    def get_conferenct(self):
        CONFERENCES = ["CVPR", "ICCV", "ECCV", "NIPS", "ICML", "AAAI", "IJCAI", "ACL", "EMNLP", "NAACL", "COLING", "ICASSP", "ICLR"]
        if self.comments:
            # get the conference name from the comments
            for conference in CONFERENCES:
                if conference in self.comments:
                    self.conference = conference
                    break


    def fetch_pdf(self):
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


    def parse(self):
        """
        Parse the paper.
        """
        logging.info("Parsing paper")
        with open(self.pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            # Extract text from the PDF
            for page_number, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                self.text_list.append(text)
            self.text = ' '.join(self.text_list)
        logging.info(f"Parsed PDF successfully")




    def summarize(self):
        """
        Summarize the paper.

        Args:
            gpt_api_key: The api key of the openai gpt-3.
        """
        logging.info("Summarizing paper")
        openai.api_key = self.gpt_api_key
        messages = [
            {"role": "system", "content": "You are a experienced AI researcher. You can read paper about "
                                          "state of the arts AI researchs and write summary about it methodology."},
            {"role": "user", "content": f"Please help me read the paper and write a summary about its methodology. The paper is here: {self.method}"},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        self.summary = response.choices[0].text.strip()
        for choice in response.choices:
            self.summary += choice.message.content
        print("summary_result:\n", self.summary)
        print("prompt_token_used:", response.usage.prompt_tokens,
              "completion_token_used:", response.usage.completion_tokens,
              "total_token_used:", response.usage.total_tokens)
        print("response_time:", response.response_ms/1000.0, 's')
        logging.info("Finished summarizing paper")

    def extract_main_figure(self):
        """
        Extract the main model structure figure
        """
        # use fitz to extract all the figures and their captions
        doc = fitz.open(self.pdf_path)

        # calcualte the number of pages in the PDF file
        page_count = len(doc)

        # create an empty list to store the figures and their captions
        figures = []

        # extract all images information from each page
        for page_num in range(page_count):
            page_content = doc[page_num]
            figures.extend(page_content.get_images())






