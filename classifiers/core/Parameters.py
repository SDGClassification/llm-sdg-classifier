from frozendict import frozendict
from .Config import Config


class Parameters(frozendict):
    """Allowed set of configuration parameters for an SDG classifier.

    Parameters are immutable. Parameters can be accessed using dict access
    or dot notation: config["param"] OR config.param
    """

    __getattr__ = dict.get

    def validate(self, config: Config) -> None:
        """Validate that the given config defines all parameters.

        Raises: Exception if config has too few or too many keys"""
        expected_keys = set(self.keys())
        actual_keys = set(config.keys())

        if expected_keys != actual_keys:
            raise Exception(
                f"{config} is not valid.\n"
                f"Expected keys: {expected_keys}\n"
                f"Actual keys: {actual_keys}"
            )
