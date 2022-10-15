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
            'D_TypeID',
            'D_GroupID',
            'D_DATE',
            'fileName',
            'D_MetadataID',
            'D_PROVINCE',
         ]