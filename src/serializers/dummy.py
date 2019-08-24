class DummySerializer(object):

    @classmethod
    def dumps(self, obj):
        return obj

    @classmethod
    def loads(self, obj):
        return obj
