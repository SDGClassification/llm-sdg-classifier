import json
import hashlib
from frozendict import frozendict

from typing import no_type_check


class Config(frozendict):
    """Configuration for an SDG classifier.

    Configurations are immutable. Parameters can be accessed using dict access
    or dot notation: config["param"] OR config.param
    """

    @no_type_check
    def __getattr__(self, key):
        """Allow accessing of parameters using dot notation."""
        return self[key]

    def get_identifier(self) -> str:
        """Unique identifier for this Config.

        Uses MD5 to generate a hash. Only the first seven chars are used.

        Returns: Unique identifier"""
        return hashlib.md5(json.dumps(self).encode("utf-8")).hexdigest()[:7]
