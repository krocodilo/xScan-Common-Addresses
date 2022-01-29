
from sys import argv
from configparser import ConfigParser
from getopt import getopt, GetoptError


from connection import api_get    #connection.py in same folder

############################################
#####   Predefined values
#
url_hostname = "api.etherscan.io"       # which equals to https://api.etherscan.io/...
api_token = "YourApiKeyToken"
api_max_tr = 10000               # request last X transactions
address = ""
show_me_top = 10        # show only top 10 most used destination addresses
#
############################################

url = "https://{}/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset={}&sort=desc&apikey={}"


def print_arg_help():
    print(
        '\nUsage:  <executable> <address> [options]'
        '\nOptions:'
        '\n\t-h\t\t->\tPrint this help menu'
        '\n\t--hostname\t->\tSpecify the hostname of the API server (default: "' + url_hostname + '")'
        '\n\t--last\t\t->\tRequest the last X transactions (default: ' + str(api_max_tr) + ')'
        '\n\t--token\t\t->\tSpecify your API token (default: "' + api_token + '")'
        '\n\t--top\t\t->\tShow the top X most used addresses (default: ' + str(show_me_top) + ')\n'
        '\nYou can also use the config.ini file, but keep in mind that CLI arguments have higher priority.\n\n'
    )

def parse_arguments():
    global url_hostname, api_token, address, show_me_top, api_max_tr

    conf = ConfigParser()
    if len(conf.read("config.ini")) > 0:
        if conf.has_option("config", "url_hostname"): url_hostname = conf.get("config", "url_hostname")
        if conf.has_option("config", "api_token"): api_token = conf.get("config", "api_token")
        if conf.has_option("config", "address"): address = conf.get("config", "address")
        if conf.has_option("config", "api_max_transactions"): api_max_tr = conf.getint("config", "api_max_transactions")
        if conf.has_option("config", "show_me_top"): show_me_top = conf.getint("config", "show_me_top")

    try:
        address = argv[1]
        opts, args = getopt(argv[2:], "h:", ["hostname=", "token=", "top=", "last="])

        for opt, arg in opts:
            if opt == '--hostname':
                url_hostname = arg
            elif opt == '--last':
                api_max_tr = arg
            elif opt == '--token':
                api_token = arg
            elif opt == '--top':
                show_me_top = arg

    except GetoptError as e:
        print("\nError: ", e)
        exit()


def print_results(title, results):

    print("\n"+ title)

    if show_me_top > len(results): top = len(results)
    else: top = show_me_top

    for i in range(0, top):
        highest = ""
        for key in results:
            if len(highest) == 0:
                highest = key
            elif results.get(key) > results.get(highest):
                highest = key
        
        print("\t" + highest + " - appears ", results.get(highest), " times")
        results.pop(highest)



def start():
    transactions = api_get( url.format(url_hostname, address, api_max_tr, api_token) )["result"]

    ins = dict()
    outs = dict()
    for tr in transactions:
        if tr["from"].lower() != address.lower():
            # If my address is not the sender: is the receiver (transaction going in)
            sender = tr["from"]       # get sender address of this transaction
            if sender in ins:
                ins[sender] = ins.get(sender) + 1
            else:
                ins.update( {sender : 1} )

        else:
            # If my address is the sender (transaction going out)
            target = tr["to"]       # get recipient address of this transaction
            if target in outs:
                outs[target] = outs.get(target) + 1
            else:
                outs.update( {target : 1} )

    print_results("\nTop "+str(show_me_top)+" most used for transactions going Out:", outs)
    print_results("\nTop "+str(show_me_top)+" most used for transactions going In:", ins)
        

if __name__ == '__main__':

    if len(argv) < 2 or argv[1] == '-h':   # at least executable + address
        print_arg_help()
        exit()
    
    try:
        parse_arguments()
        start()

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()

    # except Exception as e:
    #     print("\n\nError")
    #     print(str(e) + '\\\\\\\n' + traceback.format_exc(5) + '///\n')
    #     exit()

    print()