from abc import ABC, abstractmethod

class StoragePort(ABC):

    @abstractmethod
    def upload(self, bucket_name, object_name, data, length) -> None:
        pass

    @abstractmethod
    def delete(self, bucket_name: str, object_name: str) -> None:
        pass
    
    @abstractmethod
    def get(self, bucket_name: str, objetc_name: str):
        pass