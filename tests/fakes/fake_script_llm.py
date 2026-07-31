class FakeStructuredLLM:

    def __init__(self, response):
        self.response = response

    def __ror__(self, other):
        return self

    def invoke(self, data):
        return self.response


class FakeLLM:

    def __init__(self, response):
        self.response = response

    def with_structured_output(self, schema):
        return FakeStructuredLLM(self.response)