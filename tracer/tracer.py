import subprocess
import re
import sys


def get_info(ip):
    try:
        whois_output = subprocess.getoutput('whois {}'.format(ip))

        asn_regex = r'AS[0-9]+'
        asn_match = re.search(asn_regex, whois_output)
        asn = asn_match.group(0) if asn_match else '-'

        country_regex = r'country:(.*)'
        country_match = re.search(country_regex, whois_output, re.IGNORECASE)
        country = country_match.group(1).strip() if country_match else '-'

        isp_regex = r'org-name:(.*)'
        isp_match = re.search(isp_regex, whois_output, re.IGNORECASE)
        isp = isp_match.group(1).strip() if isp_match else '-'

        return asn, country, isp

    except Exception:
        pass

    return '-', '-'


def traceroute(target):
    output = subprocess.getoutput('traceroute {}'.format(target))
    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = re.findall(ip_regex, output)
    print('№\tIP Address\t\tASN\t\tCountry\t\tProvider')
    for i, ip in enumerate(ips):
        try:
            asn, country, isp = get_info(ip)
            print(f'{i + 1}\t{ip}\t\t{asn}\t\t{country}\t\t{isp}')
        except Exception as e:
            print(f'{i + 1}\t{ip}\t\t-\t\t-\t\t-')


def read_input():
    if len(sys.argv) != 2:
        print('Type \'python tracer.py -h\' to get help')
        sys.exit(1)
    elif sys.argv[1] == '-h':
        print('\nAutonomous system tracing\n')
        print('Usage: python tracer.py <target>')
        print('<target> - the node to be traced to (ip address or domain name)\n')
        sys.exit(1)
    return sys.argv[1]


def main():
    target = read_input()
    if not re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$', target):
        print('Error: Incorrect input data')
        print('Type \'python tracer.py -h\' to get help')
    else:
        traceroute(target)


if __name__ == '__main__':
    main()
