from minio import Minio

class MinioStorage:
    def __init__(self, client: Minio):
        self.client = client
    
    def upload(self, bucket_name, object_name, data, length) -> None:
        self.client.put_object(bucket_name, object_name, data, length)
        
    def delete(self, bucket_name: str, object_name: str) -> None:
        self.client.remove_object(bucket_name, object_name)
    
    def get(self, bucket_name: str, object_name: str):
        self.client.get_object(bucket_name, object_name)
    
    