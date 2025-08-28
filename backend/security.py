"""
Security module for preventing SSRF attacks and other security checks.
"""
import ipaddress
import socket
from urllib.parse import urlparse
from typing import List, Union, Optional
from backend.validators import get_domain

class SecurityChecker:
    def __init__(self):
        # Private IPv4 ranges
        self.private_ipv4_ranges = [
            '10.0.0.0/8',        # Private network
            '172.16.0.0/12',     # Private network
            '192.168.0.0/16',    # Private network
            '127.0.0.0/8',       # Localhost
            '169.254.0.0/16',    # Link-local
        ]
        
        # Private IPv6 ranges
        self.private_ipv6_ranges = [
            'fc00::/7',          # Unique local address
            'fe80::/10',         # Link-local address
            '::1/128',           # Localhost
        ]
        
        # Initialize network objects
        self.blocked_networks = self._init_network_objects()

    def _init_network_objects(self) -> List[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]:
        """Initialize network objects for IP range checking"""
        networks = []
        
        # Add IPv4 networks
        for ip_range in self.private_ipv4_ranges:
            networks.append(ipaddress.ip_network(ip_range))
            
        # Add IPv6 networks
        for ip_range in self.private_ipv6_ranges:
            networks.append(ipaddress.ip_network(ip_range))
            
        return networks

    def _is_ip_private(self, ip: str) -> bool:
        """
        Check if an IP address is in a private range.
        
        Args:
            ip (str): IP address to check
            
        Returns:
            bool: True if IP is private, False otherwise
        """
        try:
            ip_addr = ipaddress.ip_address(ip)
            return any(ip_addr in network for network in self.blocked_networks)
        except ValueError:
            return False

    def check_url_security(self, url: str) -> bool:
        """
        Performs security checks on the URL.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL passes security checks, False otherwise
        """
        try:
            domain = get_domain(url)
            if not domain:
                return False

            # Try to resolve domain to IP
            try:
                ip = socket.gethostbyname(domain)
                if self._is_ip_private(ip):
                    return False
            except socket.gaierror:
                # If we can't resolve the IP, we'll err on the side of caution
                return False

            # Additional security checks can be added here
            # For example: checking against a blocklist, rate limiting, etc.

            return True
            
        except Exception:
            return False

# Create a singleton instance
security_checker = SecurityChecker()

def check_url_security(url: str) -> bool:
    """
    Wrapper function for the security checker.
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if URL passes security checks, False otherwise
    """
    return security_checker.check_url_security(url)

