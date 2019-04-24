from collections import OrderedDict

from bitarray import bitarray

from parameter import ConstantSizeParameter, ComplexParameter, \
    SingleUnknownSizeParameter


class Structure(object):
    PARAMETERS = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.assigned_params = OrderedDict()

        self.params_dict = OrderedDict()
        for param in self.get_all_params():
            self.params_dict[param.name] = param

        self.initialize()

    @classmethod
    def get_all_params(cls):
        return cls.PARAMETERS

    def initialize(self):
        self.initialize_default_params()
        self.fill_values()
        self.validate_all_present()

    def __getattr__(self, item):
        return self.assigned_params[item]

    def ignore_keys(self):
        return ["params_dict", "assigned_params", "kwargs"]

    def __setattr__(self, key, value):
        if key in self.ignore_keys():
            super(Structure, self).__setattr__(key, value)
            return

        param = self.params_dict[key]

        if isinstance(param,
                      (ConstantSizeParameter, SingleUnknownSizeParameter)):
            linked_param = self.params_dict[param.linked_length_param]
            setattr(self, linked_param.name, len(value))

        if isinstance(param, ComplexParameter):
            linked_param = self.params_dict[param.linked_length_param]
            setattr(self, linked_param.name, len(param.type.pack(value)))

        param.validate(value)
        self.assigned_params[key] = value

    def __dir__(self):
        res = dir(type(self)) + list(self.__dict__.keys())
        res.extend(self.params_dict.keys())
        return res

    def validate_all_present(self):
        for param in self.params_dict.values():
            if param.default is not None:
                if not hasattr(self, param.name):
                    raise RuntimeError("Required param `{}` is not set!".format(
                        param.name))

    def initialize_default_params(self):
        for param in self.params_dict.values():
            if param.default is not None:
                setattr(self, param.name, param.default)

    def fill_values(self):
        for key, value in self.kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{}(**{})".format(
            self.__class__.__name__,
            self.kwargs
        )

    def pack_params(self):
        params = []
        for param in self.params_dict.values():
            value = getattr(self, param.name)
            params.append(param.pack(value))

        return params

    @classmethod
    def unpack_params(cls, raw_params, kls=None, counter=None):
        current_index = 0
        params = OrderedDict()
        parameters = kls.get_all_params() if kls else cls.get_all_params()
        for param in parameters:
            length = param.length
            special = {}
            if isinstance(param, SingleUnknownSizeParameter):
                length = params[param.linked_length_param]
                special["length"] = params[param.linked_length_param]

            elif isinstance(param, (ConstantSizeParameter, ComplexParameter)):
                length = params[param.linked_length_param] * param.length
                special["count"] = params[param.linked_length_param]

            if isinstance(param, ComplexParameter):
                value = param.unpack(raw_params[current_index:], **special)
                length = len(value)

            else:
                value = param.unpack(
                    raw_params[current_index:current_index + length], **special)

            params[param.name] = value
            current_index += length

        if counter:
            counter.index += current_index

        return params
