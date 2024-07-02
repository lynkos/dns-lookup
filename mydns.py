from sys import argv, exit

if __name__ == "__main__":
    # get filename from command line
    if len(argv) != 3:
        print("Usage: python mydns.py domain-name root-dns-ip")
        exit(1)

    # domain name to be resolved and root DNS server's IPv4 address
    # list of current root DNS servers: https://www.iana.org/domains/root/servers
    domain_name, root_dns_ip = argv[1], argv[2]
    domain_name, root_dns_ip = "cs.fiu.edu", "202.12.27.33"

    # format and print root DNS server's IP address
    print("----------------------------------------------------------------")
    print(f"DNS server to query: {root_dns_ip}")

    exit(0)