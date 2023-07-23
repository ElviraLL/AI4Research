"""
A module that looks for papers from arxiv.
Version: 0.1
Auther: Jingwen Liang
Date: 2023-06-29
"""
import arxiv
import datetime

class ArxivResultWrapper:
    def __init__(self, original_object):
        self.original_object = original_object

    def __hash__(self):
        return hash(self.original_object.entry_id)

    def __eq__(self, other):
        if not isinstance(other, ArxivResultWrapper):
            return False
        return self.original_object.entry_id == other.original_object.entry_id


class Fetcher:
    def get_papers(self, query, max_results=30, sort=arxiv.SortCriterion.SubmittedDate):
        """
        Fetch papers from Arxiv API.
        search_terms is a dictionary where keys are the fields to search (title, authors, etc.)
        and values are the search terms.
        """
        papers = []
        # Fetch the data from the API
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort,
            sort_order=arxiv.SortOrder.Descending,
        )
        for index, result in enumerate(search.results()):
            papers.append({
                "title": result.title,
                "link": result.link,
            })
        return papers

    def fetch_papers_by_date(
            self,
            query: str,
            target_date: datetime.datetime.date,
            max_results_each_category: int = 100):
        papers = set()
        idx = 0
        search = arxiv.Search(
            query=query,
            max_results=max_results_each_category,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        for result in search.results():
            print(idx, result.entry_id, result.published)
            published_date = result.published.date()
            if published_date == target_date:
                papers.add(ArxivResultWrapper(result))
                idx += 1

        return list(papers)

    def fetch_daily_papers(self):
        """
        Return a list of arxiv.Results objects
        """
        current_datetime = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        yesterday = (current_datetime - one_day).date()
        categories = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.GR', 'cs.RO']
        categories_str = " OR ".join(f"cat:{cat}" for cat in categories)
        results = self.fetch_papers_by_date(categories_str, yesterday, 200)
        # papers = [item.original_object for item in results if self.paper_filter(item.original_object)]
        return [item.original_object for item in results]


if __name__ == "__main__":
    # query = "draggan, "
    fetcher = Fetcher()
    papers = fetcher.fetch_daily_papers()
    print(papers)
    for idx, paper in enumerate(papers):
        print(f"{idx}: {paper.entry_id}, {paper.categories}")

