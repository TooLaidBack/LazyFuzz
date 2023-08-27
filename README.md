<h1 align="center">LazyFuzz</h1>
<h2 align="center">Web Directory Fuzzer</h2>

**Disclaimer:** I take no responsibility for how you use this script. Use at your own discretion.

# LazyFuzz 1.0
This is a basic web directory fuzzer that I will continue to work on and update as there are some kinks that need to be worked out, other than that the script works completely fine as is and any feedback would be helpful.
```
usage: Lazy Fuzz [-h] -u URL [-c COOKIES] [-p PROXY] [--sc SC] [--cl CL] [-w WORDLIST] [-t THREADS]

Directory Fuzzer

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Enter your Url here, make sure to add 'FUZZ'
  -c COOKIES, --cookies COOKIES
                        Use Cookies
  -p PROXY, --proxy PROXY
                        Use Proxies
  --sc SC               Exclude Status Code
  --cl CL               Exclude Content Length
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -t THREADS, --threads THREADS
                        Chose Amount of Threads, Default is 10
  ```
  
Install Libraries:
  
    pip install -r requirements.txt
