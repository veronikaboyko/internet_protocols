import subprocess
import re
import sys


def traceroute(target):
    output = subprocess.getoutput('traceroute {}'.format(target))
    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = re.findall(ip_regex, output)
    print('№\tIP Address\tASN')
    for i, ip in enumerate(ips):
        try:
            whois_output = subprocess.getoutput('whois {}'.format(ip))

            asn_regex = r'AS[0-9]+'
            asn_match = re.search(asn_regex, whois_output)
            asn = asn_match.group(0) if asn_match else '-'
            print(f'{i+1}\t{ip}\t{asn}')

        except Exception as e:
            print(f'{i+1}\t{ip}\terror')


def read_input():
    if len(sys.argv) < 2:
        print('Usage: python tracer.py <target>')
        sys.exit(1)
    return sys.argv[1]


def main():
    target = read_input()
    if not re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$', target):
        print('Error: Incorrect input data')
    else:
        traceroute(target)


if __name__ == '__main__':
    main()
