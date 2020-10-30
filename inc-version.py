import sys
import regex

with open('pi_server/__init__.py', 'rb') as f:
    data = str(f.read(), 'utf8')

re = regex.compile(r"__version__ = '(\d+.\d+.\d+)'")


def inc_ver(s: str) -> str:
    v = list(map(int, s.split('.')))
    v[-1] += 1
    s2 = '.'.join(map(str, v))
    print(s, '->', s2)
    return s2


data, count = re.subfn(
    lambda x: f"__version__ = '{inc_ver(x.group(1))}'",
    data)

if not count:
    print('version not found!')
    sys.exit(1)

if count != 1:
    print('multiple versions found!')
    sys.exit(2)

with open('pi_server/__init__.py', 'wb') as f:
    f.write(data.encode('utf8'))
