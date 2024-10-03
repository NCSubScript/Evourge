import typing

class List(list):
    def __init__(self, data = None):
        if data is not None:
            super().__init__(data)
        else:
            super().__init__()
        


class Dict(dict):
    def __init__(self, data = None):
        if data is not None:
            super().__init__(data)
        else:
            super().__init__()
        self['previous'] = {}


    def toJSON(self):
        return json.dumps(
        self,
        default=lambda o: {o.data}, 
        sort_keys=True,
        indent=4)

    def add(self, k, v):
        try:
            self[k].append(v)
        except:
            self[k] = List(v)

    def change(self, object):
        if isinstance(object, dict):
            for k, v in object.items():
                if k in self.data.keys():
                    self['previous'][k] = self[k]
                self[k] = v
                
    def change(self, name, value):
        if name in self.keys():
            self['previous'][name] = self[name]
        self.data[name] = value

    def __getattr__(self, name: str):
        if name in self.keys():
            return self[name]
        return None
    
    def __setattr__(self, name: str, value: typing.Any) -> None:
        if name in self.keys():
            self['previous'][name] = self[name]
        self[name] = value

    def __str__(self):
        return str(self.toJSON())