from dataclasses import dataclass
from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM
from dataclasses import dataclass, astuple
from struct import pack, unpack
from random import randint, seed
from io import BytesIO
from typing import List

A: int = 1
NS: int = 2
TIMEOUT: int = 5
BUFFER: int = 1024

@dataclass
class Header:
    id: int
    flags: int
    num_queries: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

@dataclass
class Query:
    name: bytes
    typ: int 
    cls: int

@dataclass
class Reply:
    name: bytes
    typ: int
    cls: int
    ttl: int
    data: bytes | str

@dataclass
class Packet:
    header: Header
    questions: List[Query]
    answers: List[Reply]
    authorities: List[Reply]
    additionals: List[Reply]

def dns_query(domain_name, record_type):
    encoded_name = b""
    for part in domain_name.encode("ascii").split(b"."):
        encoded_name += bytes([len(part)]) + part
    encoded_name += b"\x00"
    seed(1)
    header = Header(id = randint(0, 65535), num_queries = 1, flags = 1 << 8)
    header_to_bytes =  pack("!HHHHHH", *astuple(header))
    question_to_bytes = encoded_name + pack("!HH", record_type, 1)
    return header_to_bytes + question_to_bytes

def decode_name(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else: parts.append(reader.read(length))
    return b".".join(parts)

def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result

def parse_reply(reader):
    name = decode_name(reader)
    data = reader.read(10)
    typ, cls, ttl, data_len = unpack("!HHIH", data)
    if typ == NS: data = decode_name(reader)
    elif typ == A: data = ".".join([ str(x) for x in reader.read(data_len) ])
    else: data = reader.read(data_len)
    return Reply(name, typ, cls, ttl, data)

def parse_query(reader):
    name = decode_name(reader)
    data = reader.read(4)
    typ, cls = unpack("!HH", data)
    return Query(name, typ, cls)

def parse_packet(data):
    reader = BytesIO(data)
    header = Header(*unpack("!HHHHHH", reader.read(12)))
    queries = [ parse_query(reader) for _ in range(header.num_queries) ]
    answers = [ parse_reply(reader) for _ in range(header.num_answers) ]
    authorities = [ parse_reply(reader) for _ in range(header.num_authorities) ]
    additionals = [ parse_reply(reader) for _ in range(header.num_additionals) ]
    return Packet(header, queries, answers, authorities, additionals)

def send_query(ip_address, domain_name, record_type):
    query = dns_query(domain_name, record_type)
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.sendto(query, (ip_address, 53))
        data, _ = sock.recvfrom(BUFFER) 
    return parse_packet(data)

def get_answer(packet):
    for x in packet.answers:
        if x.typ == A: return x.data
        
def get_ns_ip(packet):
    for x in packet.additionals:
        if x.typ == A: return x.data

def get_ns(packet):
    for x in packet.authorities:
        if x.typ == NS: return x.data.decode("utf-8")

def display_reply(packet):
    print("Reply received. Content overview:")

    num_answers = len(packet.answers)
    num_authorities = len(packet.authorities)
    num_additionals = len(packet.additionals)
        
    print(f"\t{num_answers} Answers.")
    print(f"\t{num_authorities} Intermediate Name Servers.")
    print(f"\t{num_additionals} Additional Information Records.")

    if num_answers > 0:
        print("\nAnswers Section:")
        for answer in packet.answers:
            if answer.typ == A:
                print(f"\tName: {answer.name.decode()}\tIP: {answer.data}")
            else: print(f"\tName: {answer.name.decode()}")

    if num_authorities > 0:
        print("\nAuthority Section:")
        for authority in packet.authorities:
            if authority.typ == NS:
                print(f"\tName: {authority.name.decode()}\tName Server: {authority.data.decode()}")
            else: print(f"\tName: {authority.name.decode()}")

    if num_additionals > 0:
        print("\nAdditional Information Section:")
        for additional in packet.additionals:
            if additional.typ == A:
                print(f"\tName: {additional.name.decode()}\tIP: {additional.data}")
            else: print(f"\tName: {additional.name.decode()}")

def dns_lookup(domain_name, dns_ip, record_type):
    ns = dns_ip
    while True:
        print("\n----------------------------------------------------------------\n")
        print(f"DNS server to query: {ns}\n")
        reply = send_query(ns, domain_name, record_type)

        if reply:
            display_reply(reply)
            if ip := get_answer(reply): return ip
            elif ns_ip := get_ns_ip(reply): ns = ns_ip
            elif ns_domain := get_ns(reply): ns = dns_lookup(ns_domain, ns, A)
            else:
                print("Error")
                exit(1)

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python mydns.py domain-name root-dns-ip")
        exit(1)

    # domain name to be resolved and root DNS server's IPv4 address
    # list of current root DNS servers: https://www.iana.org/domains/root/servers
    domain_name, root_dns_ip = argv[1], argv[2]

    for values in root_dns_ip:
        if not values.isdigit() and values != ".":
            print("Invalid IP address")
            exit(1)
    
    dns_lookup(domain_name, root_dns_ip, A)
    exit(0)
