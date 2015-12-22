import cloudpassage
import datetime
import json
import os


policy_file_name = "core-system-files-centos-v1.fim.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestFimPolicy:
    def build_fim_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.FimPolicy(session)
        return(return_obj)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FimPolicy(session)

    def test_list_all(self):
        """This test attempts to get a list of all FIM policies for your
        account.  If you don't have any FIM policies, it will fail.
        """
        request = self.build_fim_policy_object()
        response = request.list_all()
        assert "id" in response[0]

    def test_get_details(self):
        """This test attempts to get the details for one of your FIM policies.
        If you have no configured FIM policies, it will fail.
        """
        request = self.build_fim_policy_object()
        policy_list = request.list_all()
        target_policy_id = policy_list[0]["id"]
        target_policy_body = request.describe(target_policy_id)
        assert "id" in target_policy_body

    def test_fim_policy_create_delete(self):
        deleted = False
        policy_retrieved = {"fim_policy": None}
        request = self.build_fim_policy_object()
        newname = "Functional Test Name Change"
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        policy_id = request.create(policy_body)
        request.delete(policy_id)
        try:
            request.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted

    def test_fim_policy_create_update_delete(self):
        deleted = False
        policy_retrieved = {"fim_policy": None}
        request = self.build_fim_policy_object()
        newname = "Functional Test Name Change"
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        policy_id = request.create(policy_body)
        policy_update = json.loads(policy_body)
        policy_update["fim_policy"]["name"] = newname
        policy_update["fim_policy"]["id"] = policy_id
        request.update(policy_update)
        request.delete(policy_id)
        try:
            request.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted


class TestFimBaseline:
    def build_fim_baseline_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.FimBaseline(session)
        return(return_obj)

    def build_fim_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.FimPolicy(session)
        return(return_obj)

    def get_active_linux_policy(self):
        """This test requires an active Linux FIM policy to run correctly.
        If your account does not have an active Linux FIM policy, this
        test will fail.
        """
        request = self.build_fim_policy_object()
        response = request.list_all()
        target_id = None
        for policy in response:
            if (policy["active"] == True and policy["platform"] == "linux"):
                target_id = policy["id"]
                break
        assert target_id is not None
        return target_id

    def get_active_linux_host(self):
        """This test requires an active Linux host in order to run
        successfilly.
        """
        session = cloudpassage.HaloSession(key_id, secret_key)
        server = cloudpassage.Server(session)
        list_of_active_linux_servers = server.list_all(state="active",
                                                       platform="linux")
        return list_of_active_linux_servers[0]["id"]

    def test_create_update_delete_baseline(self):
        """This test attempts to get an existing, active FIM policy and
        create a baseline using an active Linux host.  It then attempts
        to update then delete the baseline.  If you are lacking an active
        Linux host or an active FIM policy, this test will fail.
        """
        fim_policy_id = self.get_active_linux_policy()
        target_host_id = self.get_active_linux_host()
        fim_baseline = self.build_fim_baseline_object()
        expiration = 1
        comment_text = "Testing Comment"
        baseline_id = fim_baseline.create(fim_policy_id,
                                          target_host_id,
                                          expires=expiration,
                                          comment=comment_text)
        fim_baseline.update(fim_policy_id, baseline_id, target_host_id)
        none_is_success = fim_baseline.delete(fim_policy_id, baseline_id)
        assert none_is_success is None

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FimBaseline(session)

    def test_list_all_baselines_for_policy(self):
        """This test attempts to get a list of baselines for a FIM policy
        in your account.  If you don't have an active FIM policy, this test
        will fail.
        """
        baseline_request = self.build_fim_baseline_object()
        target_policy_id = self.get_active_linux_policy()
        baseline_response = baseline_request.list_all(target_policy_id)
        assert "id" in baseline_response[0]

    def test_get_details_of_baseline(self):
        """This test attempts to get the details of a baseline configured
        in your Halo account.  If you don't have an active FIM policy,
        this test will fail.
        """
        baseline_request = self.build_fim_baseline_object()
        target_policy_id = self.get_active_linux_policy()
        baseline_list = baseline_request.list_all(target_policy_id)
        target_baseline_id = baseline_list[0]["id"]
        baseline_details = baseline_request.describe(target_policy_id,
                                                     target_baseline_id)
        assert "id" in baseline_details
