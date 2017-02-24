# Torrent Creator
I wanted to explore how a torrent file is created, so I decided to create a program that does it for you. This program is for educational purposes: use it at your own peril.

## Installation
Run the following command:
```bash
$ python3 setup.py install
```

## Usage
```
$ torrent-creator --help
usage: torrent-creator [-h] [--trackers tracker [tracker ...]] [--private]
                       [--piece-size 16KiB/32KiB/2MiB/etc.] --output path
                       [--comment comment] [--unique]
                       file/dir

Create a torrent file.

positional arguments:
  file/dir              a file or directory that you want to add to the
                        torrent

optional arguments:
  -h, --help            show this help message and exit
  --trackers tracker [tracker ...]
                        a list of trackers that you want to use
  --private             mark the torrent private
  --piece-size 16KiB/32KiB/2MiB/etc.
                        the piece size
  --output path         the path of the torrent that will be created
  --comment comment     a comment which will be added to the torrent
  --unique              make the info-hash unique by adding random data to the
                        info dictionary
```