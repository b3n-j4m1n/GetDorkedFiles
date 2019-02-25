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
```
# python3 GetDorkedFiles.py -s github.com -f doc,xls
[*] looking in search results 0 - 100
[*] attempting to evade CAPTCHA...
[*] looking in search results 100 - 200
[*] 30 files found, list saved in /root/GetDorkedFiles/github.com-20190225200528/github.com-20190225200528.list
[?] download files (y/n)? [warning: file size not considered, check url list and re-run with -u option, else download everything]: y
[+] downloading - http://alloyteam.github.com/DevelopmentCodes.doc
[+] downloading - http://yannik520.github.com/liyanqing.doc
[+] downloading - http://tchalvak.github.com/n/english/Humn2201Ronalds_Rv2.doc
[+] downloading - https://github.com/qreal/qreal/wiki/ConstraintsEditor_description.doc
[+] downloading - https://github.com/qreal/qreal/wiki/matveev.doc
[+] downloading - https://github.com/qreal/qreal/wiki/bryksin.doc
[+] downloading - https://github.com/Esenin/qreal/wiki/matveev.doc
[+] downloading - https://github.com/qreal/qreal/wiki/Takun_diploma.doc
[+] downloading - http://elainehu.github.com/demo/Notes/photoshop_notes.doc
[+] downloading - https://github.com/qreal/qreal/wiki/naidionysheva.doc
[-] 404 not found - https://github.com/OpenCyclone/model/wiki/template_data.doc
[+] downloading - https://github.com/vkaliteevsky/qreal/wiki/simonova.doc
[+] downloading - https://github.com/qreal/qreal/wiki/bakalov.doc
[-] 404 not found - https://github.com/OpenCyclone/model/wiki/template_algorithm.doc
***snip***
#
```

TODO
- include Bing results
