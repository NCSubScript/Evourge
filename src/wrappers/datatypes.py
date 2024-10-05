import typing

class DictAccess():
    
    def __init__(self, data = None):
        self.data = Dict(data)
    
    def __getattr__(self, attr):
        if attr in self.__dict__["data"].keys():
            return self.data[attr]
        return None


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


    def toJSON(self):
        return json.dumps(
        self,
        default=lambda o: {o}, 
        sort_keys=True,
        indent=4)

    def add(self, k, v):
        if 'previous' not in self.keys():
            self['previous'] = Dict()
        try:
            self[k].append(v)
        except:
            self[k] = List(v)

    def change(self, object):
        if 'previous' not in self.keys():
            self['previous'] = Dict()
        if isinstance(object, dict):
            for k, v in object.items():
                if k in self.keys():
                    self['previous'][k] = self[k]
                self[k] = v
                
    def change(self, name, value):
        if 'previous' not in self.keys():
            self['previous'] = Dict()
        if name in self.keys():
            self['previous'][name] = self[name]
        self[name] = value

    def __getattr__(self, name: str):
        if 'previous' not in self.keys():
            self['previous'] = Dict()
        return self[name]
    
    def __setattr__(self, name: str, value: typing.Any) -> None:
        if 'previous' not in self.keys():
            self['previous'] = Dict()

        if name in self['previous'].keys():
            self['previous'][name] = self[name]
        else:
            self['previous'][name] = None
        self[name] = value


    def __str__(self):
        return str(self.toJSON())