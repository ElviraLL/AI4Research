import logging
from paper import Paper

logging.basicConfig(level=logging.INFO)

API_KEY = "YOUR_API_KEY"
# arXiv paper URL
arxiv_url = "https://arxiv.org/abs/2304.10537"

# Direct PDF URL


# Test with an arXiv URL
paper = Paper(url=arxiv_url, save_folder="D:\\Papers", gpt_api_key=API_KEY)
paper.fetch()
paper.parse()
paper.get_chapter_names()
# paper.extract_main_figure()
# paper.summarize()

print("Title:", paper.title)
print("Authors:", paper.authors)
print("Abstract:", paper.abstract)
print("Conference:", paper.conference)
print("Chapters:", paper.chapter_names)
# print("Summary:", paper.summary)


# # Test reading from local pdf
# paper = Paper(
#     gpt_api_key=API_KEY,
#     pdf_input_path="D:\\Papers\\Conditional_Negative_Sampling_for_Contrastive_Learning_of_Visual_Representations\\Conditional_Negative_Sampling_for_Contrastive_Learning_of_Visual_Representations.pdf"
# )
# paper.fetch()
# paper.parse()
# paper.extract_main_figure()
#
# print("Title:", paper.title)
# print("Authors:", paper.authors)
# print("Abstract:", paper.abstract)
