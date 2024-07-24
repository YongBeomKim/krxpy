from .base import *


class Post:

    def __init__(self, headers=None):
        self.headers = {
            "User-Agent": FakeAgent.random
        }
        if headers is not None:
            self.headers.update(headers)

    def read(self, **params):
        # print(f"Headers : {self.headers}")
        # print(f"Params : {params}")
        resp = requests.post(self.url, headers=self.headers, data=params)
        return resp

    @property
    @abstractmethod
    def url(self):
        return NotImplementedError
