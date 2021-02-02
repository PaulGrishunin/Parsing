#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Pavel Hryshunin, grupa 1


   ### Parser Actual free proxy ports from (for example) http://foxtools.ru/Proxy  using Beautifulsoup4  
   ### And write results to file:  proxy_list_checked.txt

import sys

import requests
from bs4 import BeautifulSoup
import socket
from colorama import init
init()

### Check for args / Help
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-h'):
        print('''\033[33m Proxies can be used for a variety of purposes, including: to solve problems with performance, security, network load balancing, gaining access to local/closed network sections, etc. Attackers can use proxies to preserve their anonymity on the network, or to intercept other people's data, or to replace data. \033[00m
            On the page \033[04m http://foxtools.ru/Proxy \033[00m (for example) every day the list of free proxy servers is updated with the country of the proxy, level of anonymity, response time. This script collects the most current proxy server addresses and writes them to a text file ( proxy_list_checked.txt)  for future use. 
\033[31m "-h" | --help Prints this help message\033[00m''')
        sys.exit()


def get_html(site):
    r = requests.get(site)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    head = soup.find('thead').find_all('tr')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')

    for tr in head:
        th = tr.find_all('th')
        ip1 = th[1].text
        port1 = th[2].text
        country1 = th[3].text.replace('\xa0', '')
        anonym1 = th[4].text.replace('\r\n        ', '')
        types1 = th[5].text.replace('\r\n\t\t\t\t\t', '').replace('\r\n        ', '')
        time1 = th[6].text

        data1 = (ip1, port1, country1, anonym1, types1, time1)
        print(", ".join([str(s) for s in data1]))
        
        for tr in line:
            td = tr.find_all('td')
            ip = td[1].text
            port = td[2].text
            country = td[3].text.replace('\xa0', '')
            anonym = td[4].text.replace('\r\n        ', '')
            types = td[5].text.replace('\r\n\t\t\t\t\t', '').replace('\r\n        ', '')
            time = td[6].text

            data = (ip, port, country, anonym, types, time)
            print(", ".join([str(s) for s in data]))
            
            ### Check port proxy
            s = socket.socket()
            s.settimeout(4)          ### How long wait connection (sec)
            print('try proxy\033[93m',ip+':'+port,'\033[00m')
            try:
                s.connect((ip,int(port)))
            except socket.error:
                s.close()
                print('port closed! proxy \033[31m'+ip+':'+port,'!UNAVAILABLE!\033[00m')
            else:
                s.close()
                with open ('proxy_list_checked.txt','a') as fa:
                    print('proxy:\033[32m',ip+':'+port,'AVAILABLE\033[00m and written to file')
                    fa.write(ip+':'+port+'\n')


def main():
    
    try:
        ### Parser logics
        url = 'http://foxtools.ru/Proxy'
        get_page_data(get_html(url))
        r = requests.get(url)
 
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

if __name__ == '__main__':
    main()


