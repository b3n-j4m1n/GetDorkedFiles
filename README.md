# GetDorkedFiles
Google dork specified file(s) in specified website and optionally download the results.

It uses three techniques to evade the CAPTCHA (which work better than expected but aren't perfect), use in moderation or with a proxy.

https://en.wikipedia.org/wiki/Google_hacking

# Usage
```
# python3 GetDorkedFiles.py
python3 GetDorkedFiles.py [-h] [-v] [-s SITE] [-f FILES] [-u URL-LIST]

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
                      file containing a list of file urls to download
```

TODO
- include Bing results
