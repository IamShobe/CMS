# taken from https://raw.githubusercontent.com/jowave/vcard2to3/master/vcard2to3.py
# and altered alittlebit
from StringIO import StringIO

import re
import quopri


class VCard(object):
    BEGIN = 'BEGIN:VCARD'
    END = 'END:VCARD'
    FN = re.compile('FN[:;]')
    NICKNAME = re.compile('NICKNAME[:;]')

    def __init__(self, prune_empty=False):
        self.reset()
        self._prune_empty = prune_empty

    def reset(self):
        self.lines = []
        self._omit = False
        self._fn = None

    def add(self, line):
        self.lines.append(line)
        if VCard.FN.match(line):
            self._fn = line

    def omit(self):
        self._omit = True

    def valid(self):
        return self._fn != None

    def write(self, to):
        if self._omit:
            return
        nick_idx = -1
        for i, l in enumerate(self.lines[1:-1]):
            if VCard.NICKNAME.match(l):
                if self._fn and (self._fn[3:] == l[9:]):
                    del (self.lines[i + 1])  # NICKNAME == FN => remove nickname
                else:
                    nick_idx = i + 1
        if not self.valid() and nick_idx >= 0 and (
                not self._prune_empty or len(self.lines) > 4):
            # no FN but NICKNAME found, use it
            self.lines[nick_idx] = self.lines[nick_idx].replace('NICKNAME',
                                                                'FN', 1)
            self._fn = self.lines[nick_idx]
            nick_idx = -1
        if not self.valid():
            return
        for line in self.lines:
            to.write(line)


class QuotedPrintableDecoder(object):
    quoted = re.compile('.*(;CHARSET=.+;ENCODING=QUOTED-PRINTABLE)')

    def __init__(self):
        self._consumed_lines = ''
        pass

    def __call__(self, line):
        return self.decode(line)

    def decode(self, line):
        line = self._consumed_lines + line  # add potentially stored previous lines
        self._consumed_lines = ''
        m = QuotedPrintableDecoder.quoted.match(line)
        if m:
            line = line[:m.start(1)] + line[m.end(1):]
            return quopri.decodestring(line).decode('UTF-8')
        return line

    def consume_incomplete(self, line):
        # consume all lines ending with '=', where the first line started the quoted-printable
        if line.endswith('=\n'):
            m = QuotedPrintableDecoder.quoted.match(line)
            if m or len(self._consumed_lines) > 0:
                self._consumed_lines += line
                return True
        return False


class Replacer(object):
    def __init__(self):
        self.replace_filters = []
        self.replace_filters.append((re.compile('^VERSION:.*'), 'VERSION:3.0'))
        # self.replace_filters.append( (re.compile('^PHOTO;ENCODING=BASE64;JPEG:'), 'PHOTO:data:image/jpeg;base64,') ) # Version 4.0
        self.replace_filters.append((re.compile('^PHOTO;ENCODING=BASE64;(\w+?):'),
                                     'PHOTO;ENCODING=b;TYPE=\\1:'))  # Version 3.0
        self.replace_filters.append((re.compile(';X-INTERNET([;:])'), '\\1'))
        self.replace_filters.append((re.compile(
            '^X-ANDROID-CUSTOM:vnd.android.cursor.item/nickname;([^;]+);.*'),
                                     'NICKNAME:\\1'))
        self.replace_filters.append(
            (re.compile(';PREF([;:])'), ';TYPE=PREF\\1'))  # Version 3.0
        # self.replace_filters.append( (re.compile(';PREF([;:])'), ';PREF=1\\1') ) # Version 4.0
        self.replace_filters.append((re.compile('^X-JABBER(;?.*):(.+)'),
                                     'IMPP\\1:xmpp:\\2'))  # Version 4.0
        self.replace_filters.append(
            (re.compile('^X-ICQ(;?.*):(.+)'), 'IMPP\\1:icq:\\2'))  # Version 4.0
        self.replace_filters.append((re.compile(
            '^(TEL|EMAIL|ADR|IMPP);([^;:=]+[;:])'), Replacer.type_lc))
        self.replace_filters.append(
            (re.compile('^EMAIL:([^@]+@jabber.*)'), 'IMPP;xmpp:\\1')),
        self.replace_filters.append(
            (re.compile('^X-IRMC-CALL-DATETIME;(\w+):(\d+)'),
             'X-IRMC-CALL-DATETIME;TYPE=\\1:\\2'))

    @classmethod
    def type_lc(cls, matchobj):
        return matchobj.group(1) + ';TYPE=' + matchobj.group(2).lower()

    def __call__(self, line):
        return self.replace(line)

    def replace(self, line):
        for r in self.replace_filters:
            line = r[0].sub(r[1], line)
        return line


class Remover:
    def __init__(self, patterns):
        self.filters = []
        if patterns is not None:
            for p in patterns:
                self.filters.append(re.compile(p))

    def __call__(self, line):
        return self.remove(line)

    def remove(self, line):
        for f in self.filters:
            if f.match(line):
                return True
        return False


def as_utf8(line):
    try:
        return line.encode("utf-8")

    except:
        return line


def convert(infile):
    outfile = StringIO()
    vcard = VCard()
    decoder = QuotedPrintableDecoder()
    replace = Replacer()

    for line in infile.split("\n"):
        line += "\n"
        if decoder.consume_incomplete(line):
            continue

        if line.startswith(VCard.BEGIN):
            vcard.reset()

        line = decoder.decode(line)
        line = replace(line)
        vcard.add(as_utf8(line))

        if line.startswith(VCard.END):
            vcard.write(outfile)

    return outfile.getvalue()
