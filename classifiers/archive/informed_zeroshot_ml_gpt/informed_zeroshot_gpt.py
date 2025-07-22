from classifiers import BaseClassifier, Config
from openai import OpenAI
from dotenv import load_dotenv
import re
import os

class Classifier(BaseClassifier):
    """Classify texts by SDG using ChatGPT.

    The prompt does not include examples for each SDG. Instead of relying on GPT's knowledge of SDGs,
    it provides the descriptions of all SDGs.

    """

    def __post_init__(self, configuration: Config) -> None:

        load_dotenv()
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.create_chat_completion = self.with_cache(client.chat.completions.create)

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs in numeric form."""

        # Send prompt to ChatGPT
        completion = self.create_chat_completion(
            model="gpt-4o",
            messages=[
                dict(role="system", content=self.get_prompt("system")),
                dict(role="user", content=self.get_prompt("user", text=text)),
            ],
            # response_format={"type": "json_object"},
            temperature=0,
        )
        # message = response.choices[0].message.content
        sdgs = re.findall('\d+', completion.choices[0].message.content)

        return [int(sdg) for sdg in sdgs]
