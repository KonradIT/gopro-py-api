import netifaces as ni
from goprocam import GoProCamera, constants

ifaces = ni.interfaces()
for iface in ifaces:
    try:
        ip = ni.ifaddresses(iface)[ni.AF_INET][0]["addr"]
        if ip.startswith("172."):
            print(f"IP: {ip} from Interface {iface}")
    except:
        pass
