from models import BitlyURL
from bitly import Api
import settings
import re

PRIVATES = ['(^127\.0\.0\.1)',
            '(^10\.)',
            '(^172\.1[6-9]\.)',
            '(^172\.2[0-9]\.)',
            '(^172\.3[0-1]\.)',
            '(^192\.168\.)'
        ]


class DjanglyMiddleware():
    """ Middleware to examine requested URL and, where appropriate, go get a shortened bit.ly URL """
    def process_request(self, request):
        host = request.META['HTTP_HOST']
        if host in settings.EXCLUDED_HOSTS:
            return None
        request_uri = request.build_absolute_uri()
        if '/admin/' in request_uri:
            return None
        
        ## do a single check to see if there's anything alphabetical
        has_alpha = re.compile('[a-zA-Z]+')
        if has_alpha.search(host) is not None:
            ## check if someone is hitting their application via a private IP rather than hostname
            for private in PRIVATES:
                p = re.compile(private)
                if p.match(host) is not None:
                    return None
        
        ## okay, looks like all those tests were passed, let's go shorten...
        if BitlyURL.objects.filter(unshorted_url=request_uri).count() < 1:
			try:
	            newbitly = BitlyURL()
	            newbitly.unshorted_url = request_uri
	            a=Api(login=settings.BITLY_LOGIN,apikey=settings.BITLY_API_KEY)
	            short=a.shorten(request_uri,{'history':1}) 
	            newbitly.shortened_url=short
	            newbitly.save()
			except:
				pass
            
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    
    def process_response(self, request, response):
        return response
    
    def process_exception(self, request, exception):
        return None
    
