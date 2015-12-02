import json

def jsonify(method):
    def do_method(self, *args, **kwargs):
        self.response.set_status(200)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        self.response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, content-type'
        return json.dumps(method(self, *args, **kwargs))
    return do_method


def check(*arguments):
    def check_decorator(method):
        def do_check(self, *args, **kwargs):
            if all(hasattr(self, arg) and getattr(self, arg) is not None for arg in arguments):
                return method(self, *args, **kwargs)

            # The check failed for at least on argument
            self.response.set_status(500)
            self.response.write('ERROR 500: non-recoverable condition, argument check failed for %s', arguments)

        return do_check
    return check_decorator