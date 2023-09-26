import requests
import dns.resolver
import socket
import re
from bs4 import BeautifulSoup
from datetime import date


class SubdomainSearch:

    def find_ip_addresses(subdomain):

        ip_addresses = []

        try:
            addrinfo = socket.getaddrinfo(subdomain, None)
            
            for item in addrinfo:
                ip_address = item[4][0]
                ip_addresses.append(ip_address)
        except socket.gaierror:
            pass

        return ip_addresses
    
    def search_subdomains(vt_key, domain, db):
        subdomains_list = SubdomainSearch.search_subs(vt_key, domain)
        
        processed_subdomains = set()
        for subdomain_info in subdomains_list:
            subdomain_name = subdomain_info[0]
            subdomain_source = subdomain_info[1]
            if (subdomain_name, subdomain_source) in processed_subdomains:
                continue
            db.add_subdomain(subdomain_name, '', subdomain_source, date.today())
            processed_subdomains.add((subdomain_name, subdomain_source, date.today()))
        
        return(db)