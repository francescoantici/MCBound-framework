class IRequestValidator:
    
    @classmethod
    def validate_request(cls, request):
        return cls._isValidRequest(request)
    
    @classmethod
    def _isValidRequest(cls, request):
        pass
