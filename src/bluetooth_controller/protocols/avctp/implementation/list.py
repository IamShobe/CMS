from backports.functools_lru_cache import lru_cache


class List(object):
    class Counter(object):
        def __init__(self):
            self.index = 0

    def __init__(self, type):
        self.type = type

    @classmethod
    def pack(cls, items):
        return "".join(item.pack() for item in items)

    @lru_cache()
    def unpack(self, raw_text, count=1, counter=None):
        to_ret = []
        current_counter = 0
        current_buffer = raw_text
        for _ in xrange(count):
            _counter = self.Counter()
            to_ret.append(self.type.unpack(current_buffer, counter=_counter))
            current_counter += _counter.index
            current_buffer = current_buffer[_counter.index:]

            if counter:
                global_counter = current_counter + counter.parser_index
                if global_counter >= counter.max_length:
                    break

        return to_ret
