### Подключаем к монгоДБ. нужно доставить pymongo
'''
>>> import pymongo
>>> m = pymongo.MongoClient()
>>> m
MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True)
>>> dir(m.test.users)  ## списко комманд относительно коллекции, которые можно применить. EX. find(), insert()...

>>> m.test.users.insert({'a': 1, 'b': [1,2,3], 'd': {'q':3, 'w': 'qwe'}})
ObjectId('5923284d60d99f291f62422d')
>>> m.test.users.find()
<pymongo.cursor.Cursor object at 0x7f7df08ea910>

>>> for d in m.test.users.find():
...     print(d)
... 
{u'a': 1, u'_id': ObjectId('5923284d60d99f291f62422d'), u'b': [1, 2, 3], u'd': {u'q': 3, u'w': u'qwe'}}
mongodb University --- можно получить сертификат.
'''

### Работа с redis
'''
>>pip install redis
>>import redis
>> r = redis.StrictRedis() ### команды такие же как и в документации для redis
>> dir(r)
>> r.get('a')
b'11'
>> r.set('a', 5)
True
>> r.get('a')
b'5'
'''

### РАбота с elasticsearch
'''
>> pip install elasticsearch

>> import elasticsearch
>> es = elasticsearch.Elasticsearch() ## conecct to localhost
>> r = es.index(index='i1', doc_type='d1', id=1, body={'tittle':'mongodb vs elasticsearch', 'author': 'Pushkin'})

>> es.search(index='i1', doc_type='d1', body={'query':{'match_all': 'mongodb'}})
'''