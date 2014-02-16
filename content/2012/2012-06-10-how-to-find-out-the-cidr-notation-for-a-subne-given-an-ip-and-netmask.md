Title: How to Find Out the CIDR Notation for a Subnet, Given an IP and Netmask
Date: 2012-06-10 22:50
Category: Blog
Tags: networking, programming, python
Slug: 2012/06/10/how-to-find-out-the-cidr-notation-for-a-subnet-given-an-ip-and-netmask
Author: Erik Johnson
Summary: I like to listen to streaming radio while I work. However, sometimes having a web browser open is too much of a temptation to just start browsing and ignore the work that needs to be done...

In the process of working on some contributions to
[Salt](http://github.com/saltstack/salt) (a fantastic new infrastructure
automation system), I needed to figure out how to find the [CIDR
notation](http://en.wikipedia.org/wiki/CIDR_notation) for a subnet, given only
an IP address and netmask. There is a Python module called
[netaddr](http://pypi.python.org/pypi/netaddr/) which is capable of performing
this calculation, but it is not a core Python module and using it would have
required this module to be added to Salt's dependency list. So, I needed to
find a good way of calculating this information without the aid of a Python
module. To my surprise, documentation on how to do this doesn't appear to be
that common on the web, so I thought I'd share it.

But first, a little bit of explanation for those that may need it. An IPv4
address contains 4 octets, each ranging from 0 to 255 (for example,
**56.78.123.45**). However, this notation is really just shorthand, designed be
easier for humans to read. An IP address is really just a a 32-bit number, with
bits 1-8 making up the first octet, 9-16 making up the second, etc. In binary,
**255** is **11111111**, while **0** is **00000000**. The network mask
(sometimes also referred to as a "netmask") uses the same notation as an IP
address. When converted from that notation to binary, the number of zeros at
the end will let you know the size of the network. A network mask (in binary)
will be several 1s followed by (in most cases) several 0s. In the case of
255.255.255.0, there are 24 1s followed by 8 0s:

    :::
    Normal: 255      255      255      0
    Binary: 11111111 11111111 11111111 00000000

CIDR notation for a network would be the starting IP of the network followed by
**/NN**, where **NN** is equal to **32 - the number of zeros**. Since there are
8 zeros at the end, a netmask of **255.255.255.0** would be a **/24** network.
These are quite common. For the IP address **56.78.123.45**, the CIDR notation
for the network would be **56.78.123.0/24**. /24 networks are easy because they
always start at zero, but what if the netmask was **255.255.252.0**? How would
you find the start of *that* network?

The answer lies in [bitwise
operations](http://en.wikipedia.org/wiki/Bitwise_operation), specifically the
[bitwise AND](http://en.wikipedia.org/wiki/Bitwise_operation#AND). A bitwise
AND will take two binary numbers and compare the first bit of both numbers to
each other, then the second bit of each number, etc., and will yield a 1 when
both are 1, and 0 if either (or both) are *not* 1. Remember that a netmask will
always be 1s up to a certain point. That point represents the start of the
network. So executing a bitwise AND on the IP and netmask will give you 1s
where there were 1s in the IP address, but only up to the point where the
network began. The rest of the bits in the result will all be zeros.

    :::
    56.78.123.45  = 00111000 01001110 01111011 00101101
    255.255.252.0 = 11111111 11111111 11111100 00000000
    ---------------------------------------------------
                    00111000 01001110 01111000 00000000 = 56.78.120.0

As you can see, the result is **56.78.120.0**. Because there are 10 zeros at
the end of the netmask, this is a **/22** (32 - 10) network, making the CIDR
notation for this network **56.78.120.0/22**.

Of course, it's not too fun to do these conversions every time you want to get
this information. There is a command-line tool called
[ipcalc](http://jodies.de/ipcalc) which does this for you quite easily (The
link was for a web version, but you can get a command-line version of the same
tool in most Linux distributions).

    :::bash
    $ ipcalc -b 56.78.123.45/255.255.252.0 | grep Network
    Network:   56.78.120.0/22

Let's make a programming exercise out of this, though. In Python, the bitwise
AND operator is a single ampersand.

    :::python
    >>> 56 & 255
    56
    >>> 123 & 252
    120

So, the below Python code will give you the CIDR notation:

    :::python
    #!/usr/bin/python2

    import sys
    from socket import inet_aton

    USAGE = 'usage: {0} ipaddr netmask\n'.format(sys.argv[0])

    def get_net_size(netmask):
        binary_str = ''
        for octet in netmask:
            binary_str += bin(int(octet))[2:].zfill(8)
        return str(len(binary_str.rstrip('0')))

    if len(sys.argv) != 3:
        sys.stderr.write(USAGE)
        sys.exit(1)

    # validate input
    try:
        inet_aton(sys.argv[1])
        inet_aton(sys.argv[2])
    except:
        sys.stderr.write('IP address or netmask invalid\n')
        sys.stderr.write(USAGE)
        sys.exit(2)

    ipaddr = sys.argv[1].split('.')
    netmask = sys.argv[2].split('.')

    # calculate network start
    net_start = [str(int(ipaddr[x]) &amp; int(netmask[x]))
                 for x in range(0,4)]

    # print CIDR notation
    print '.'.join(net_start) + '/' + get_net_size(netmask)

And here's the output:

    :::bash
    $ python2 cidr_notation.py 12.34.56.78 255.255.255.248
    12.34.56.72/29

This is a /29 network, which has 2<sup>(32-29)</sup>, or 2<sup>3</sup>, or 8 IP
addresses, so it would span the IP addresses 12.34.56.72 to 12.34.56.79.

Hopefully you grok CIDR a little more now than you did a few minutes ago. :)
