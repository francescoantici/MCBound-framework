from schema.requests.requests_validators import IRequestValidator


class CharacteriseRequestValidator(IRequestValidator):
    
    @classmethod
    def _isValidRequest(cls, request):
        if not("jobs_data" in request) or (len(request["jobs_data"]) == 0):
            raise Exception("Jobs data not present")
        if not(isinstance(request["jobs_data"][0], dict)):
            raise Exception("Wrongly formatted jobs data")