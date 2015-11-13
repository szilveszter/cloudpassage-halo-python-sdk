import os
import imp
import pytest
import json
import datetime



module_path = os.path.abspath('../')
#path = os.path.abspath('../cloudpassage/halo.py')
policy_path = os.path.abspath('./policies/')
#cpapi = imp.load_source('HALO', path)

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
api_hostname = os.environ.get('HALO_API_HOSTNAME')

"""
@pytest.fixture(scope='class')
def api_calls():
    return halo.HALO()

@pytest.fixture(scope='class')
def get_token():
    auth = halo.HALO()
    auth.key_id = key_id
    auth.secret = secret_key
    auth.base_url = api_hostname
    token = auth.authenticateClient()
    return token

@pytest.mark.usefixtures('api_calls')
@pytest.mark.usefixtures('get_token')
class TestAPI:
    def test_cpapi_url_default(self):
        api = api_calls()
        default_url = 'https://api.cloudpassage.com'
        default_port = 443

        assert api.base_url == default_url
        assert api.port == default_port

    def test_cpapi_url_override(self):
        api = api_calls()
        override = 'https://nonexist.cloudpassage.com'

        api.base_url = override
        assert api.base_url == override

    def test_cpapi_auth(self):
        api = api_calls()
        api.key_id = key_id
        api.secret = secret_key
        api.base_url = api_hostname

        token = api.authenticateClient()
        assert len(str(token)) == 32

    def test_get_request(self):
        api = api_calls()
        token = get_token()
        request = '/v1/servers'
        endpoint = api_hostname + request
        resp = api.doGetRequest(endpoint, token)
        data =  json.loads(resp[0])
        assert 'servers' in data

    def test_get_server_list(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        resp = api.getServerList()
        assert 'servers' in resp[0]

    def test_get_server_group_list(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        resp = api.getServerGroupList()
        assert 'groups' in resp[0]

    def test_get_servers_in_group(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        slist = api.getServerList()
        target_server = slist[0]["servers"][0]
        target_server_grp_id = target_server["group_id"]
        resp = api.getServersInGroup(target_server_grp_id)
        assert 'servers' in resp[0]

    def test_get_server_details(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        servers = api.getServerList()
        server_id = servers[0]["servers"][0]["id"]
        server_details = api.getServerDetails(server_id)
        assert server_id in server_details[0]["server"]["id"]

    def test_firewall_policy_list(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        fw_policies = api.getFirewallPolicyList()
        assert 'firewall_policies' in fw_policies[0]

    def test_get_firewall_policy_details(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        fw_policies = api.getFirewallPolicyList()
        target_fw_policy_id = fw_policies[0]["firewall_policies"][0]["id"]
        fw_policy_details = api.getFirewallPolicyDetails(target_fw_policy_id)
        assert 'firewall_policy' in fw_policy_details[0]

    def test_get_servers_auth_error(self):
        print("We should see an auth error -->")
        api = api_calls()
        token_rip = list(get_token())
        if token_rip[0] == 'A':
            token_rip[0] = 'B'
        else:
            token_rip[0] = 'A'
        api.key_id = key_id
        api.secret = secret_key
        api.base_url = api_hostname
        api.authenticateClient()
        api.authToken = "".join(token_rip)
        resp = api.getServerList()
        authError = resp[1]
        assert authError == True

    def test_create_delete_server_group(self):
        # Create a fairly unique group name
        grp_name = "TEST_GROUP-" + str(datetime.datetime.now()).replace(' ','_').replace(':','_').replace('.','_')
        api = api_calls()
        token = get_token()
        api.authToken = token
        # Create the new group
        create_resp, create_err = api.createServerGroup(grp_name)
        #print create_resp
        grp_id = create_resp["group"]["id"]
        # Delete the new group
        del_success, err = api.deleteServerGroup(grp_id)
        assert err == False

    def test_get_announcements(self):
        api = api_calls()
        token = get_token()
        api.authToken = token
        retval = api.getAnnouncements()
        assert 'announcements' in retval[0]

    def test_initiate_sva_scan(self):
        scan_type = 'sva'
        api = api_calls()
        token = get_token()
        api.authToken = token
        server_list =  api.getServerList()
        target_server_id = server_list[0]["servers"][0]["id"]
        retval = api.initiateScan(target_server_id, scan_type)
        assert 'command' in retval[0]

    def test_initiate_bad_scan(self):
        scan_type = 'barf'
        api = api_calls()
        token = get_token()
        api.authToken = token
        server_list =  api.getServerList()
        target_server_id = server_list[0]["servers"][0]["id"]
        retval = api.initiateScan(target_server_id, scan_type)
        assert 'command' not in retval[1]

    def test_policy_group_create_destroy(self):
        success = True
        grp_name = "CPAPI-TEST"
        csm_file = "cis-benchmark-for-centos-7-v1.policy.json"
        fim_file = "core-system-files-centos-v1.fim.json"
        fw_file = "firewall.json"
        lids_file= "core-system-centos-v1-1.lids.json"
        api = api_calls()
        token = get_token()
        api.authToken = token
        # Load up policy contents
        for fname in [csm_file, fim_file, fw_file, lids_file]:
            with open(os.path.join(policy_path, fname), "r") as fobj:
                data=json.load(fobj)
                ptype = data.items()[0][0]
                if ptype == "policy":
                    csm_ret = api.createConfigurationPolicy(data)
                elif ptype == "fim_policy":
                    fim_ret = api.createFIMPolicy(data)
                elif ptype == "lids_policy":
                    lids_ret = api.createLIDSPolicy(data)
                elif ptype == "firewall_policy":
                    fw_ret = api.createFirewallPolicy(data)
        try:
            lids_id = lids_ret[0]["lids_policy"]["id"]
        except:
            print("Failed to set LIDS policy ID.  Manual cleanup may be necessary.")
            lids_id = ""
            success = False
        try:
            csm_id = csm_ret[0]["policy"]["id"]
        except:
            print("Failed to set CSM policy ID.  Manual cleanup may be necessary.")
            csm_id = ""
            success = False
        try:
            fim_id = fim_ret[0]["fim_policy"]["id"]
        except:
            print("Failed to set LIDS policy ID.  Manual cleanup may be necessary.")
            fim_id = ""
            success = False
        try:
            fw_id = fw_ret[0]["firewall_policy"]["id"]
        except:
            print("Failed to set LIDS policy ID.  Manual cleanup may be necessary.")
            fw_id = ""
            success = False
        # Create Group
        grp_create_ret = api.createServerGroup(grp_name,
                                       linux_firewall_policy_id=fw_id,
                                       policy_ids=[csm_id],
                                       linux_fim_policy_ids=[fim_id],
                                       lids_policy_ids=[lids_id])
        try:
            grp_id = grp_create_ret[0]["group"]["id"]
        except:
            print("Failed to set group ID.  Manual cleanup may be necessary.")
            success = False
        if grp_id not in json.dumps(api.getServerGroupList()[0]):
            print("Server group ID not in server group list!")
            print(api.getServerGroupList()[0])
            success = False
        # Find policy IDs in list for pol type
        if fw_id not in json.dumps(api.listFirewallPolicies()[0]):
            print("Failed to find firewall policy in list!!")
            success = False
        if csm_id not in json.dumps(api.listConfigurationPolicies()[0]):
            print("Failed to find CSM policy in list!")
            success = False
        if fim_id not in json.dumps(api.listFIMPolicies()[0]):
            print("Failed to find FIM policy in list!!")
            success = False
        if lids_id not in json.dumps(api.listLIDSPolicies()[0]):
            print("Failed to find LIDS policy in list!!")
            success = False
        # Update server group, removing all policies
        grp_mod_ret = api.updateServerGroup(grp_id,
                                            linux_firewall_policy_id=None,
                                            policy_ids=[],
                                            linux_fim_policy_ids=[],
                                            lids_policy_ids=[])
        if grp_mod_ret[0] != None:
            print("Call to updateServerGroup failed.")
            success = False
        # Delete Group
        grp_delete_ret = api.deleteServerGroup(grp_id)
        if grp_delete_ret[0] != None:
            print("Failed to delete group.  Manual cleanup may be necessary.")
            success = False
        # Delete policies
        fw_del = api.deleteFirewallPolicy(fw_id)
        csm_del = api.deleteConfigurationPolicy(csm_id)
        fim_del = api.deleteFIMPolicy(fim_id)
        lids_del = api.deleteLIDSPolicy(lids_id)
        for delete in [fw_del, csm_del, fim_del, lids_del]:
            if delete[1] != False:
                print("Delete job failed: %s") % str(delete)
                success = False
        assert success == True

"""
