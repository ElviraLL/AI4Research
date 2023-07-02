"""
A module that looks for papers from arxiv.
Version: 0.1
Auther: Jingwen Liang
Date: 2023-06-29
"""
import arxiv


class Fetcher:
    def get_papers(self, query, max_results=30, sort=arxiv.SortCriterion.SubmittedDate):
        """
        Fetch papers from Arxiv API.
        search_terms is a dictionary where keys are the fields to search (title, authors, etc.)
        and values are the search terms.
        """
        # Fetch the data from the API
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort,
            sort_order=arxiv.SortOrder.Descending,
        )
        return search


if __name__ == "__main__":
    query = "draggan, "
    feacher = Fetcher()
    search = feacher.get_papers(query)
    print("All search: ")
    for index, result in enumerate(search.results()):
        print(index, result.title, result.updated)
    # > All search:
    # > 0 DragDiffusion: Harnessing Diffusion Models for Interactive Point-based Image Editing 2023-06-27 11:30:16+00:00
    # > 1 Drag Your GAN: Interactive Point-based Manipulation on the Generative Image Manifold 2023-05-18 13:41:25+00:00