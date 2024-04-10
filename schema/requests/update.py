from schema.requests.requests_validators import IRequestValidator


class UpdateRequestValidator(IRequestValidator):
    
    @classmethod
    def _isValidRequest(cls, request):
        return True