import ipaddress
import socket
import psutil
import nmap, os


from rich.console import Console
from rich.table import Table

console = Console()

# عدل المسار إذا كان Nmap مثبتاً في مكان آخر
NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"

COMMON_PORTS = (
    "21,22,23,25,53,80,110,"
    "135,139,143,443,445,"
    "3306,3389,5900,8080"
)

RISK_PORTS = {
    # Remote Access
    22: 5,      # SSH
    23: 30,     # Telnet
    3389: 25,   # RDP
    5900: 20,   # VNC
    5901: 20,
    5902: 20,

    # File Sharing
    20: 15,     # FTP Data
    21: 20,     # FTP
    69: 20,     # TFTP
    139: 20,    # NetBIOS
    445: 30,    # SMB
    2049: 15,   # NFS

    # Email
    25: 10,     # SMTP
    110: 10,    # POP3
    143: 10,    # IMAP
    465: 5,
    587: 5,
    993: 5,
    995: 5,

    # Web
    80: 5,
    443: 2,
    8080: 5,
    8081: 5,
    8443: 5,

    # DNS
    53: 5,

    # Databases
    1433: 25,   # MSSQL
    1434: 25,
    1521: 20,   # Oracle
    3306: 20,   # MySQL
    33060: 20,
    5432: 15,   # PostgreSQL
    6379: 30,   # Redis
    27017: 30,  # MongoDB
    27018: 30,
    27019: 30,

    # Directory Services
    389: 10,    # LDAP
    636: 5,
    3268: 10,
    3269: 10,

    # SNMP
    161: 15,
    162: 15,

    # RPC / Windows
    135: 20,
    137: 20,
    138: 20,
    593: 15,

    # Industrial / IoT
    502: 20,    # Modbus
    102: 20,    # Siemens S7
    20000: 20,  # DNP3
    47808: 20,  # BACnet

    # Containers & Virtualization
    2375: 30,   # Docker
    2376: 20,
    6443: 20,   # Kubernetes API
    10250: 20,

    # Message Queues
    5672: 15,   # RabbitMQ
    61616: 15,  # ActiveMQ

    # Monitoring
    9090: 10,   # Prometheus
    9100: 10,

    # Proxy
    3128: 15,
    1080: 15,

    # Misc
    111: 10,
    123: 5,
    515: 10,
    631: 10,
    873: 15,
    1723: 15,
    5060: 15,
    5061: 15,
}


def get_interfaces():
    interfaces = []

    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if addr.address.startswith("127."):
                    continue

                interfaces.append({
                    "name": name,
                    "ip": addr.address
                })

    return interfaces


def choose_interface():
    interfaces = get_interfaces()

    table = Table(
        title="[bold yellow]NETWORK INTERFACES[/bold yellow]",
        border_style="yellow"
    )
    table.add_column("#")
    table.add_column("Interface")
    table.add_column("IPv4")

    for i, iface in enumerate(interfaces, start=1):
        table.add_row(
            str(i),
            iface["name"],
            iface["ip"]
        )

    console.print(table)

    while True:
        try:
            choice = int(input("\nSelect interface: "))
            if 1 <= choice <= len(interfaces):
                return interfaces[choice - 1]
        except:
            pass

        print("Invalid selection")


def get_network(ip):
    network = ipaddress.ip_network(
        f"{ip}/24",
        strict=False
    )

    return str(network)


def calculate_risk(open_ports):

    score = 0

    for port in open_ports:
        score += RISK_PORTS.get(port, 1)

    score = min(score, 100)

    if score < 20:
        level = "LOW"
    elif score < 50:
        level = "MEDIUM"
    elif score < 80:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return score, level


def discover_hosts(scanner, network):

    console.print(
        f"\n[yellow]Discovering hosts in {network}[/yellow]\n"
    )

    scanner.scan(
        hosts=network,
        arguments="-sn"
    )

    hosts = []

    for host in scanner.all_hosts():
        hosts.append(host)

    return hosts


def scan_host(scanner, host):

    scanner.scan(
        host,
        ports=COMMON_PORTS,
        arguments="-T4"
    )

    ports = []

    if host in scanner.all_hosts():

        if "tcp" in scanner[host]:

            for port in scanner[host]["tcp"]:

                if scanner[host]["tcp"][port]["state"] == "open":
                    ports.append(port)

    return ports


def scan():

    console.print(
        "\n[bold white]Network Inventory Scanner[/bold white]\n"
    )

    iface = choose_interface()

    network = get_network(
        iface["ip"]
    )

    console.print(
        f"\n[yellow]Interface:[/yellow] [white]{iface['name']}[/white]"
    )

    console.print(
        f"[yellow]IP:[/yellow] [white]{iface['ip']}[/white]"
    )

    console.print(
        f"[yellow]Network:[/yellow] [white]{network}[/white]"
    )

    scanner = nmap.PortScanner(
        nmap_search_path=(NMAP_PATH,)
    )

    hosts = discover_hosts(
        scanner,
        network
    )

    console.print(
        f"\n[yellow]Hosts Found:[/yellow] [white]{len(hosts)}[/white]\n"
    )

    table = Table(
        title="[bold red]SCAN RESULTS[/bold red]",
        border_style="red"
    )

    table.add_column("IP", style="white")
    table.add_column("Hostname", style="white")
    table.add_column("Open Ports", style="yellow")
    table.add_column("Risk %", style="red")
    table.add_column("Level", style="red")

    for host in hosts:

        hostname = "-"

        try:
            hostname = socket.getfqdn(host)
        except:
            pass

        open_ports = scan_host(
            scanner,
            host
        )

        risk, level = calculate_risk(
            open_ports
        )

        if risk < 20:
            level_color = "[white]LOW[/white]"
        
        elif risk < 50:
            level_color = "[yellow]MEDIUM[/yellow]"
        
        else:
            level_color = f"[red]{level}[/red]"
        table.add_row(
            host,
            hostname,
            ", ".join(
                map(str, open_ports)
            ) if open_ports else "-",
            f"{risk}%",
            level_color
        )

    console.print(table)
