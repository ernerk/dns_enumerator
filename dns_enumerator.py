import dns.resolver
import whois
import socket
import argparse
import json
from datetime import datetime
from colorama import init, Fore, Style
import concurrent.futures
import ipaddress

init()  # Colorama'yı başlat

class DNSEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.results = {
            "domain": domain,
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "records": {},
            "whois": {},
            "subdomains": [],
            "reverse_dns": [],
            "common_ports": {}
        }

    def get_dns_records(self, record_type):
        """Belirtilen türdeki DNS kayıtlarını al"""
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(self.domain, record_type)
            return [str(answer) for answer in answers]
        except Exception as e:
            return [f"Hata: {str(e)}"]

    def get_all_records(self):
        """Tüm DNS kayıt türlerini tara"""
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        print(f"\n{Fore.CYAN}[*] DNS kayıtları taranıyor...{Style.RESET_ALL}")
        for record_type in record_types:
            records = self.get_dns_records(record_type)
            if records:
                self.results["records"][record_type] = records
                print(f"{Fore.GREEN}[+] {record_type} kayıtları bulundu:{Style.RESET_ALL}")
                for record in records:
                    print(f"    {record}")

    def get_whois_info(self):
        """WHOIS bilgilerini al"""
        try:
            print(f"\n{Fore.CYAN}[*] WHOIS bilgileri alınıyor...{Style.RESET_ALL}")
            w = whois.whois(self.domain)
            self.results["whois"] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails
            }
            print(f"{Fore.GREEN}[+] WHOIS bilgileri başarıyla alındı{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] WHOIS bilgileri alınamadı: {str(e)}{Style.RESET_ALL}")

    def check_common_subdomains(self):
        """Yaygın subdomain'leri kontrol et"""
        common_subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 
                           'test', 'staging', 'api', 'shop', 'store', 'app',
                           'portal', 'secure', 'vpn', 'remote', 'git', 'gitlab',
                           'jenkins', 'jira', 'docs', 'wiki', 'support']
        
        print(f"\n{Fore.CYAN}[*] Yaygın subdomain'ler kontrol ediliyor...{Style.RESET_ALL}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for sub in common_subdomains:
                subdomain = f"{sub}.{self.domain}"
                futures.append(executor.submit(self.check_subdomain, subdomain))
            
            concurrent.futures.wait(futures)

    def check_subdomain(self, subdomain):
        """Tek bir subdomain'i kontrol et"""
        try:
            ip = socket.gethostbyname(subdomain)
            self.results["subdomains"].append({
                "subdomain": subdomain,
                "ip": ip
            })
            print(f"{Fore.GREEN}[+] Bulunan subdomain: {subdomain} ({ip}){Style.RESET_ALL}")
        except:
            pass

    def perform_reverse_dns(self):
        """Reverse DNS lookup gerçekleştir"""
        print(f"\n{Fore.CYAN}[*] Reverse DNS taraması yapılıyor...{Style.RESET_ALL}")
        try:
            # A kayıtlarından IP adreslerini al
            if 'A' in self.results["records"]:
                for ip in self.results["records"]["A"]:
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                        self.results["reverse_dns"].append({
                            "ip": ip,
                            "hostname": hostname
                        })
                        print(f"{Fore.GREEN}[+] Reverse DNS: {ip} -> {hostname}{Style.RESET_ALL}")
                    except:
                        continue
        except Exception as e:
            print(f"{Fore.RED}[-] Reverse DNS taraması başarısız: {str(e)}{Style.RESET_ALL}")

    def check_common_ports(self):
        """Yaygın portları kontrol et"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080, 8443]
        print(f"\n{Fore.CYAN}[*] Yaygın portlar kontrol ediliyor...{Style.RESET_ALL}")
        
        try:
            if 'A' in self.results["records"]:
                ip = self.results["records"]["A"][0]  # İlk IP adresini kullan
                self.results["common_ports"][ip] = []
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    futures = []
                    for port in common_ports:
                        futures.append(executor.submit(self.check_port, ip, port))
                    
                    concurrent.futures.wait(futures)
        except Exception as e:
            print(f"{Fore.RED}[-] Port taraması başarısız: {str(e)}{Style.RESET_ALL}")

    def check_port(self, ip, port):
        """Tek bir portu kontrol et"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = socket.getservbyport(port)
                self.results["common_ports"][ip].append({
                    "port": port,
                    "service": service,
                    "state": "open"
                })
                print(f"{Fore.GREEN}[+] Açık port bulundu: {port} ({service}){Style.RESET_ALL}")
            sock.close()
        except:
            pass

    def save_results(self):
        """Sonuçları JSON dosyasına kaydet"""
        filename = f"dns_scan_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\n{Fore.GREEN}[+] Sonuçlar kaydedildi: {filename}{Style.RESET_ALL}")

    def run_enumeration(self):
        """Tüm tarama işlemlerini çalıştır"""
        print(f"\n{Fore.YELLOW}=== DNS Enumeration Başlatılıyor: {self.domain} ==={Style.RESET_ALL}")
        self.get_all_records()
        self.get_whois_info()
        self.check_common_subdomains()
        self.perform_reverse_dns()
        self.check_common_ports()
        self.save_results()
        print(f"\n{Fore.YELLOW}=== Tarama Tamamlandı ==={Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='DNS Enumeration Tool')
    parser.add_argument('domain', help='Taranacak domain adı')
    args = parser.parse_args()

    enumerator = DNSEnumerator(args.domain)
    enumerator.run_enumeration()

if __name__ == "__main__":
    main() 