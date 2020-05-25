import json, ssl, re, sys, getopt
import http.client


def extract_number(s):
    result = [int(s) for s in s.split() if s.isdigit()]
    if len(result) > 0:
        return result[0]
    else:
        return 0


def version_to_number(version):
    a, b, c = version
    return 100 * a + 10 * b + c


def resolve_version(package_name):
    # print("package_name>>: %s" % package_name)

    conn = http.client.HTTPSConnection('api.nuget.org', context=ssl._create_unverified_context())
    conn.request("GET", "/v3-flatcontainer/%s/index.json" % package_name)
    response = conn.getresponse()
    bytes = response.readlines()
    conn.close()

    # print("response: %s" % bytes)
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
    opts, args = getopt.getopt(sys.argv, "v", [])
    print(opts)
    print(args)

    if len(sys.argv[1:]) == 0:
        print("No <package-name> provided")
    else:
        # print command line arguments
        for arg in sys.argv[1:]:
            print(str(next_version(arg)))
