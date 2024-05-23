import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from classifiers import BaseClassifier, Parameters, ConfigSet, Config


class Classifier(BaseClassifier):
    """Classify texts by SDG using ChatGPT.

    The prompt does not include examples for each SDG. It relies on ChatGPT's
    existing knowledge of the SDGs.

    Response is in JSON format.
    """

    CONFIGURATIONS = ConfigSet(
        Parameters(model="ChatGPT model to use"),
        Config(model="gpt-4-0125-preview"),
        Config(model="gpt-3.5-turbo-0125"),
    )

    # ChatGPT model to use
    # See: https://platform.openai.com/docs/models/overview
    model: str

    def __post_init__(self, configuration: Config) -> None:
        self.model = configuration.model

        load_dotenv()
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.create_chat_completion = self.with_cache(client.chat.completions.create)

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs in numeric form."""

        # Send prompt to ChatGPT
        response = self.create_chat_completion(
            model=self.model,
            messages=[
                dict(role="system", content=self.get_prompt("system")),
                dict(role="user", content=self.get_prompt("user", text=text)),
            ],
            response_format={"type": "json_object"},
        )
        message = response.choices[0].message.content

        # Verify that message is not empty
        if not message:
            raise Exception("Message is empty")

        # Get SDGs from message
        data = json.loads(message)
        return data["sdgs"]


# Example code for directly running without going through evaluate script
# Note that this does not update the READMEs
if __name__ == "__main__":
    from sdgclassification.benchmark import Benchmark

    classifier = Classifier(config=1)
    benchmark = Benchmark(classifier.classify, sdgs=[10])

    benchmark.run()
