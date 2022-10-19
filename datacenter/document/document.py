from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from ..models import Metadata

@registry.register_document
class MetadataDocument(Document):
    class Index:
        name = 'metadata'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Metadata
         fields = [
            'metadataGroupId',
            'dataSetGroupId',
            'fileName',
            'provinceId',
            'timestamp',
            'dataName',
            'description',
         ]