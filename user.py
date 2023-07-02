
class User:
    def __init__(self, name):
        self.name = name
        self.preferences = {
            'title': [],
            'author': [],
            'category': ['cs.LG'],
            'abstract': []
        }
        self.papers = []

    def update_preferences(self, preferences):
        self.preferences = preferences

    def get_preferences(self):
        return self.preferences

    def add_papers(self, papers):
        self.papers.extend(papers)

    def get_and_clear_papers(self):
        papers = self.papers
        self.papers = []
        return papers




