from django.db import models


class QuerySetManager(models.Manager):

    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, item, *args):
        try:
            return getattr(self.__class__, item, *args)
        except AttributeError:
            return getattr(self.get_query_set(), item, *args)
