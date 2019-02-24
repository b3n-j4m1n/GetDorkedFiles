import requests
from bs4 import BeautifulSoup
import re
import time
import os
import argparse
import random
import urllib.request
from urllib.error import HTTPError
import datetime
import sys
import logging


def message():
    return """python3 GetDorkedFiles.py [-h] [-v] [-s SITE] [-f FILES] [-u URL-LIST]

Google dork specified file(s) in specified website and optionally download the
results.

documents - csv,doc,docx,pdf,ppt,xls,xlsx
sensitive - 7z,apk,bak,bat,bin,conf,dat,db,db2,db3,gz,htaccess,inf,ini,ipa,key,
            license,log,pem,ps1,ps2,rar,sh,sql,tar,tgz,vbs,xml,zip


optional arguments:
-h, --help            show this help message and exit
-v, --verbose         increase output verbosity
-s, --site            site in which to search for files, e.g. microsoft.com
-f, --files           filetype(s), accepts a comma-delimited list
-u, --url-list        instead of Google dorking, specify the absolute path of a
                      file containing a list of file urls to download"""


def parse_arguments():
    parser = argparse.ArgumentParser(usage=message(), add_help=False)
    parser.add_argument("-s", "--site", default="")
    parser.add_argument("-f", "--files", default="")
    parser.add_argument("-u", "--url-list", default=False)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.files:
        args.files = args.files.split(",")

    return args


def get_dorked_files(site, file_types, timestamp, url_list):
    if url_list is False:

        download_directory = site + "-" + timestamp
        found_files_list = (
            site + "-" + timestamp + "/" + site + "-" + timestamp + ".list"
        )
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
        file = open(found_files_list, "w")

        start = 0

        while start < 1001:
            # a list of user-agent headers that will be randomly used in the
            # request each loop to evade the CAPTCHA
            user_agent = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38",
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
            ]
            header = {"User-Agent": random.choice(user_agent)}
            # the Google dork
            request = (
                "https://www.google.com.au/search?num=100&start="
                + str(start)
                + "&q=site%3A"
                + site
                + "+filetype%3A"
                + "+OR+filetype%3A".join(file_types)
            )

            logging.info("[*] request - " + request)

            print(
                "[*] looking in search results "
                + str(start)
                + " - "
                + str(int(start + 100))
            )
            response = requests.get(request, headers=header)
            soup = BeautifulSoup(response.text, "lxml")

            if "did not match any documents" in soup.text:
                break

            if "detected unusual traffic from your computer" in soup.text:
                print("[!] blocked by CAPTCHA")

                captcha_prompt = input(
                    "[?] continue (y/n)? [wait or change proxy before resuming]: "
                )

                if captcha_prompt == ("n"):
                    print("[*] exiting")
                    exit()
                elif captcha_prompt != ("y"):
                    print("[!] invalid response")
                    exit()
                continue
            # scraping all the results and writing to the url list, the regex is
            # a nightmare...
            else:
                for line in soup.findAll("a", href=True):
                    for ext in file_types:
                        url = re.search(r"(http|https)" + "(.*?)\." + ext, line['href'])
                        if url is not None and not re.search(r"webcache.googleusercontent.com", str(line)) and not re.search(r"translate.google.com", str(line)):
                            file.write(url.group(0) + "\n")

                            logging.info(url.group(0))

                start = start + 100

                # evading the CAPTCHA with a random length pause between each
                # Google dork search, and random three letter normal search
                print("[*] attempting to evade CAPTCHA...")
                time.sleep(random.randint(3, 7))
                letters = "abcdefghijklmnopqrstuvwxyz"
                random_search = (
                    "https://www.google.com.au/search?q="
                    + random.choice(letters)
                    + random.choice(letters)
                    + random.choice(letters)
                )
                requests.get(random_search, headers=header)
                time.sleep(random.randint(3, 7))

        file.close()

        file_count = sum(1 for line in open(found_files_list))

        if file_count == 0:
            print("[-] 0 files found\n[*] exiting")
            exit()
        else:
            print(
                "[*] "
                + str(file_count)
                + " files found, list saved in "
                + os.getcwd()
                + os.path.dirname(download_directory)
                + '/'
                + found_files_list
            )

        download_prompt = input(
            "[?] download files (y/n)? [warning: file size not considered, check url list and re-run with -u option, else download everything]: "
            )

        if download_prompt == ("n"):
            print("[*] exiting")
            exit()
        elif download_prompt != ("y"):
            print("[!] invalid response")
            exit()

        # if the search finds a very large file it may cause issues with the
        # download loop, consider downloading it manually, removing it from the
        # saved url list, and re-running with the -u option
        for urls in open(found_files_list):
            filename = urls[urls.rfind("/") + 1 :]
            file_save = site + "-" + timestamp + "/" + filename.rstrip("\r\n")

            try:
                urllib.request.urlretrieve(urls, file_save)
                print("[+] downloading - " + urls.rstrip("\r\n"))
            except HTTPError:
                print("[-] 404 not found - " + urls.rstrip("\r\n"))
    else:
        print(
            "[*] "
            + str(sum(1 for line in open(url_list)))
            + " files in url list, downloading to "
            + os.path.dirname(url_list)
            + '/'
        )

        for urls in open(url_list):
            filename = urls[urls.rfind("/") + 1 :]
            file_save = os.path.dirname(url_list) + "/" + filename.rstrip("\r\n")

            try:
                urllib.request.urlretrieve(urls, file_save)
                print("[+] downloading - " + urls.rstrip("\r\n"))
            except HTTPError:
                print("[-] 404 not found - " + urls.rstrip("\r\n"))


def main():
    if len(sys.argv) <= 1 or "-h" in sys.argv or "--help" in sys.argv:
        print("usage: " + message())
        exit()

    timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M%S")

    args = parse_arguments()

    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)

    get_dorked_files(args.site, args.files, timestamp, args.url_list)


if __name__ == "__main__":
    main()
