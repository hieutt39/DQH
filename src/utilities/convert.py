class Dict2Object(object):
    def __init__(self, *args, **argd):
        self.__dict__.update(dict(*args, **argd))
