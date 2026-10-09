import uuid

class RequestIDMiddleware:
    # Building the middleware chain to continue the request pipeline
    def __init__(self, get_response):
        self.get_response = get_response # by calling `get_response` which = the next thing that should process this request i.e. the next middleware & eventually the view.

    def __call__(self, request): # makes the middleware object callable like a function.

        # Determine Request ID

        # fetching client provided Request-ID (if any)
        supplied_request_id = request.headers.get(
            "X-Request-ID"
        )

        if (
            supplied_request_id
            and len(supplied_request_id) <= 128
        ):
            request_id = supplied_request_id
        else:
            request_id = str(uuid.uuid4()) # else assigning UUID based request_id

        request.request_id = request_id

        response = self.get_response(request) # Pre-processing (req_id etc.) done; continue to rest of Django 

        response["X-Request-ID"] = request_id # add request ID header to response created/received

        return response