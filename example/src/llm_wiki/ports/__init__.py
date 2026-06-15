"""Port protocols (S2-2)."""

from llm_wiki.ports.configuration import ConfigurationPort
from llm_wiki.ports.interaction import UserInteractionPort
from llm_wiki.ports.llm import LLMPort
from llm_wiki.ports.schema import SchemaPort
from llm_wiki.ports.storage import WikiStoragePort

__all__ = [
    "ConfigurationPort",
    "LLMPort",
    "SchemaPort",
    "UserInteractionPort",
    "WikiStoragePort",
]
