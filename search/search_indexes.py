from haystack import indexes
from shop.models import Goods, GoodType


class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Goods
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_sale=True)
