from paper import Paper
import logging
import requests
from bs4 import BeautifulSoup
import re
import arxiv
from pathlib import Path

# TODO: conference

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger(__name__)
class ArxivPaper(Paper):
    def __init__(self, result: arxiv.Result=None, save_folder='', pdf_input_path='', url=''):
        if result:
            super().__init__(url="", save_folder=save_folder, pdf_input_path=pdf_input_path)
            self.url = result.entry_id
            self.pdf_path = ""
            self.title = result.title
            self.authors = [item.name for item in result.authors]
            self.conference = result.journal_ref
            self.abstract = result.summary
            self.categories = result.categories
            self.published = result.published
            self.comments = result.comment
            self.doi = result.doi
            self.fetch()
        elif url:
            super().__init__(url=url, save_folder=save_folder, pdf_input_path=pdf_input_path)
            self.comments = None
            self.fetch()
        else:
            raise ValueError("Cannot create paper object. Please provide more information!")


    def fetch(self):
        if "arxiv.org/abs" in self.url:
            self.fetch_from_arxiv()
        else:
            raise ValueError(f"The url {self.url} of the paper is not supported, please provide an arXiv paper url.")

    def fetch_from_arxiv(self):
        """
        Fetch the paper from the arxiv abstract url. Get the paper information such as title, author, abstract, etc
        """
        logger.info(f"Fetching paper from Arxiv:  %s", self.url)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.title = soup.find('h1', class_='title mathjax').text.replace("Title:", "").strip()
        valid_filename = re.sub(r'[\\/:"*?<>| \s]+', "_", self.title)

        author_elements = soup.find('div', {'class': 'authors'}).find_all('a')

        if not self.authors:
            self.authors = ', '.join(a.get_text(strip=True) for a in author_elements).split(', ')

        if not self.abstract:
            self.abstract = soup.find('blockquote', class_='abstract mathjax').text.replace("Abstract: ", "").strip()

        if not self.conference:
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


if __name__ == "__main__":
    paper = ArxivPaper(url="http://arxiv.org/abs/2307.10768v1")
    paper.parse()