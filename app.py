import json
import http.client
import ssl
import re
import sys


def extract_number(str):
    result = [int(s) for s in str.split() if str.isdigit()]
    if len(result) > 0:
        return result[0]
    else:
        return 0


def version_to_number(version):
    a, b, c = version
    return 100 * a + 10 * b + c


def resolve_version(package_name):
    conn = http.client.HTTPSConnection('api.nuget.org', context=ssl._create_unverified_context())
    conn.request("GET", f'/v3-flatcontainer/{package_name}/index.json')
    response = conn.getresponse()
    bytes = response.readlines()
    conn.close()

    my_json_str = ''.join([x.decode('utf-8') for x in bytes])
    json_result = json.loads(my_json_str)
    versions = json_result['versions']
    table = []
    for (a, b, c) in map(lambda x: re.split('\.', x), versions):
        a, b, c = (extract_number(a), extract_number(b), extract_number(c))
        table.append((a, b, c))

    table = sorted(table, key=version_to_number, reverse=True)
    current_version = (0, 0, 0)

    if len(table) > 0:
        current_version = table[0]

    return current_version


def next_version(package_name):
    a, b, c = resolve_version(package_name)
    return ".".join([str(a), str(b), str(c + 1)])


if __name__ == '__main__':
    # print command line arguments
    for arg in sys.argv[1:]:
        print(str(next_version(arg)))
