import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
from classifiers import BaseClassifier, Config

from openai.types.chat.chat_completion import ChatCompletion


class Classifier(BaseClassifier):
    """Hierarchical Multi-label Classification (HMC) with ChatGPT using topics.

    Rather than prompting ChatGPT to directly map texts to SDGs, we prompt
    ChatGPT to map texts to a manually defined list of topics (e.g. energy) and
    subtopics(e.g. renewable energy). Each subtopic is associated with one SDG.

    Thanks to the hierarchical nature of the classification, all texts are first
    broadly mapped to topics. If a topic is found in the text, the classifier
    then checks the text for the list of very specific subtopics.

    Example Prompt:

    ```
    You are an intelligent multi-label classification system designed to perform topic classification.

    You take the Text delimited by triple quotes as input and return a comma-separated list of relevant topic IDs.

    If none of the topics are relevant, return 0.

    Topics:
    1) ...
    2) ...
    3) ...

    Text: \"\"\" ... text goes here ... \"\"\"

    Topic IDs:
    ```
    """

    topics: list[str]
    energy_subtopics: list[str]

    def __post_init__(self, configuration: Config) -> None:
        load_dotenv()
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.create_chat_completion = self.with_cache(client.chat.completions.create)

        # Load topics
        with open(self.directory.joinpath("topics.yaml")) as f:
            data = yaml.safe_load(f)
            self.topics = data["topics"]
            self.energy_subtopics = data["energy_subtopics"]

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs in numeric form."""
        sdgs: list[int] = []

        # Find topics in text
        topics = self.classify_topics(text)

        # If energy topic was found, try to find specific energy subtopics
        if "energy and electricity" in topics:
            if len(self.classify_energy_subtopics(text)):
                sdgs.append(7)

        return sdgs

    def classify_topics(self, text: str) -> list[str]:
        """Classify the given text and return relevant topics.

        Args:
            text: Text to classify

        Returns: List of relevant topics
        """

        topics = self.topics

        # Send prompt to ChatGPT
        response = self.create_chat_completion(
            model="gpt-4-0125-preview",
            messages=[
                dict(
                    role="system",
                    content=self.get_prompt("system_topics", topics=topics),
                ),
                dict(role="user", content=self.get_prompt("user", text=text)),
            ],
            frequency_penalty=0,
            presence_penalty=0,
            # Long enough for 2-digit topic number + whitespace + comma
            max_tokens=len(topics) * 4,
            temperature=0,
        )

        # Get relevant topics as list
        return self.get_topics_from_response(response, topics=topics)

    def classify_energy_subtopics(self, text: str) -> list[str]:
        """Classify the given text and return relevant energy subtopics.

        Args:
            text: Text to classify

        Returns: List of relevant energy subtopics
        """

        subtopics = self.energy_subtopics

        # Send prompt to ChatGPT
        response = self.create_chat_completion(
            model="gpt-4-0125-preview",
            messages=[
                dict(
                    role="system",
                    content=self.get_prompt(
                        "system_energy_subtopics", topics=subtopics
                    ),
                ),
                dict(role="user", content=self.get_prompt("user", text=text)),
            ],
            frequency_penalty=0,
            presence_penalty=0,
            # Long enough for 2-digit topic number + whitespace + comma
            max_tokens=len(subtopics) * 4,
            temperature=0,
        )

        # Get relevant topics as list
        return self.get_topics_from_response(response, topics=subtopics)

    def get_topics_from_response(
        self, response: ChatCompletion, topics: list[str]
    ) -> list[str]:
        """Get list of topics from a ChatGPT API response.

        Converts numeric topic IDs into their string equivalent.

        Args:
            response: ChatCompletion response from ChatGPT API
            topics: List of all topic strings in the same order they were sent
                    to ChatGPT

        Returns: List of topics referenced in the response
        """
        topic_ids = response.choices[0].message.content

        # Verify that message is not empty
        if not topic_ids:
            raise Exception("ChatGPT response was empty")

        # No relevant topics
        if topic_ids == "0":
            return []

        # Remove examples from topics, if any
        for i, topic in enumerate(topics):
            if ": " in topic:
                topics[i] = topic[: topic.index(":")]

        # Return list of topics in string format
        return [topics[int(id) - 1] for id in topic_ids.split(",")]
