import collections
import pickle


class BaseClientIterator(collections.MutableSequence):

    backend_class = None
    serializer_class = pickle

    def __init__(self, iterable=None, backend_class=None, serializer_class=None, profiling_level=0):

        super(BaseClientIterator, self).__init__()

        backend_class = backend_class or self.backend_class
        serializer_class = serializer_class or self.serializer_class

        self.__backend = backend_class(profiling_level=profiling_level)
        self.__serializer = serializer_class

        if iterable is not None:
            self.extend(iterable)

    def __repr__(self):

        return '{}({})'.format(self.__class__.__name__, self.__str__())

    def __str__(self):

        return '[{}]'.format(', '.join(map(repr, self)))

    def __eq__(self, other):

        total_objs = len(self.__backend)
        if total_objs != len(other):
            return False

        for i, elem in enumerate(self):
            if elem != other[i]:
                return False

        return True

    def __delitem__(self, index):

        del self.__backend[index]

    def __getitem__(self, index):

        if isinstance(index, slice):
            objs = (self.__serializer.loads(obj) for obj in self.__backend._slice(index))
            return self.__class__(objs)

        encoded_value = self.__backend[index]
        return self.__serializer.loads(encoded_value)

    def __iter__(self):

        for value in self.__backend.__iter__():
            yield self.__serializer.loads(value)

    def __setitem__(self, index, value):

        encoded_value = self.__serializer.dumps(value)
        self.__backend[index] = encoded_value

    def __len__(self):

        return len(self.__backend)

    def __del__(self):

        del self.__backend

    def insert(self, index, value):

        encoded_value = self.__serializer.dumps(value)
        self.__backend.insert(index, encoded_value)

    def extend(self, iterable):

        self.__backend.extend((self.__serializer.dumps(value) for value in iterable))
