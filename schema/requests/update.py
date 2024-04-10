from schema.requests.requests_validators import IRequestValidator


class UpdateRequestValidator(IRequestValidator):
    
    @classmethod
    def _isValidRequest(cls, request):
        if not("stage" in request):
            raise Exception("Missing the stage descriptor")