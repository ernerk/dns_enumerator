# DNS Enumeration Tool

A powerful DNS enumeration tool for gathering and analyzing detailed DNS information about domains.

## Features

- Comprehensive DNS record scanning (A, AAAA, MX, NS, TXT, SOA, CNAME)
- WHOIS information gathering
- Common subdomain detection
- Colored terminal output
- JSON report generation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ernerk/dns-enumerator.git
cd dns-enumerator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python dns_enumerator.py example.com
```

## Sample Output

When run, the program:
- Scans DNS records
- Gathers WHOIS information
- Checks for common subdomains
- Saves results to a JSON file

Example output:
```
=== Starting DNS Enumeration: example.com ===

[*] Scanning DNS records...
[+] Found A records:
    93.184.216.34
[+] Found MX records:
    10 mail.example.com

[*] Gathering WHOIS information...
[+] WHOIS information retrieved successfully

[*] Checking common subdomains...
[+] Found subdomain: www.example.com (93.184.216.34)
[+] Found subdomain: mail.example.com (93.184.216.34)

[+] Results saved to: dns_scan_example.com_20250108_235500.json

=== Scan Complete ===
```

## Features in Detail

### DNS Record Scanning
- A and AAAA records (IPv4 and IPv6)
- MX records (Mail servers)
- NS records (Name servers)
- TXT records
- SOA records (Start of Authority)
- CNAME records (Canonical names)

### WHOIS Information
- Domain registration details
- Creation date
- Expiration date
- Name servers
- Contact information

### Subdomain Discovery
- Checks common subdomain patterns
- Lists active subdomains with IP addresses
- Identifies potential hidden services

### Reporting
- Real-time colored terminal output
- Detailed JSON report generation
- Easy-to-parse output format

## Requirements

- Python 3.6 or higher
- dnspython
- python-whois
- colorama

## Security Note

This tool should only be used on systems you have permission to scan. Unauthorized use may result in legal consequences.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 