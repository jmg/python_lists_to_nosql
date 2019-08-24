import sys
sys.path.append("..")
from src import MongoDBList, CouchDBList

default_list_class = list
test_list_classes = [MongoDBList, CouchDBList]

for klass in test_list_classes:

    test_list = klass([1,2,3])
    default_list = default_list_class([1,2,3])
    assert test_list == default_list

    test_list.append(4)
    default_list.append(4)

    assert test_list == default_list

    test_list.extend([5,6,7])
    default_list.extend([5,6,7])

    assert test_list == default_list

    test_list.extend([8,9])
    default_list.extend([8,9])

    assert test_list == default_list

    for x, y in zip(default_list, test_list):
        assert x == y

    test_list[1] = 5
    default_list[1] = 5

    assert test_list[1] == default_list[1]

    for x, y in zip(default_list, test_list):
        assert x == y

    assert test_list == default_list
    print "REPR LIST ->", repr(test_list)

    assert test_list[1:3], default_list[1:3]
    assert 3 in default_list
    assert 3 in test_list

    del test_list[2]
    del default_list[2]

    assert test_list == default_list