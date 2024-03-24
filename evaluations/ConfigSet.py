from collections import Counter
from .Config import Config
from .Parameters import Parameters

from typing import Iterator


class ConfigSet:
    """A set of Configs.

    ConfigSets are immutable."""

    paramters: Parameters
    __configs: tuple[Config, ...]

    def __init__(self, parameters: Parameters, *configs: Config) -> None:
        # Validate that each config is valid
        for config in configs:
            parameters.validate(config)

        # Validate that all configs are unique
        duplicates = [k for k, v in Counter(configs).items() if v > 1]
        if len(duplicates):
            raise Exception(f"{duplicates[0]} is not unique in ConfigSet")

        self.parameters = parameters
        self.__configs = configs

    def __len__(self) -> int:
        return len(self.__configs)

    def __iter__(self) -> Iterator[Config]:
        return iter(self.__configs)

    def __getitem__(self, key: int) -> Config:
        """Get config by index.

        Returns: The corresponding Config

        Raises:
            ValueError: When no config for the given key exists.
        """
        if key < 0 or key >= len(self.__configs):
            raise ValueError(f"Configuration for key {key} does not exist")

        return self.__configs[key]

    def get_config(self, key: int) -> Config:
        """Get config by index (starting at 1).

        Returns: The corresponding Config

        Raises:
            ValueError: When no config for the given key exists.
        """
        if key < 1 or key > len(self.__configs):
            raise ValueError(f"Configuration for key {key} does not exist")

        return self[key - 1]
