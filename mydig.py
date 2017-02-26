#! /usr/bin/python
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.query
import sys
from datetime import datetime

# https://github.com/rthalley/dnspython/blob/master/tests/test_dnssec.py
# https://www.internic.net/domain/root.zone
# https://tools.ietf.org/html/rfc4509
# https://www.iana.org/domains/root/servers


# list of root servers. resolver will always start from root


root_servers = ['198.41.0.4', '192.228.79.201', '192.33.4.12',
                '199.7.91.13', '192.203.230.10', '192.5.5.241',
                '192.112.36.4', '198.97.190.53', '192.36.148.17',
                '192.58.128.30', '193.0.14.129', '199.7.83.42',
                '202.12.27.33']

# this is public google dns. this dns is used to get only public dns key
# for dnssec verification. we can try to get this from parent server but
# using this public dns makes code more easy and there is no harm in getting
# public key from non authoritative server
google_dns = '8.8.8.8'

# root key signing key
# https://www.internic.net/domain/root.zone
ROOT_KSK = dns.rrset.from_text('.', '172800',
                               'IN', 'DNSKEY', '257 3 8 AwEAAagAIKlVZrpC6Ia7gEzahOR+9W29euxhJhVVLOyQbSEW'
                                               '0O8gcCjFFVQUTf6v58fLjwBd0YI0EzrAcQqBGCzh/RStIoO8g0NfnfL2MTJRkxoXbfDaUeVPQ'
                                               'uYEhg37NZWAJQ9VnMVDxP/VHL496M/QZxkjf5/Efucp2gaDX6RS6CXpoY68LsvPVjR0ZSwzz1'
                                               'apAzvN9dlzEheX7ICJBBtuA6G3LQpzW5hOA2hzCTMjJPJ8LbqF6dsV6DoBQzgul0sGIcGOYl7'
                                               'OyQdXfZ57relSQageu+ipAdTTJ25AsRTAoub8ONGcLmqrAmRLKBP1dfwhYB4N7knNnulqQxA+Uk1ihz0=')

# status value from the server when query being asked is failed
SERVFAIL = 2


# extract the signature and rrset from the response
def extract_rrset_and_rrsig(answer):
    rrsig = None
    rrset = None

    for x in answer:
        if x.rdtype is dns.rdatatype.RRSIG:
            rrsig = x
        elif x.rdtype is dns.rdatatype.DNSKEY:
            rrset = x
        elif x.rdtype is dns.rdatatype.DS:
            rrset = x

    return rrset, rrsig


# this routine validates the signature with corresponding given public key
# and returns the validated rrset(subdomain, key, signature)
def get_valid_rrset(server, subqname, subqtype, keys):
    try:
        # if want_dnssec==True then it returns dnssec records as well
        subquery = dns.message.make_query(subqname, subqtype, want_dnssec=True)
        reply = dns.query.udp(subquery, server, 5)
        # in some cases response packets might be big enough to handle by UDP
        # so try once with TCP as well.
        if reply.flags & dns.flags.TC:
            reply = dns.query.tcp(subquery, server, 5)
        # if reply from server is SERVFAIL then mark failed verification
        if reply.rcode() is SERVFAIL:
            return -1

        answer = reply.answer
        if not answer:
            return None

        rrset, rrsig = extract_rrset_and_rrsig(answer)

        if rrset is None or rrsig is None:
            return None

        if keys is None:
            keys = {subqname: rrset}
        # validate the signature here
        dns.dnssec.validate(rrset, rrsig, keys)
        return rrset
    except Exception, err:
        print Exception, err
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err), err)
        return None


# this routine does two tasks:
# 1) get the valid rrset from the current server
# 2) verify the current server's DS signature with the
#    the parent servers's public DNSKEY. Chain validation basically
def validate_reply(subname, server, keys):
    subqname = dns.name.from_text(subname)
    query = dns.message.make_query(subqname, dns.rdatatype.A)
    try:
        reply = dns.query.udp(query, server, 5)
        # in some cases response packets might be big enough to handle by UDP
        # so try once with TCP as well.
        if reply.flags & dns.flags.TC:
            reply = dns.query.tcp(query, server, 5)

        if len(reply.authority) > 0:
            rrset = reply.authority[0]
        else:
            rrset = reply.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            return None

        # signed DS of sub domain from  delegated server
        signed_ds = get_valid_rrset(server, subqname, dns.rdatatype.DS, keys)
        # get the DNS_KEY from public server google. no harm in getting
        # public DNS_KEY from out of the chain.
        dnskey_rrset = get_valid_rrset(google_dns, subqname, dns.rdatatype.DNSKEY, None)

        if dnskey_rrset is -1 or signed_ds is -1:
            # SERVFAIL case
            return -1

        if not dnskey_rrset and not signed_ds:
            return None

        # now verify Delegated Sign of child server coming from
        # parent server
        for dnskey in dnskey_rrset:
            for current_ds in signed_ds:
                # we need to check only two type of algorithm here
                # https://tools.ietf.org/html/rfc4509#section-6.2
                if current_ds.digest_type == 2:
                    hashing_algorithm = 'SHA256'
                else:
                    hashing_algorithm = 'SHA1'

                # generate the ds signature and compare it from given signature
                valid_ds = dns.dnssec.make_ds(subqname, dnskey, hashing_algorithm)
                if valid_ds == current_ds:
                    break
            else:
                continue
            break
        else:
            # raise Exception("DNSSEC verification failed")
            return -1
        # set the keys for next iteration
        next_keys = {subqname: dnskey_rrset}
        return next_keys
    except Exception, err:
        print Exception, err
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err), err)
        return None


# returns time delta in milliseconds
def msecs(end, start):
    dt = end - start
    msec = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return msec


# This tries to resolve the ip address of the nameservers
# itself. Used by main routine resolve_dns
def resolve_auth_dns(rr):
    try:
        response = resolve_dns(str(rr.target), 'A', print_answer=False)
    except Exception, err:
        print Exception, err
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err), err)

    ip_addr = []
    for record in response.answer:
        for ip in record:
            ip_addr.append(ip.address)
    return ip_addr


# entry point for dns resolution. supports both dnssec enabled and disabled
def resolve_dns(name, query_type, try_tcp=False, print_answer=True,
                dont_print_answer=False, dnssec_enabled=False):
    qname = dns.name.from_text(name)
    got_answer = False
    dnssec_not_supported = False
    dnssec_failed = False

    if qname.is_absolute():
        pass
    elif len(qname) > 1:
        qname.concatenate(dns.name.root)
    else:
        print "Wrong Query"
        return

    nameservers = root_servers[:]

    if query_type == 'A':
        qtype = dns.rdatatype.A
    elif query_type == 'NS':
        qtype = dns.rdatatype.NS
    elif query_type == 'MX':
        qtype = dns.rdatatype.MX
    else:
        print "Not supported query type"
        return

    if dnssec_enabled:
        try:
            # verify root key and generate public key for child server
            root_rrset = get_valid_rrset(google_dns, '', dns.rdatatype.DNSKEY, {dns.name.root: ROOT_KSK})
            pubkeys = {dns.name.root: root_rrset}
        except Exception, err:
            print Exception, err
            exit(err)

    length = len(qname.labels)
    for i in range(length):
        subname = '.'.join(qname[length - i - 2:-1])
        rqst = dns.message.make_query(qname, qtype)

        # handling of some corner/invalid domain cases
        if nameservers:
            reply = None
        else:
            print reply
            return
        # try until get some answer
        while reply is None:
            for server in nameservers:
                try:
                    if try_tcp:
                        reply = dns.query.tcp(rqst, server, 5)
                    else:
                        reply = dns.query.udp(rqst, server, 5)
                        # in some cases response packets might be big enough to handle by UDP
                        # so try once with TCP as well.
                        if reply.flags & dns.flags.TC:
                            reply = dns.query.tcp(rqst, server, 5)
                    if reply is None:
                        continue

                    if dnssec_enabled and pubkeys and subname:
                        pubkeys = validate_reply(subname, server, pubkeys)
                        if not pubkeys:
                            dnssec_not_supported = True
                        if pubkeys is -1:
                            dnssec_failed = True

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
                                if rr.rdtype is 2:
                                    ip_list = resolve_auth_dns(rr)
                                    for x in ip_list:
                                        nameservers.append(x)
                    else:
                        raise Exception
                    break
                except Exception, err:
                    print Exception, err
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err), err)
                    # try next server
                    continue
        # breaks for loop
        if got_answer:
            break
    if dnssec_failed is True:
        print "DNSSEC verification failed."
        exit(-1)
    if print_answer:
        if reply.answer:
            if not dont_print_answer:
                print ";; ANSWER:"
            for x in reply.answer:
                print x
                if x.rdtype is not 1 and query_type == 'A':
                    for cname in x:
                        resolve_dns(str(cname), query_type, dont_print_answer=True)
        elif reply.authority:
            print ";; AUTHORITY:"
            for x in reply.authority:
                print x
        elif reply.additional:
            print ";; ADDITIONAL:"
            for x in reply.additional:
                print x
        else:
            raise Exception
        if dnssec_enabled:
            if dnssec_not_supported and not dont_print_answer:
                print "DNSSEC not supported."
            if not dnssec_not_supported and not dont_print_answer:
                print "DNSSEC is configured and verification passed."
    else:
        return reply


# Wrapper of entry function resolve_dns
def get_dig_output(name, query_type, dnssec_enabled):
    start_time = datetime.now()
    resolve_dns(name, query_type, False, True, False, dnssec_enabled)
    end_time = datetime.now()
    print "Query time:", str(msecs(end_time, start_time)) + " ms"


# Test code. ignore it
# get_dig_output('paypal.com', 'NS', True)
# get_dig_output('example.com', 'A', True)
# get_dig_output('google.co.jp', 'A', True)
# get_dig_output('google.co.jp', 'A', False)
#
# get_dig_output('facebook.com', 'A', True)
# get_dig_output('facebook.com', 'A', False)
# # get_dig_output('example.com', 'A', True)
# # get_dig_output('example.com', 'A', True)
# # get_dig_output('example.com', 'NS', True)
#
# get_dig_output('dnssec-failed.org', 'A', True)


def main():
    args = sys.argv[1:]

    if not args or len(args) < 3:
        print "Usage: python my_dig.py <name> <type> <dnssec_enabled>"
        print "name: domain name"
        print "type: A / NS / MX"
        print "dnssec_enabled: T(t)rue / F(f)alse"
        exit()

    name = args[0]
    query_type = args[1]
    if args[2] == 'True' or args[2] == 'true':
        dnssec_enabled = True
    else:
        dnssec_enabled = False

    get_dig_output(name, query_type, dnssec_enabled)

main()
