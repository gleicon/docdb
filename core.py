from twisted.internet import defer
from twisted.python import log
import nltk


class DBOper:
    def __init__(self, redis):
        self.redis = redis
        self.ALLWORDS = 'S_ALLWORDS'
        self.STOPWORDS = nltk.corpus.stopwords.words('english')
        self.p=nltk.stem.PorterStemmer()

    @defer.inlineCallbacks
    def insert(self, doc):
        log.msg('insert')

        _id = self.redis.incr('NEXT.DOC')
        res = self.redis.set('DOCID:%s' % _id, doc)
        # SET DOCMETA:_id DOC's metadata (name, tstamp, revision)
        acc=0
        for i in doc.split(): # tokenizer
            if i not in self.STOPWORDS: 
                word = self.p.stem(i)
                self.redis.sadd(word, _id)
                self.redis.sadd(self.ALLWORDS, word)
                acc=acc+1

        defer.returnValue((_id, acc, res))

    @defer.inlineCallbacks
    def find(self, words=[]):
        log.msg('find')
        wordsets=[]
        for w in words:
            ism = yield self.redis.scard(self.p.stem(w))
            if ism > 0:
                wordsets.append(self.p.stem(w))
        if len(wordsets) < 1: 
            defer.returnValue(None)

        docs = yield self.redis.sinter(*wordsets)
        defer.returnValue(docs)


  #  @defer.inlineCallbacks
    def delete(self, _id=None):
        log.msg('delete')

   # @defer.inlineCallbacks
    def update(self, _id, doc):
        log.msg('update')
    
    @defer.inlineCallbacks
    def get(self, _id):
        log.msg('get %s' % _id)
        doc = yield self.redis.get('DOCID:%s' % _id)
        defer.returnValue(doc)

