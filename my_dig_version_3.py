#! /usr/bin/python
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys

root_servers = ['198.41.0.4', '192.228.79.201', '192.33.4.12',
                '199.7.91.13', '192.203.230.10', '192.5.5.241',
                '192.112.36.4', '198.97.190.53', '192.36.148.17',
                '192.58.128.30', '193.0.14.129', '199.7.83.42',
                '202.12.27.33']

def resolve_auth_dns(rr):
    local_res = dns.resolver.get_default_resolver()
    try:
        response = local_res.query(str(rr.target),'A').response
    except Exception, err:
        print Exception, err

    ip_addr = []
    for record in response.answer:
        for ip in record:
            ip_addr.append(ip.address)
    return ip_addr



def resolve_dns(name, type, try_tcp = False):
    qname = dns.name.from_text(name)
    got_answer = False

    if qname.is_absolute():
        pass
    elif len(qname) > 1:
       qname.concatenate(dns.name.root)
    else:
        print "Failed"
        return


    nameservers = root_servers[:]

    # for root_server in root_servers:
    #     nameservers.append(root_server)

    if type == 'A':
        qtype = dns.rdatatype.A
    elif type == 'NS':
        qtype = dns.rdatatype.NS
    elif type == 'MX':
        qtype = dns.rdatatype.MX
    else:
        print "Not supported query type"
        return
    reply = None
    for i in range(0, len(qname.labels)):
        rqst = dns.message.make_query(qname, qtype, want_dnssec= True)

        if nameservers:
            reply = None
        else:
            print reply
            return

        while None == reply:
            for server in nameservers:
                try:
                    if try_tcp:
                        reply = dns.query.tcp(rqst, server, 2)
                    else:
                        reply = dns.query.udp(rqst, server, 2)
                        if reply.flags & dns.flags.TC:
                            reply = dns.query.tcp(rqst, server, 2)

                    print reply
                    if None == reply:
                        continue
                    #reset the name server list
                    nameservers[:] = []

                    if len(reply.answer):
                        got_answer = True
                    elif len(reply.additional):
                        for records in reply.additional:
                            for rr in records:
                                 if rr.rdtype == 1:  #IPv4
                                    nameservers.append(rr.address)
                    elif len(reply.authority):
                        for records in reply.authority:
                            for rr in records:
                                 # print rr.rdtype
                                 if rr.rdtype == 2:
                                    ip_list  = resolve_auth_dns(rr)
                                    for x in ip_list:
                                        nameservers.append(x)
                    else:
                        raise Exception
                    break
                except Exception, err:
                    print Exception, err
                    # try next server
                    continue

        if got_answer:
            break

    print ";; ANSWER:"
    for x in reply.answer:
        print x
    print ""
    return reply
#
#while(1):
# resolve_dns('facebook.com', 'NS')
# resolve_dns('google.com', 'A')
resolve_dns('www3.cs.stonybrook.edu','NS')
# resolve_dns('google.co.jp', 'A')
# resolve_dns('iana.org', 'A')
# resolve_dns('abc.go.com', 'NS')
# resolve_dns('www.tutorialspoint.com', 'A')
# # resolve_dns('abc.xvt','A')


def main():
    args = sys.argv[1:]
    if not args or len(args) < 2:
        print "Usage: <name> <type>"

    name = args[0]
    type = args[1]

    resolve_dns(name, type)


if __name__ == '__main__':
    #main()
    pass
