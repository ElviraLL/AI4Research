"""
A module communicates with ChatGPT and reads the paper.
Version: 0.1
Auther: Jingwen Liang
Date: 2023-04-21
"""
import os
import logging

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


from paper_arxiv import ArxivPaper
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

logger = logging.getLogger(__name__)


class PaperReader:
    def __init__(self, paper=None):
        self.paper = paper
        self.chat = ChatOpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY)

    def set_paper(self, paper):
        self.paper = paper

    def get_paper(self):
        if self.paper:
            return self.paper.title
        else:
            raise "The paper hasn't been set yet!"

    def get_summary_langchain(self):
        """
        Summarize the paper using langchain.
        """

        summary_template = """\
        You are an experienced AI Research that helps reading the papers.
        Providing the abstract and conclusion of an AI / Machine Learning paper, extract the following information:
        
        Research Objectives: What is this paper doing, What is the main objective of this research paper, what problem did it solve?
        Research Outcomes: What is the conclusion of this paper?
        Methods: What is the main method does the paper proposed?
                
        abstract:{abstract}
        conclusion:{conclusion}
        {format_instructions}
        """

        objectives_schema = ResponseSchema(
            name="objectives",
            description="What is this paper doing? What is the main objective of this research paper? what problem did it solve?"
        )
        conclusion_schema = ResponseSchema(
            name="conclusion",
            description="What is the conclusion of this paper?"
        )
        methods_schema = ResponseSchema(
            name="methods",
            description="What method does this paper propose to achieve the objectives?"
        )

        response_schemas = [objectives_schema, conclusion_schema, methods_schema]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        prompt = ChatPromptTemplate.from_template(template=summary_template)

        paper_abstract = self.paper.abstract
        paper_conclusion = self.paper.conclusion
        messages = prompt.format_messages(
            abstract=paper_abstract,
            conclusion=paper_conclusion,
            format_instructions=format_instructions
        )
        response = self.chat(messages)
        output_dict = output_parser.parse(response.content)

        return output_dict

    def translate_dict(self, data, target_language):
        """
        Translate the data in dictionary in to target languages.
        """
        template_string = """Translate the text \
        that is delimited by triple backticks \
        into a style that is {style}. \
        Preserving the original English terms for AI/ML-related terms and capitalized phrases invented by the authors.

        text: ```{text}```
        """
        prompt_template = ChatPromptTemplate.from_template(template_string)
        customer_style = f"""{target_language} in a professional AI Research tone, calm and respectful"""
        for key, value in data.items():
            messages = prompt_template.format_messages(style=customer_style, text=value)
            response = self.chat(messages)
            data[key] = value + '\n' + response.content
        return data


if __name__ == "__main__":
    paper = ArxivPaper("https://arxiv.org/abs/2304.00414", save_folder=".")
    paper.parse()
    bot = PaperReader(paper)
    summary = bot.get_summary_langchain()
    translate = bot.translate_dict(summary, "Chinese")
    print(translate)


