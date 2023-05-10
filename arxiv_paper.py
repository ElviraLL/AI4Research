from paper import Paper
import logging
import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path


logger = logging.getLogger(__name__)
class ArxivPaper(Paper):
    def __init__(selfself, url='', save_folder='',  pdf_input_path=""):
        super().__init__(url, save_folder, pdf_input_path)


    def fetch(self):
        if "arxiv.org/abs" in self.url:
            self.fetch_from_arxiv()
        else:
            raise ValueError("The url of the paper is not supported, please provide an arXiv paper url.")

    def fetch_from_arxiv(self):
        """
        Fetch the paper from the arxiv abstract url. Get the paper information such as title, author, abstract, etc
        """
        logger.info(f"Fetching paper from URL:  %s", self.url)
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