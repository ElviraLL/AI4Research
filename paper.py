"""
A module to represent a paper.
Version: 0.1
Auther: Jingwen Liang
Date: 2023-04-21
"""
from pathlib import Path
import logging
from abc import abstractmethod
from collections import OrderedDict
import re

from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from collections import Counter
import numpy as np


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

class Paper:
    """
    A class to represent a paper.
    """
    def __init__(self,  url='', save_folder='',  pdf_input_path=""):
        if len(url) == 0 and len(pdf_input_path) == 0:
            raise ValueError("Please provide a url to fetch the paper or a path to your local paper.")
            return
        if len(url) != 0 and len(save_folder) == 0:
            raise ValueError("The save folder is empty.")
            return
        self.url = url
        self.save_folder = Path(save_folder)
        self.pdf_input_path = pdf_input_path

        self.pdf_path = ""

        self.title = ""
        self.authors = ""
        self.conference = ""
        self.model_structure_image = ""

        self.abstract = ""
        self.sections = {}
        self.subsections = {}
        self.pdf_dict = {}

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    @abstractmethod
    def fetch(self):
        """
        Fetch the paper from the url or local path.
        """
        pass

    def get_font_sizes(self):
        """
        Get the font sizes in the paper.
        The function first goes through the entire PDF document and gathers all font sizes. It does this by iterating
        over all the pages in the PDF document and processing each one with the PDFPageInterpreter and
        PDFPageAggregator. It then examines each layout object in the page layout. If the object is a LTTextBox (a block
        of text), it examines each text line in the box. If the text line is not empty, it appends the height (which
        corresponds to the font size) to the font_sizes list. Note that it ignores text in the area where the arXiv
        identifier typically appears (top left of the first page).
        """
        logging.info("Getting the font sizes in the paper.")
        if self.pdf_path == "":
            raise ValueError("The pdf file path is empty.")
            return
        with open(self.pdf_path, 'rb') as fp:
            # PDFParser object, takes a file-like object and extracts raw information from the PDF file.
            parser = PDFParser(fp)
            # PDFDocument object, represents the structure of a PDF document and is created from the PDFParser object
            doc = PDFDocument(parser)
            # PDFResourceManager object, stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice.
            rsrcmgr = PDFResourceManager()

            laparams = LAParams()
            # PDFPageAggregator object, takes a PDFPageInterpreter object and collects layout information from the interpreter.
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # PDFPageInterpreter object, processes the page contents and sends the information to a device (in this case, the PDFPageAggregator).
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # first, get all the font sizes in the document
            font_sizes = {}
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                for lobj in layout:
                    if isinstance(lobj, LTTextBox):
                        for obj in lobj:
                            if obj.get_text().strip():
                                # ignore the arxiv identifier TODO: need to find a better way to do this
                                if obj.width <= 21:
                                    continue
                                size = np.round(obj.height, decimals=2)
                                if size not in font_sizes:
                                    font_sizes[size] = [obj.get_text().strip()]
                                else:
                                    font_sizes[size].append(obj.get_text().strip())
            return font_sizes


    def get_sections(self):
        font_sizes = self.get_font_sizes()
        font_sizes = OrderedDict(sorted(font_sizes.items(), reverse=True))

        # put the pdf into a dictionary by hierarchy
        # step 1: get the font size of the title
        title_font_size = list(font_sizes.keys())[0]
        if not self.title:
            # it is possible that the title has two lines
            # TODO: we ignore the case where the title has more than two lines
            if len(font_sizes[title_font_size]) >= 2:
                self.title = font_sizes[title_font_size][0] + " " + font_sizes[title_font_size][1]

        # step 2: get the section names and subsection names using regular expressions
        pattern = re.compile(r'\d+(\.\d+)?\.\s+.+')  # TODO: only deal with the case where the section number is 1.1
        sections = []
        sec1_size = 0
        subsections = []
        for key, value in font_sizes.items():
            temp = []
            for text in value:
                match = pattern.match(text)
                if match:
                    temp.append(text)
            if len(temp) >= 3:
                if not sections:
                    sections = temp.copy()
                    sec1_size = key
                else:
                    if key < sec1_size:
                        subsections = temp.copy()
                    else:
                        subsections = sections.copy()
                        sections = temp.copy()
                        break
        sections.insert(0, "Abstract")
        self.sections = sections
        self.subsections = subsections


    def parse(self):
        """
        Parse the paper.
        """
        self.get_sections()
        pdf_dict = {}

        # Flatten the sections for easier lookup
        flat_sections = self.sections + self.subsections

        # Extract text from the PDF
        text = extract_text(self.pdf_path)

        # Split text into lines
        lines = text.split('\n')

        # Initialize variables
        current_section = None
        current_subsection = None

        # Iterate over lines
        for line in lines:
            # TODO: skip everything after the references section
            # TODO: skip page numbers
            # TODO: skip figures and tables
            if line == 'References':
                break
            # If line is a section header, start a new section
            if line in flat_sections:
                if line in self.sections:
                    current_section = line
                current_subsection = line
                pdf_dict.setdefault(current_section, {}).setdefault(current_subsection, [])
            # Otherwise, append line to current section
            elif current_section is not None:
                pdf_dict[current_section][current_subsection].append(line)

        self.pdf_dict = pdf_dict
        for section, subsections in pdf_dict.items():
            print(f'{section}:')
            for subsection, content in subsections.items():
                print(f'  {subsection}:')
                for line in content:
                    print(f'    {line}')













