import os
import time
import hashlib
import string
import random

from bencoder import bencode

class Torrent:

    def __init__(self, content, piece_size, trackers=[], private=False, unique=False, comment=None):
        self.data = {}

        self.data['creation date'] = int(time.time())
        self.data['created by'] = 'Torrent Creator v1.0'

        if len(trackers) > 0:
            self.data['announce'] = trackers[0]

            if len(trackers) > 1:
                self.data['announce-list'] = trackers[1:]

        self.data['info'] = self._info_dict(os.path.realpath(content), piece_size)

        if private:
            self.data['info']['private'] = True

        if unique:
            self.data['info']['unique'] = self._rand_string(32)

    def _pieces(self, files, piece_size):
        def chunks():
            chunk = b''

            for file in files:
                with open(file, 'rb') as f:
                    while True:
                        data = f.read(piece_size - len(chunk))
                        if data == b'':
                            break
                        chunk += data

                        isLastFile = file is files[-1]
                        if len(chunk) == piece_size or isLastFile:
                            yield chunk
                            chunk = b''

        digests = b''
        for piece in chunks():
            digests += hashlib.sha1(piece).digest()

        return digests

    def _info_dict(self, content, piece_size):
        info = {}
        paths = []

        info['name'] = os.path.basename(content)

        if os.path.isfile(content):
            size = os.path.getsize(content)

            info['length'] = size

            paths.append(content)
        elif os.path.isdir(content):
            info['files'] = []

            for root, dirs, files in os.walk(content):
                for file in files:
                    path = os.path.join(root, file)
                    size = os.path.getsize(path)
                    
                    file = {
                        'path': os.path.relpath(path, content).split(os.sep),
                        'length': size
                    }

                    info['files'].append(file)
                    paths.append(path)


        info['piece length'] = piece_size
        info['pieces'] = self._pieces(paths, piece_size)

        return info

    def _rand_string(self, length):
        alphabet = string.ascii_letters + string.digits
        return ''.join([ random.choice(alphabet) for i in range(length) ])

    def bencoded(self):
        return bencode(self.data)
