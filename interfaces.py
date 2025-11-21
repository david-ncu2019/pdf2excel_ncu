from abc import ABC, abstractmethod
from typing import List, Any, Dict

class IExtractor(ABC):
    """
    Interface for extracting data from a document.
    Must return a dictionary mapping 'Sheet/Page Names' to 'Table Data'.
    """
    @abstractmethod
    def extract(self, file_path: str) -> Dict[str, List[List[Any]]]:
        pass

class IExporter(ABC):
    """
    Interface for saving data to a persistent format.
    Accepts the dictionary structure from IExtractor.
    """
    @abstractmethod
    def save(self, data: Dict[str, List[List[Any]]], output_path: str) -> None:
        pass