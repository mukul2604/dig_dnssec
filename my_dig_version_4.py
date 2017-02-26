#! /usr/bin/python
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
from datetime import datetime
from datetime import timedelta

root_servers = ['198.41.0.4', '192.228.79.201', '192.33.4.12',
                '199.7.91.13', '192.203.230.10', '192.5.5.241',
                '192.112.36.4', '198.97.190.53', '192.36.148.17',
                '192.58.128.30', '193.0.14.129', '199.7.83.42',
                '202.12.27.33']

def msecs(end, start):
    """
    :param start: datetime.now()
    :param end: datetime.now()
    :return: msec
    """
    dt = end - start
    msec = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return msec





def resolve_auth_dns(rr):
    try:
        response = resolve_dns(str(rr.target), 'A', print_answer=False)
    except Exception, err:
        print Exception, err

    ip_addr = []
    for record in response.answer:
        for ip in record:
            ip_addr.append(ip.address)
    return ip_addr


def resolve_dns(name, query_type, try_tcp=False, print_answer=True, dont_print_answer=False):
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

    if query_type is 'A':
        qtype = dns.rdatatype.A
    elif query_type is 'NS':
        qtype = dns.rdatatype.NS
    elif query_type is 'MX':
        qtype = dns.rdatatype.MX
    else:
        print "Not supported query type"
        return

    reply = None
    for i in range(0, len(qname.labels)):
        rqst = dns.message.make_query(qname, qtype)
        if nameservers:
            reply = None
        else:
            print reply
            return

        while reply is None:
            for server in nameservers:
                try:
                    if try_tcp:
                        reply = dns.query.tcp(rqst, server, 5)
                    else:
                        reply = dns.query.udp(rqst, server, 5)
                        if reply.flags & dns.flags.TC:
                            reply = dns.query.tcp(rqst, server, 5)
                    if reply is None:
                        continue

                    # reset the name server list
                    nameservers[:] = []
                    if reply.answer:
                        got_answer = True
                    elif reply.additional:
                        for records in reply.additional:
                            for rr in records:
                                if rr.rdtype is 1:  # IPv4
                                    nameservers.append(rr.address)
                    elif reply.authority:
                        for records in reply.authority:
                            for rr in records:
                                # print rr.rdtype
                                # if rr.rdtype is not 2:
                                #     raise Exception
                                if rr.rdtype is 2:
                                    ip_list = resolve_auth_dns(rr)
                                    for x in ip_list:
                                        nameservers.append(x)
                                if rr.rdtype is 6:
                                    pass
                    else:
                        raise Exception
                    break
                except Exception, err:
                    print Exception, err
                    # try next server
                    continue

        if got_answer:
            break
    if print_answer:
        if reply.answer:
            if not dont_print_answer:
                print ";; ANSWER:"
            for x in reply.answer:
                print x
                if x.rdtype is not 1 and query_type is 'A':
                    for cname in x:
                        resolve_dns(str(cname), query_type, dont_print_answer=True)
                        # print ""
        elif reply.authority:
            print ";; AUTHORITY:"
            for x in reply.authority:
                print x
    else:
        return reply


def get_dig_output(name, query_type):
    start_time = datetime.now()
    resolve_dns(name, query_type)
    end_time = datetime.now()
    print ";; Query time:"
    print str(msecs(end_time, start_time)) + " ms"

#
# get_dig_output('facebook.com', 'A')
# get_dig_output('apple.com', 'NS')
# get_dig_output('apple.com', 'A')
# get_dig_output('google.com', 'A')
# get_dig_output('cs.stonybrook.edu', 'A')
get_dig_output('upenn.edu', 'MX')
get_dig_output('www.cs.stonybrook.edu', 'A')
# get_dig_output('google.co.jp', 'A')
# get_dig_output('iana.org', 'A')
# get_dig_output('abc.go.com', 'A')
# get_dig_output('tutorialspoint.com', 'A')
# get_dig_output('bloomberg.com', 'A')
# get_dig_output('baidu.com', 'A')
# get_dig_output('yahoo.com', 'A')
# get_dig_output('wikipedia.org','NS')
# get_dig_output('qq.com','A')
# get_dig_output('tmall.com','A')
# get_dig_output('sohu.com', 'MX')
# get_dig_output('sina.com.cn', 'A')
# get_dig_output('t.co', 'A')
# get_dig_output('yandex.ru', 'NS')
# get_dig_output('www.amazon.com','A')
# get_dig_output('www.alexa.com','A')
# get_dig_output('www.alibaba.com','A')
# get_dig_output('www.alibaba.com','MX')
# get_dig_output('www.alibaba.com', 'NS')
# get_dig_output('www.yahoo.com','A')
# get_dig_output('www.dnssec-failed.org', 'A')


# resolve_dns('www.yahoo.com','MX')
# resolve_dns('abc.xvt', 'A')
def main():
    args = sys.argv[1:]
    if not args or len(args) < 2:
        print "Usage: <name> <type>"
        exit()

    name = args[0]
    query_type = args[1]

    get_dig_output(name, query_type)


#main()
# if __name__ is '__main__':
#     main()
