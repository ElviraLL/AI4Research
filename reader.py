import logging

logger = logging.getLogger(__name__)
import openai

class PaperReader:
    def __init__(self, paper):
        self.paper = paper
        self. summary = ""

    def get_summary(self):
        """
        Summarize the paper.

        Args:
            gpt_api_key: The api key of the openai gpt-3.
        """
        logging.info("Summarizing paper")
        openai.api_key = self.gpt_api_key
        messages = [
            {"role": "system", "content": "You are a experienced AI researcher. You can read paper about "
                                          "state of the arts AI researchs and write summary about it methodology."},
            {"role": "user",
             "content": f"Please help me read the paper and write a summary about its methodology. The paper is here: {self.method}"},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        self.summary = response.choices[0].text.strip()
        for choice in response.choices:
            self.summary += choice.message.content
        print("summary_result:\n", self.summary)
        print("prompt_token_used:", response.usage.prompt_tokens,
              "completion_token_used:", response.usage.completion_tokens,
              "total_token_used:", response.usage.total_tokens)
        print("response_time:", response.response_ms / 1000.0, 's')
        logging.info("Finished summarizing paper")