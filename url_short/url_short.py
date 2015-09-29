import cherrypy
import string
import random
import time

urls = {
    '1': {
        'full_url': 'www.google.com',
        'short_url': 'gggg'
    },

    '2': {
        'full_url': 'www.msn.com',
        'short_url': 'msnmsn'
    },

    '3': {
        'full_url': 'www.bing.com',
        'short_url': 'bng'
    }
}

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate


 
class UrlShortService:

    exposed = True

    @RateLimited(2)  # 2 per second at most
    def GET(self, shortUrl=None):

        if shortUrl is None:
            return """<html>
               <head></head>
                 <body>
                   <form method="get">
                    Short Url: <input type="text" name="shortUrl"></input>
                    <button type="submit">Get Full URL</button>
                 </form>
                 <form method="post">
                    Full Url: <input type="text" name="fullUrl"></input>
                    <button type="submit">Create Short URL</button>
                 </form>
              </body>
            </html>"""
        else:
           for k in urls:
             url = urls[k]
             if url['short_url'] == shortUrl:
              raise cherrypy.HTTPRedirect("http://"+url['full_url'])
#               return( 'The full URL for %s is %s\n' % (
#                    shortUrl, url['full_url']))
           return('No full url for short url \'%s\'\n' % shortUrl)

    def POST(self, fullUrl):

        id = str(max([int(_) for _ in urls.keys()]) + 1)

        urls[id] = {
            'full_url': fullUrl,
            'short_url': ''.join([random.choice(string.ascii_letters +                                string.digits) for n in xrange(6)])
        }

        return ('Create a new url with short url: %s\n' 
                   % urls[id]['short_url'])

    def PUT(self, shortUrl=None, fullUrl=None):
        if shortUrl is None:
          return('No URL specified\n' )
        else:
          for k in urls:
            url = urls[k]
            if url['short_url'] == shortUrl:
              urls[k] = {'full_url': fullUrl, 
                     'short_url': shortUrl}
              return( 'The full URL for %s is now %s\n' % (
                    shortUrl, fullUrl))
          return('No short url %s in database\n' % shortUrl)

    def DELETE(self, shortUrl=None):
        if shortUrl is None:
          return('No URL specified\n' )
        else:
          for k in urls:
            url = urls[k]
            if url['short_url'] == shortUrl:
              del urls[k]
              return( 'The URL for %s has been removed\n' % (
                    shortUrl))
          return('No short url %s in database\n' % shortUrl)

if __name__ == '__main__':

    cherrypy.tree.mount(
        UrlShortService(), '/api/UrlShortService',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()

