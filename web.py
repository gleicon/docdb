import sys
import cyclone.web
from twisted.python import log
from twisted.internet import reactor
from twisted.internet import defer
import txredisapi
import core

class MainHandler(cyclone.web.RequestHandler):
    
    @defer.inlineCallbacks
    @cyclone.web.asynchronous
    def get(self, id):
        if id == None:
            self.write('docdb help\r\n')
        else:
            doc = yield self.settings.oper.get(id)
            self.write('docdb get\r\n%s\r\n' % doc)
        self.finish()

    @defer.inlineCallbacks
    @cyclone.web.asynchronous
    def post(self, id):
        #TODO: modify to handle file upload. documents are huge
        body = self.get_argument("body", None)
        if body == None:
            self.write('empty doc')
        else:
            self.settings.oper.insert(body)
            self.write('docdb post\r\n')
        self.finish()

def main():

    db = txredisapi.lazyRedisConnectionPool(pool_size=10)
    oper = core.DBOper(db)

    settings = {
        "db": db,
        "oper": oper
    }
    
    application = cyclone.web.Application([
        (r"/docdb/(\d+)?", MainHandler),
        ], **settings)


    reactor.listenTCP(8888, application)
    reactor.run()

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()

