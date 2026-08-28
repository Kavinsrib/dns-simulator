\# DNS Resolution Path and Caching Simulator



A Python-based simulation of DNS resolution paths and TTL-based caching, developed as a networking/5G simulation project.



\## Overview



This project models a simplified DNS hierarchy consisting of:



\- DNS Client

\- DNS Resolver / Cache

\- Root DNS Server

\- TLD DNS Server

\- Authoritative DNS Server



The simulator implements both recursive and iterative DNS resolution and models the effect of DNS caching on query latency.



\## Features



\- Recursive DNS resolution

\- Iterative DNS resolution

\- Root → TLD → Authoritative DNS hierarchy

\- TTL-based DNS caching

\- Cache expiration

\- Network latency modelling

\- Average latency measurement

\- P95 latency measurement

\- Cache-hit ratio measurement

\- TTL-based performance experiments

\- Recursive vs iterative comparison

\- CSV result generation

\- Latency and cache-performance graphs



\## Project Structure



```text

dns-simulator/

├── dns\_simulator.py

├── run\_experiments.py

├── results/

│   ├── latency\_vs\_ttl.png

│   ├── cache\_hit\_vs\_ttl.png

│   ├── recursive\_vs\_iterative.png

│   └── results.csv

├── report/

└── README.md



Technologies



Python

NumPy

Pandas

Matplotlib

DNS utilities



How to Run



Install the required Python packages:

pip install numpy pandas matplotlib



Run the simulator:

python dns\_simulator.py



Generate the experiments and graphs:

python run\_experiments.py



The generated graphs and numerical results are stored in the results/ directory.



