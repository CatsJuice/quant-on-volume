
import pcap
import dpkt
 
import getopt
import sys
import datetime
import time
import os
import platform
 
if 'Windows' in platform.platform():
    import winreg as wr
 
 
IF_REG = r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
def getInterfaceByName(name):
    '''Get guid of interface from regedit of windows system
    Args:
        name: interface name
    Returns:
        An valid guid value or None.
    Example:
        getInterfaceByName('eth0')
    '''
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, IF_REG)
    for i in range(wr.QueryInfoKey(reg_key)[0]):
        subkey_name = wr.EnumKey(reg_key, i)
        try:
            reg_subkey = wr.OpenKey(reg_key, subkey_name + r'\Connection')
            Name = wr.QueryValueEx(reg_subkey, 'Name')[0]
            wr.CloseKey(reg_subkey)
            if Name == name:
                return r'\Device\NPF_' + subkey_name
        except FileNotFoundError as e:
            pass
 
    return None
 
def mac_addr(mac):
    return '%02x:%02x:%02x:%02x:%02x:%02x'%tuple(mac)
 
def ip_addr(ip):
    return '%d.%d.%d.%d'%tuple(ip)
 
def captureData(iface):
    pkt = pcap.pcap(iface, promisc=True, immediate=True, timeout_ms=50)
    # filter method
    filters = {
        'DNS': 'udp port 53',
        'HTTP': 'tcp port 80'
    }
    # pkt.setfilter(filters['HTTP'])
 
    pcap_filepath = 'pkts/pkts_{}.pcap'.format(time.strftime("%Y%m%d-%H%M%S",
        time.localtime()))
    pcap_file = open(pcap_filepath, 'wb')
    writer = dpkt.pcap.Writer(pcap_file)
    print('Start capture...')
    try:
        pkts_count = 0
        for ptime, pdata in pkt:
            writer.writepkt(pdata, ptime)
            # anlysisData(pdata)
            printRawPkt(ptime, pdata)
            pkts_count += 1
    except KeyboardInterrupt as e:
        writer.close()
        pcap_file.close()
        if not pkts_count:
            os.remove(pcap_filepath)
        print('%d packets received'%(pkts_count))
 
def printRawPkt(time, data):
    eth = dpkt.ethernet.Ethernet(data)
    print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(time)))
    print('Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst))
    if not isinstance(eth.data, dpkt.ip.IP):
        print('')
        return
 
    ip = eth.data
 
    # get fragments info
    do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
    more_fragments = bool(ip.off & dpkt.ip.IP_MF)
    fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
 
    print('IP: %s -> %s (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % (
        ip_addr(ip.src), ip_addr(ip.dst), ip.len, ip.ttl,
        do_not_fragment, more_fragments, fragment_offset))
 
def anlysisData(data):
    packet = dpkt.ethernet.Ethernet(data)
    if isinstance(packet.data, dpkt.ip.IP):
        ip = ip_addr(packet.data.dst)
        if packet.data.data.dport == 80 or packet.data.data.sport == 80:
            try:
                print(packet.data.data.data.decode('utf-8', errors='ignore'))
            except UnicodeDecodeError as uderr:
                print(uderr.__str__())
 
 
def main():
    if 'Windows' in platform.platform():
        iface = getInterfaceByName('Router')
    else:
        iface = 'enp2s0'
    captureData(iface)
 
if __name__ == "__main__":
    main()
