from schema.requests.requests_validators import IRequestValidator

class FetchDataValidator(IRequestValidator):
    
    @classmethod
    def _isValidRequest(cls, request):
        if not("start_time" in request):
            raise Exception("Missing start time in request")
        if not("end_time" in request):
            raise Exception("Missing end time in request")
        if not("feature" in request):
            raise Exception("Missing feature time in request")