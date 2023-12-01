class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        print("1")

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        print("2")
        return response
