import importlib
from pathlib import Path
from yaml import safe_load
from diskcache import Cache
from jinja2 import Template, StrictUndefined
from .ConfigSet import ConfigSet
from .Config import Config
from .Parameters import Parameters

from typing import TypeVar, Callable, Self, Type

C = TypeVar("C", bound=Callable)


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class BaseClassifier:
    cache: Cache
    configuration: Config
    CONFIGURATIONS: ConfigSet = ConfigSet(Parameters(), Config())

    def __init__(self, config: int = 1) -> None:
        """Initialize a classifier.

        Args:
            config: The index of the configuration to load (default = 1)
        """
        # Set up configuration
        self.configuration = self.CONFIGURATIONS.get_config(config)

        # Set up cache
        self.cache = Cache(self.directory.joinpath(".cache"))

        # Run optional post initialization
        self.__post_init__(self.configuration)

    def __post_init__(self, configuration: Config) -> None:
        """Post initialization of the classifier.

        This method should be overridden by child classes and used to take care
        of the classifier setup with the received Config object.

        Args:
            configuration: The Config object"""
        pass

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs.

        Args:
            text: The text to classify

        Returns: A list of SDGs in numeric form, eg: 1, 5, 9"""
        raise Exception("classify method must be implemented")

    def get_prompt(self, key: str, **kwargs) -> str:
        """Returns the prompt for the given key from prompt.yaml file.

        Args:
            key: Name of the prompt
            All other keyword arguments will be passed to the template.

        Returns: Prompt"""
        # Load all prompts
        with open(self.directory.joinpath("prompts.yaml")) as f:
            prompts = safe_load(f)

        # Prepare prompt template
        prompt_template = Template(prompts[key], undefined=StrictUndefined)

        return prompt_template.render(**kwargs)

    def with_cache(self, method: C) -> C:
        """Wraps the given method in a diskcache.

        When calling the method, diskcache checks if the method has been called
        with the exact arguments before. If so, the method does not get executed
        and the cached response is simply returned."""
        return self.cache.memoize()(method)

    @classproperty
    def name(cls) -> str:
        """The name of the classifier"""
        return Path(cls.__module__.replace(".", "/")).name

    @classproperty
    def directory(cls) -> Path:
        """The path to the directory where this classifier is defined"""
        return Path(cls.__module__.replace(".", "/")).parent

    @classproperty
    def runs_directory(cls) -> Path:
        """The path to the directory where runs for this classifier are stored"""
        return cls.directory.joinpath("runs")

    @classmethod
    def load(cls, classifier: str) -> Type[Self]:
        """Loads the classifier class by the provided name.

        Args:
            classifier: Name of classifier class to load

        Returns: Class of classifier"""

        module_path = f"evaluations.{classifier}.{classifier}"
        try:
            module = importlib.import_module(module_path, __name__)
            return getattr(module, "Classifier")
        except ModuleNotFoundError as e:
            file_path = module_path.replace(".", "/") + ".py"
            print(
                f"Tried to load classifier {classifier}. But file {file_path} does not exist."
            )
            exit(1)
