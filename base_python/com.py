class comunication:
    Information = {

    }

    def write(self, **kwargs):
        for x in kwargs:
            self.Information[x] = kwargs[x]

    def get(self, key):
        return self.Information[key]

