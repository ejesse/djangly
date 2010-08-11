from models import BitlyURL
from bitly import Api
import settings

class DjanglyMiddleware():
    
    def process_request(self, request):
        host = request.META['HTTP_HOST']
        if not host in settings.EXCLUDED_HOSTS:
            request_uri = request.build_absolute_uri()
            if BitlyURL.objects.filter(unshorted_url=request_uri).count() < 1:
                newbitly = BitlyURL()
                newbitly.unshorted_url = request_uri
                a=Api(login=settings.BITLY_LOGIN,apikey=settings.BITLY_API_KEY)
                short=a.shorten(request_uri,{'history':1}) 
                newbitly.shortened_url=short
                newbitly.save()
            
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    
    def process_response(self, request, response):
        return response
    
    def process_exception(self, request, exception):
        return None
    
