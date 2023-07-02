"""
A module that deal with paper feeding process
Version: 0.1
Auther: Jingwen Liang
Date: 2023-06-29
"""

import json
from datetime import datetime, timedelta

class PaperFeeder:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.users = {}

    def add_user(self, user):
        self.users[user.name] = user

    def remove_user(self, user):
        if user.name in self.users:
            del self.users[user.name]

    def generate_query(self, preferences):
        # Start with an empty list for the query parts
        query_parts = []

        # Loop over each preference
        for key, values in preferences.items():
            # Combine the values for this preference using the AND operator
            value_query = ' AND '.join(values)

            # Add this query part to the list
            query_parts.append(f'{key}:({value_query})')

        # Combine all query parts using the OR operator
        query = ' OR '.join(query_parts)
        return query

    def run_daily_task(self):
        # Get the current date and time
        now = datetime.now()

        # Loop over each user
        for user in self.users.values():
            # Add a time filter to the preferences to only get papers from the last 24 hours
            yesterday = (now - timedelta(days=1)).strftime('%Y%m%d%H%M%S')
            preferences = {**user.get_preferences(), 'submittedDate': f'>={yesterday}'}

            # Get the papers for this user
            print(f"getting papers for {preferences}")
            responds = self.fetcher.get_papers(preferences)
            papers = []
            for index, result in enumerate(responds.results()):
                papers.append((index, result.title, result.updated, result.id))
            user.add_papers(papers)


if __name__ == "__main__":
    from fetcher import Fetcher
    from user import User

    # Create the fetcher
    paper_fetcher = Fetcher()
    paper_feeder = PaperFeeder(paper_fetcher)

    user = User('user1')
    user.update_preferences(preferences={
            'category': ['cs.GR', 'cs.LG'],
        })
    paper_feeder.add_user(user)
    # Run the daily task
    paper_feeder.run_daily_task()

    # Get the new papers for the user
    papers = user.get_and_clear_papers()
    print(len(papers))
    for paper in papers:
        print(paper.title)
