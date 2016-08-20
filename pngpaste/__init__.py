import datetime
import os
import sys
import atexit
from subprocess import call


def capture():
    try:
        call(['/usr/local/bin/pngpaste', '-v'], stderr=open('/dev/null', 'w'))
    except OSError:
        print('please preinstall pngpaste use `brew install pngpaste` before use this script')
        sys.exit()

    file_name = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.png')
    file_path = os.path.join('/tmp', file_name)
    atexit.register(lambda x: os.remove(x) if os.path.exists(x) else None, file_path)
    save = call(['/usr/local/bin/pngpaste', file_path])
    if save == 1:
        sys.exit()
    return file_path, file_name


if __name__ == '__main__':
    print(capture())
