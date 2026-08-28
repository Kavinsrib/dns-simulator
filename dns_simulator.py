import random
import time
from dataclasses import dataclass


# ============================================================
# DNS RECORD
# ============================================================

@dataclass
class DNSRecord:
    domain: str
    ip: str
    ttl: float


# ============================================================
# DNS SERVERS
# ============================================================

class RootServer:
    def query(self, domain):
        # Root server gives referral to the appropriate TLD
        tld = domain.split(".")[-1]
        return f"TLD server for .{tld}"


class TLDServer:
    def query(self, domain):
        # TLD server gives referral to authoritative server
        return f"Authoritative server for {domain}"


class AuthoritativeServer:
    def __init__(self):
        self.records = {
            "www.example.com": "93.184.216.34",
            "www.google.com": "142.250.72.14",
            "www.youtube.com": "142.250.72.206",
            "www.amazon.com": "205.251.242.103",
            "www.github.com": "140.82.112.3",
            "www.cloudflare.com": "104.16.132.229",
            "www.microsoft.com": "20.112.250.133",
            "www.apple.com": "17.253.144.10",
            "www.netflix.com": "52.85.61.1",
            "www.meta.com": "157.240.241.17",
        }

    def query(self, domain, ttl):
        ip = self.records.get(domain, "0.0.0.0")
        return DNSRecord(domain, ip, ttl)


# ============================================================
# DNS CACHE
# ============================================================

class DNSCache:
    def __init__(self):
        self.entries = {}

    def lookup(self, domain, current_time):
        if domain not in self.entries:
            return None

        record, expiry = self.entries[domain]

        if current_time < expiry:
            return record

        # TTL expired
        del self.entries[domain]
        return None

    def insert(self, record, current_time):
        self.entries[record.domain] = (
            record,
            current_time + record.ttl
        )


# ============================================================
# DNS SIMULATOR
# ============================================================

class DNSSimulator:

    def __init__(self, ttl=30):
        self.ttl = ttl

        self.root = RootServer()
        self.tld = TLDServer()
        self.auth = AuthoritativeServer()

        self.cache = DNSCache()

        # Approximate network latency in milliseconds
        self.client_to_resolver = 5
        self.resolver_to_root = 20
        self.root_to_tld = 15
        self.tld_to_auth = 20
        self.auth_processing = 2

    # --------------------------------------------------------
    # Recursive DNS
    # --------------------------------------------------------

    def recursive_query(self, domain, current_time):

        # Check resolver cache first
        cached = self.cache.lookup(domain, current_time)

        if cached:
            return cached, self.client_to_resolver, True

        latency = 0

        # Client -> Recursive Resolver
        latency += self.client_to_resolver

        # Resolver -> Root
        latency += self.resolver_to_root

        self.root.query(domain)

        # Root -> TLD
        latency += self.root_to_tld

        self.tld.query(domain)

        # TLD -> Authoritative
        latency += self.tld_to_auth

        record = self.auth.query(domain, self.ttl)

        latency += self.auth_processing

        # Store result in resolver cache
        self.cache.insert(record, current_time)

        # Return answer to client
        latency += self.client_to_resolver

        return record, latency, False

    # --------------------------------------------------------
    # Iterative DNS
    # --------------------------------------------------------

    def iterative_query(self, domain, current_time):

        # Client maintains its own cache
        cached = self.cache.lookup(domain, current_time)

        if cached:
            return cached, self.client_to_resolver, True

        latency = 0

        # Client -> Root
        latency += self.resolver_to_root

        self.root.query(domain)

        # Client -> TLD
        latency += self.root_to_tld

        self.tld.query(domain)

        # Client -> Authoritative
        latency += self.tld_to_auth

        record = self.auth.query(domain, self.ttl)

        latency += self.auth_processing

        # Cache answer at client
        self.cache.insert(record, current_time)

        # Authoritative -> Client
        latency += self.client_to_resolver

        return record, latency, False


# ============================================================
# SINGLE EXPERIMENT
# ============================================================

def run_experiment(
    mode="recursive",
    ttl=30,
    queries=1000,
    query_interval=1.0,
    popularity=0.8
):

    domains = [
        "www.example.com",
        "www.google.com",
        "www.youtube.com",
        "www.amazon.com",
        "www.github.com",
        "www.cloudflare.com",
        "www.microsoft.com",
        "www.apple.com",
        "www.netflix.com",
        "www.meta.com",
    ]

    simulator = DNSSimulator(ttl)

    total_latency = 0
    latencies = []

    cache_hits = 0

    current_time = 0

    for _ in range(queries):

        # 80% popular-domain queries, 20% random
        if random.random() < popularity:
            domain = random.choice(domains[:3])
        else:
            domain = random.choice(domains)

        if mode == "recursive":
            _, latency, hit = simulator.recursive_query(
                domain,
                current_time
            )
        else:
            _, latency, hit = simulator.iterative_query(
                domain,
                current_time
            )

        total_latency += latency
        latencies.append(latency)

        if hit:
            cache_hits += 1

        current_time += query_interval

    average_latency = total_latency / queries

    latencies.sort()

    p95_index = int(0.95 * len(latencies)) - 1
    p95_latency = latencies[max(0, p95_index)]

    cache_hit_ratio = cache_hits / queries

    return {
        "mode": mode,
        "ttl": ttl,
        "average_latency": average_latency,
        "p95_latency": p95_latency,
        "cache_hit_ratio": cache_hit_ratio,
        "cache_hits": cache_hits,
        "total_queries": queries,
    }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNS RESOLUTION PATH AND CACHING SIMULATOR")
    print("=" * 60)

    print("\nRecursive DNS example:")

    result = run_experiment(
        mode="recursive",
        ttl=30,
        queries=1000
    )

    print(f"Average latency : {result['average_latency']:.2f} ms")
    print(f"P95 latency     : {result['p95_latency']:.2f} ms")
    print(f"Cache hit ratio : {result['cache_hit_ratio'] * 100:.2f}%")

    print("\nIterative DNS example:")

    result = run_experiment(
        mode="iterative",
        ttl=30,
        queries=1000
    )

    print(f"Average latency : {result['average_latency']:.2f} ms")
    print(f"P95 latency     : {result['p95_latency']:.2f} ms")
    print(f"Cache hit ratio : {result['cache_hit_ratio'] * 100:.2f}%")

    print("\nSimulation completed successfully.")