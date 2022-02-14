import requests
import sys
import os
import threading

found = []

log = ("""
  █████▒▄▄▄▄    █    ██   ██████ ▄▄▄█████▓▓█████  ██▀███  
▓██   ▒▓█████▄  ██  ▓██▒▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
▒████ ░▒██▒ ▄██▓██  ▒██░░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
░▓█▒  ░▒██░█▀  ▓▓█  ░██░  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
░▒█░   ░▓█  ▀█▓▒▒█████▓ ▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
 ▒ ░   ░▒▓███▀▒░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
 ░     ▒░▒   ░ ░░▒░ ░ ░ ░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
 ░ ░    ░    ░  ░░░ ░ ░ ░  ░  ░    ░         ░     ░░   ░ 
        ░         ░           ░              ░  ░   ░     
             ░                                            
   Made by ozzzozo https://github.com/ozzzozo
""")


def thread(f, t, url, file_, ex):
	try:
		for i in range(f, t):
			try:
				line = file_[i]
			except:
				break

			if not line or '#' in line:
				break

			for j in ex:
				check(url, line + "." + j)

			check(url, line)
	except KeyboardInterrupt:
		plog("Quiting", 0)
		sys.exit()

def plog(message, color):
	if color == 0:
		print("\033[1;32;31m" + "[*] " + message + "\033[m")
	elif color == 1:
		print("\033[1;32;32m" + "[*] " + message + "\033[m")
	elif color == 2:
		print("\033[1;32;33m" + "[*] " + message + "\033[m")
	elif color == 3:
		print("\033[1;32;35m" + "[*] " + message + "\033[m")

def check(url, dire):
	if len(dire) > 0:
	
		if dire in found: return
		
		con = url + dire

		try:
			response = requests.get(con)
			status = response.status_code;
		except:
			return
		
		if status >= 200 and status <= 226:
			plog(con + " - SUCCESS", 1)
		elif status == 403:
			plog(con + " - FORBIDDEN", 2)
		elif status == 204:
			plog(con + " - NO CONTENT", 1)
		elif status == 302:
			plog(con + " - MOVED TEMPORARILY", 2)
		elif status == 301:
			plog(con + " - MOVED PERMANENTLY", 2)
		elif status == 307:
			plog(con + " - TEMPORARY REDIRECT", 2)
		elif status == 400:
			plog(con + " - BAD REQUEST", 2)
		elif status == 401:
			plog(con + " - UNAUTHORIZED", 2)
		elif status == 402:
			plog(con + " - PAYMENT REQUIRED", 2)
		elif status == 504:
			plog(con + " - GATEWAY TIMEOUT", 3)

		found.append(dire)

def parseUrl(url):
	t = url

	if not t.endswith('/'):
		t = t + '/'

	if ("https://" not in t) and ("http://" not in t):
		t = "http://" + t

	return t
	

def checkForPing(url):
	domain = url
	
	port = 80

	if "https://" in domain:
		port = 443

	domain = domain.replace("http://", "")
	domain = domain.replace("https://", "")

	#domain = domain[:-1]

	if "/" in domain:
		domain = domain[0 : domain.find("/")]

	if ":" in domain:
		port = domain[domain.find(":") + 1 : len(domain)]
		domain = domain.replace(":" + port, "")

	response = os.system("nc -w 30 -vz {} {}".format(domain, port))

	if response == 0:
		plog("Target is alive", 1)
	else:
		plog("Target is dead", 0)
		sys.exit()

if __name__ == "__main__":

	makethreads = True

	try:
		print("\033[1;32;32m" + log + "\033[m")

		if len(sys.argv) >= 5:
			#url = parseUrl(sys.argv[1])
			#dic = sys.argv[2]

			ex = ""

			url = parseUrl(sys.argv[sys.argv.index("-u") + 1])
			dic = sys.argv[sys.argv.index("-w") + 1]

			if "-e" in sys.argv:
				ex = sys.argv[sys.argv.index("-e") + 1]
				ex = ex.split(',')

			checkForPing(url)

			file_ = open(dic, 'r', encoding="ISO-8859-1").read().split('\n')

			count = 0

			if url[len(url) - 1] != '/':
				url = url + '/'

			while makethreads:
				count += 1

				f = count * 10
				t = f + 20

				try:
					file_[f]
					file_[t]
				except:
					makethreads = False

				if makethreads:
					t = threading.Thread(target=thread, args=(f, t, url, file_, ex))
					#t.daemon = True
					t.start()
		else:
			plog("Syntax: python3 FBuster.py -u <url> -w <PathToWordlist> -e <extensions>(optional)", 0)
			plog("Example: python3 FBuster.py -u somewebsite.com -w /usr/share/wordlists/dirb/common.txt -e txt,php,js,pdf,bak,zip", 0)
	except KeyboardInterrupt:
		plog("Quiting", 0)
		sys.exit()
