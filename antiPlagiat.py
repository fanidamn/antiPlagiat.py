"""

    *** antiPlagiat by crryx
    *   levenshtein method example.
    *** 22.09.21

"""

                #
                # list of sites to pars <p> tag and check
                #
url_list = {
    "https://learninbound.com/": "",
    "https://learninbound.com/community/": "",
    "https://learninbound.com/blog/buyer-funnel/": "",
    "https://learninbound.com/blog/buyer-funnel/": "",
    "https://learninbound.com/videos/ross-simmonds-2019/": "",
    "https://learninbound.com/videos/april-dunford-2019/": "",
    "https://learninbound.com/blog/": "",
    "https://learninbound.com/terms/": "",
    "https://learninbound.com/privacy-policy/": ""
}
plagiat_list = {}

                #
                # library importing
                #
import requests
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

                #
                # setting up headers for not to get 403 forbidden error
                # set a domain (for checking func)
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.197"}
domain = "https://learninbound.com"

                #
                # a <p> tag parsing function
                # using libraries: requests, bs4
def p_tag_parsing():
    for i in url_list:                                      # here we run the links list
        print("trying: ", i)                                # printing current link in process
        conn = requests.get(i, headers=headers)             # connecting to the link from "i" variable
        if conn.status_code == 200:                         # if 200 (accepted and loaded) goin' next step
            bs = BeautifulSoup(conn.text, "lxml")           # declare a lxml text type into "bs" variable
            pTags = bs.find_all("p")                        # declare a <p> tag for found on link

            for tags in pTags:                              # run the list with <p> tags for "tags" variable
                for v in tags:                              # run the "tags" list for "v" variable | ???
                    url_list[i] += str(v)                   # declare a key ("v") for "url_list" list in "i" position

            conn.close()                                    # closing an connection for not to get a troubles
        else:                                               # if status_code isn't 200, then:
            print("connection err, got ", conn.status_code) # we print a error in console
    main()                                                  # restart a main thread function

                #
                # a check ration function
                # using libraries: dict, fuzzymuzzy (levenshtein method)
def start_check():
    for iId, i in enumerate(list(url_list.values())):       # run a list for get link ratio in order
        for kId, k in enumerate(list(url_list.values())):   # run a list for link ratio in order w/o first value
            if iId == kId:                                  # if we found another links, we just skip them
                pass                                        # pass...
            else:
                ratio = fuzz.ratio(i, k)                    # fuzzymuzzy func (checking a text ratio)
                if ratio == 0:                              # if the ratio = 0 then we've pass that links (will be broken)
                    pass                                    # pass...
                else:
                    print(f"[*] {list(url_list)[iId].split(domain)[1]} and {list(url_list)[kId].split(domain)[1]} | have {ratio}% ratio")
                                                            # debugging a links checking
                    if ratio >= 50:
                                                            # checks if ratio > 50%
                        print(f"[!] ||| An {list(url_list)[iId].split(domain)[1]} looks like plagiat of {list(url_list)[kId].split(domain)[1]}!!!")
                                                            # pinging user about plagiat will be founded
    print("Domain is: ", domain)
                                                            # just for debug

def main():
    input_ = input("'getp' or 'check': ")                   # asks a user "pars <p> tag" or "check ratio"
    if "getp" in input_:                                    # if getp then we start parsing
        p_tag_parsing()                                     # call func
    elif "check" in input_:                                 # if check then we start check ratio
        start_check()                                       # call func

if __name__ == "__main__":
    main()