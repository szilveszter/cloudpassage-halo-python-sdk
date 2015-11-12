#!/usr/bin/env python
import pytest
import yaml
import sys
import os


def usage():
    print "%s <environment.yml>" % sys.argv[0]
    exit(0)

if len(sys.argv) < 2:
    usage()

with open('configs/{}'.format(sys.argv[1]), 'r') as f:
    env = yaml.load(f)['defaults']
    env_name = sys.argv[1].split('.')[0]

os.environ['HALO_API_HOSTNAME'] = 'https://{}'.format(env['api_hostname'])
os.environ['HALO_KEY_ID'] = env['key_id']
os.environ['HALO_SECRET_KEY'] = env['secret_key']
os.environ['RO_HALO_KEY_ID'] = env['ro_key_id']
os.environ['RO_HALO_SECRET_KEY'] = env['ro_secret_key']

# pytest.main(['--pylama', '-x', 'tests/',
#              '--junit-xml', 'public/reports/%s.xml' % env_name])

pytest.main(['-x', 'tests/',
			 '-s',
             '--junit-xml', 'public/reports/%s.xml' % env_name])
