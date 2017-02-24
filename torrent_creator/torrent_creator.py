import argparse
import os
import os.path
import sys
import re

from . import math_utils
from .torrent import Torrent

def parse_piece_size(size):
    matches = re.findall('^(\d+)\s*(KiB|MiB)$', str(size))[0]
    if len(matches) != 2:
        raise ValueError('Invalid size')

    number, unit = matches

    bytes_in_kib = 2**10
    bytes_in_mib = 2**20
    if unit == 'KiB':
        return int(number) * bytes_in_kib
    elif unit == 'MiB':
        return int(number) * bytes_in_mib

    raise ValueError('Invalid unit')


def validate_args(args):
    if not os.path.exists(args.content):
        print('The provided file or directory does not exist: {}'.format(args.content))
        sys.exit(1)

    if args.piece_size != False:
        try:
            piece_size = parse_piece_size(args.piece_size)
        except ValueError:
            print('The provided piece size is invalid')
            sys.exit(1)

        if not math_utils.is_power(piece_size, 2):
            print('The provided piece size must be a power of 2')
            sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description='Create a torrent file.')
    parser.add_argument('--trackers', metavar='tracker', type=str, default=[], nargs='+', help='a list of trackers that you want to use')
    parser.add_argument('--private', action='store_true', default=False, help='mark the torrent private')
    parser.add_argument('--piece-size', metavar='16KiB/32KiB/2MiB/etc.', type=str, default='1MiB', help='the piece size')
    parser.add_argument('--output', metavar='path', type=str, required=True, help='the path of the torrent that will be created')
    parser.add_argument('--comment', metavar='comment', type=str, help='a comment which will be added to the torrent')
    parser.add_argument('--unique', action='store_true', default=False, help='make the info-hash unique by adding random data to the info dictionary')
    parser.add_argument('content', metavar='file/dir', type=str, help='a file or directory that you want to add to the torrent')

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    validate_args(args)

    torrent = Torrent(args.content, parse_piece_size(args.piece_size), trackers=args.trackers, private=args.private, unique=args.unique, comment=args.comment)

    with open(args.output, 'wb') as f:
        f.write(torrent.bencoded())


if __name__ == '__main__':
    main()