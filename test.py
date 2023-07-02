# import logging
# from paper_arxiv import ArxivPaper
#
# logging.basicConfig(level=logging.INFO)

# API_KEY = "YOUR_API_KEY"
# # arXiv paper URL
# arxiv_url = "https://arxiv.org/abs/2304.10537"
#
# # Test with an arXiv URL
# paper = ArxivPaper(url=arxiv_url, save_folder="D:\\Papers")
# paper.fetch()
# paper.parse()
# # paper.extract_main_figure()
# # paper.summarize()
#
# print("Title:", paper.title)
# print("Authors:", paper.authors)
# print("Abstract:", paper.abstract)
# print("Conference:", paper.conference)
# print("sections:", paper.pdf_dict.keys())

from fetcher import Fetcher
query = "draggan, "
feacher = Fetcher()
search = feacher.get_paper(query)
print("All search: ")
for index, result in enumerate(search.results()):
    print(index, result.title, result.updated)

