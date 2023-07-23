"""
Main entry point for the application.
Version: 0.1
Auther: Jingwen Liang
"""
from paper_arxiv import ArxivPaper
import logging
from pathlib import Path

from fetcher import Fetcher
from bot_read import PaperReader
from notion_properties import NotionProperties

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)
logger = logging.getLogger(__name__)

CATEGORY = {
    'cs.LG': 'ML',
    'cs.CL': 'NLP',
    'cs.CV': 'CV',
    'cs.GR': 'CG',
    'cs.RO': 'Robotics'
}

if __name__ == "__main__":
    # create a notion properties object to manage notion pages
    notion = NotionProperties()

    # Create the fetcher
    fether = Fetcher()

    # Run the daily task
    daily_papers = fether.fetch_daily_papers()
    if len(daily_papers) == 0:
        logger.info("Didn't fetch any paper desired the date.")
    if daily_papers:
        date = daily_papers[0].published.date()
        save_folder = Path(f'D:/Papers/{date.strftime("%Y_%m_%d")}')

        logger.info(f'Date is: {date.strftime("%Y-%m-%d")}')
        logger.info(f"There are: {len(daily_papers)} submissions on date {date.strftime('%Y-%m-%d')}")

        bot = PaperReader()

        papers_with_bugs = []
        for result in daily_papers:
            try:
                paper = ArxivPaper(result, save_folder=save_folder.as_posix())
                paper.parse()

                bot.set_paper(paper)
                summary = bot.get_summary_langchain()
                translate = bot.translate_dict(summary, "Chinese")

                page = notion.create_paper_page(paper)
                block = notion.append_paper_summary(page['id'], summary)
                logger.info("Successfully created a page for paper: %s", paper.title)

            except Exception as error:
                logger.error("Getting Error! for %s", paper.url)
                logger.error(error)
                papers_with_bugs.append(result)
            logging.info(" ")
        for item in papers_with_bugs:
            print(item.entry_id)


