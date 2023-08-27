import requests
import argparse
import concurrent.futures
import threading
from tabulate import tabulate
from colorama import init, Fore


def main(args):
    results = []
    # Opens wordlist chosen by user, if one is not given a default one will be used
    try:
        with open(args.wordlist) as f:
            payloads = f.readlines()

    except TypeError:
        with open("mylist.txt") as f:
            payloads = f.readlines()

    # Error Handling, If user defined wordlist isn't found, print error message out and exit the code.
    except FileNotFoundError:
        print("Wordlist not found.")
        exit()

    def lazy_fuzz(payload):
        url = args.url.replace("FUZZ", payload.strip())
        try:
            request = requests.get(url, cookies=args.cookies, proxies=args.proxy)
            content_length = request.headers.get("Content-Length")
            status_code = request.status_code
            if status_code != args.sc:
                if int(content_length) != args.cl:
                    results.append((payload, str(status_code), str(content_length)))

        except Exception as e:
            print(f"An error has occurred, {e}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(lazy_fuzz, payloads)
    user_display(results)


def user_display(results):
    # Initializing Colorama and setting the colors for the status code output
    init(autoreset=True)
    colors = {200: Fore.GREEN,
              404: Fore.RED,
              301: Fore.BLUE,
              302: Fore.BLUE,
              307: Fore.BLUE,
              308: Fore.BLUE,
              400: Fore.RED,
              403: Fore.RED,
              406: Fore.RED,
              407: Fore.RED,
              409: Fore.RED,
              410: Fore.RED,
              421: Fore.RED,
              500: Fore.YELLOW,
              502: Fore.YELLOW,
              503: Fore.YELLOW,
              504: Fore.YELLOW,
              511: Fore.YELLOW,
              }
    # Giving the user a more presentable output with rows, columns and color coded status codes
    formatted_results = []
    for payload, status_code, content_length in results:
        status_colors = colors.get(int(status_code), "")
        formatted_results.append([payload, f"{status_colors}{status_code}{Fore.RESET}", content_length])

    print_lock = threading.Lock()
    with print_lock:
        table_rows = ["Payload", "Status Code", "Content Length"]
        print(tabulate(formatted_results, headers=table_rows, colalign=('left', 'center', 'center')))


def handle_args():
    parser = argparse.ArgumentParser(prog="Lazy Fuzz", description="Directory Fuzzer")
    parser.add_argument('-u', '--url', type=str, help="Enter your Url here, make sure to add 'FUZZ'", required=True)
    parser.add_argument('-c', '--cookies', type=str, help="Use Cookies")
    parser.add_argument('-p', '--proxy', type=str, help="Use Proxies")
    parser.add_argument('--sc', type=int, help="Exclude Status Code")
    parser.add_argument('--cl', type=int, help="Exclude Content Length")
    parser.add_argument('-w', '--wordlist', type=str, help="Wordlist")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Chose Amount of Threads, Default is 10")
    args = parser.parse_args()

    # Error Handling, adding 'http' if user forgets to enter 'http' or 'https' in the url argument
    if not args.url.startswith("http://") and not args.url.startswith("https://"):
        args.url = ''.join(("http://", args.url))

    # Error Handling, Checking if url is valid
    try:
        requests.get(args.url, cookies=args.cookies, proxies=args.proxy)
        if "FUZZ" not in args.url:
            print("Missing 'FUZZ' parameter"), exit()
        main(args)
    except requests.exceptions.ConnectTimeout:
        print("Connection timed out. Check url to make sure it is valid or try using another proxy.")


if __name__ == "__main__":
    handle_args()
