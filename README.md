# FBuster v1.3 (@ozzzozon)

FBuster is a fast tool to brute force directories and files for websites

## How to use

Syntax:

$ python3 FBuster.py -u url -w path/to/wordlist -e ext,ens,ion,s(optional)

Example:

$ python3 FBuster.py -u somewebsite.com -w /usr/share/wordlists/dirb/common.txt -e txt,php,js,zip

### Requirements
netcat<br />
python3

**note: FBuster is not designed for windows**<br />
**note: if you add extensions it will make FBuster slower obv**<br />
**note: FBuster is not designed for small wordlists**<br />
