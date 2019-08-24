import collections

class BaseCollectionsBackend(collections.MutableSequence):

    def __repr__(self):

        return '{}({})'.format(self.__class__.__name__, self.__str__())

    def __str__(self):

        return '[{}]'.format(', '.join(map(repr, self)))
