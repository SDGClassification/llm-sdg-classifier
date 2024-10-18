from classifiers import BaseClassifier, Parameters, ConfigSet, Config
from openai import OpenAI
from dotenv import load_dotenv
import re
import os

class Classifier(BaseClassifier):
    """Classify texts by SDG using ChatGPT.

    The prompt does not include examples for each SDG. Instead of relying on GPT's knowledge of SDGs,
    it provides the formal descriptions of all SDGs, e.g. SDG 1: End poverty in all its forms everywhere.

    This is an informed zero-shot multilabel classifier.

    """
    CONFIGURATIONS = ConfigSet(
        Parameters(model="ChatGPT model to use"),
        Config(model="gpt-4o-mini"),
        Config(model="gpt-4o"),
        Config(model="gpt-4-turbo"),
    )

    def __post_init__(self, configuration: Config) -> None:

        load_dotenv()
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.create_chat_completion = self.with_cache(client.chat.completions.create)

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs in numeric form."""

        # Send prompt to ChatGPT
        completion = self.create_chat_completion(
            model=self.configuration.model,
            messages=[
                dict(role="system", content=self.get_prompt("system")),
                dict(role="user", content=self.get_prompt("user", text=text)),
            ],
            # response_format={"type": "json_object"},
            temperature=0,
        )
        # message = response.choices[0].message.content
        sdgs = re.findall(r'\d+', completion.choices[0].message.content)

        return [int(sdg) for sdg in sdgs]

# inspection, will not be saved in readme, but in cache
if __name__ == "__main__":
    from sdgclassification.benchmark import Benchmark

    classifier = Classifier(config=1)
    benchmark = Benchmark(classifier.classify, sdgs=[10])

    benchmark.run()