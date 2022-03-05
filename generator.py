# %%
import os
import json

# %%
def dns_job(ip: str):
    return {
        'type': 'udp',
        'args': {
            'address': ip,
            'interval_ms': 1,
            'body': "{{- random_payload 1000 -}}",
        },
    }

# %%
def http_job(ip: str, domain_name: str=''):
    target = domain_name if domain_name != '' else f'{ip}:80'
    return {
        'type': 'http',
        'args': {
            'method': 'GET',
            'path': f'http://{target}',
            'interval_ms': 1,
        },
        'client': {
            'async': True,
        },
    }
# %%

SOURCES_NAME = 'sources.txt'

cwd = os.getcwd()
sources_path = os.path.join(cwd, SOURCES_NAME)

ts = ''

with open(sources_path, 'r') as f:
    ts = f.read()
# %%

config = {'jobs': []}
# %%
for line in ts.splitlines():
    domain, ip, ports, *other = line.split(' ')
    for port in ports.split('/'):
        job = {}
        if port == '53':
            config['jobs'].append(dns_job(ip))
        if port == '80':
            config['jobs'].append(http_job(ip))

# %%
with open('config.json', 'w') as f:
    f.write(json.dumps(config, indent=4))
# %%
