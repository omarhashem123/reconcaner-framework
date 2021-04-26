import concurrent.futures,requests
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', help='file contain subdomains with http and https')
parser.add_argument('-o', help='file to write output')
parser.add_argument('-t', help='threads')
args = parser.parse_args()

def clickjacking_requester(subdomain):
    req = requests.get(subdomain)
    headers = dict((k.lower(), v.lower()) for k, v in req.headers.items())
    if "x-frame-options" not in headers and("content-security-policy" not in headers or "frame-ancestors" not in headers["content-security-policy"]):
        output.write(subdomain + "\n")
        print(subdomain)

def logo():
    print("""
 ██████╗██╗     ██╗ ██████╗██╗  ██╗     ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔════╝██║     ██║██╔════╝██║ ██╔╝     ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ 
██║     ██║     ██║██║     █████╔╝      ██║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗
██║     ██║     ██║██║     ██╔═██╗ ██   ██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║
╚██████╗███████╗██║╚██████╗██║  ██╗╚█████╔╝██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝
 ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
    Coded by:Omar Hashem
    Twitter:@omarhashem666
        """)
if __name__ == '__main__':
    if args.i and args.t and args.o is not None:
        logo()
        input = set(open(args.i).readlines())
        subdomains = set()
        for i in input:
            subdomains.add(i.strip())
        output = open(args.o, "a")
        with concurrent.futures.ThreadPoolExecutor(max_workers=(int(args.t))) as e:
            e.map(clickjacking_requester, subdomains)
    else:
        logo()
        parser.print_help()