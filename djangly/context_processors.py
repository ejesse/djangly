from models import BitlyURL
from bitly import BitlyError

def bitly(request):
    request_uri = request.build_absolute_uri()
    bitly_url = request_uri
    try:
        bitly_url_object = BitlyURL.objects.filter(unshorted_url=request_uri)[0]
        bitly_url = bitly_url_object.shortened_url
    except IndexError:
        ## We don't want raise exceptions if we're local or bit.ly is having issues
        ## since it will interrupt page rendering, and well, it would be embarrassing
        ## to have your site crash cause it couldn't get a short URL. Having said that,
        ## you may want to log here, rather than just passing
        pass
    except BitlyError:
        pass
    finally:
        return {'BITLY_URL': bitly_url}
