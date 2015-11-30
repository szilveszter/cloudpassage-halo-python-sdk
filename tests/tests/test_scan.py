import cloudpassage
import pytest
import pep8
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/scan.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestScan:
    def get_fim_scan_with_findings(self):
        scan_type = "fim"
        scan_status = "completed_clean"
        scanner = self.build_scan_object()
        report = scanner.scan_history(module=scan_type, status=scan_status)
        for item in report:
            if (item["critical_findings_count"] >= 0 or
                    item["non_critical_findings_count"] >= 0):
                return item["id"]
        return None

    def build_scan_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.Scan(session)
        return(return_obj)

    def build_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.ServerGroup(session)
        return(return_obj)

    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.Server(session)
        return(return_obj)

    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def get_svm_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            target_group_id = g["id"]
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_group.list_members(target_group_id)
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_csm_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            csm_policies = g["policy_ids"]
            num_members = g["server_counts"]["active"]
            if num_members > 0 and len(csm_policies) > 0:
                members = s_group.list_members(g["id"])
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_fim_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            fim_policies = g["fim_policy_ids"]
            num_members = g["server_counts"]["active"]
            if num_members > 0 and len(fim_policies) > 0:
                members = s_group.list_members(g["id"])
                target_id = members[0]["id"]
                break
        return(target_id)

    def get_sam_target(self):
        target_id = None
        s_group = self.build_server_group_object()
        list_of_groups = s_group.list_all()
        num_members = 0
        for g in list_of_groups:
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_group.list_members(g["id"])
                for member in members:
                    if member["platform"] is not "windows":
                        target_id = members[0]["id"]
                if target_id is not None:
                    break
        return(target_id)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.Scan(session)

    def test_bad_scan_type(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        scanner = cloudpassage.Scan(session)
        s_group = cloudpassage.ServerGroup(session)
        scan_type = "barfola"
        server_id = s_group.list_all()[0]["id"]
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_bad_server_id(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        scanner = cloudpassage.Scan(session)
        scan_type = "svm"
        server_id = "ABC123"
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_scan_type_valid(self):
        valid_types = ["svm", "sva", "csm", "sca", "fim", "sam", "sv"]
        invalid_types = ["death_stare", "lids"]
        session = cloudpassage.HaloSession(key_id, secret_key)
        scanner = cloudpassage.Scan(session)
        for v in valid_types:
            assert scanner.scan_type_supported(v)
        for i in invalid_types:
            assert not scanner.scan_type_supported(i)

    def test_sv_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        command = scanner.initiate_scan(target_id, "sv")
        assert command["id"]

    def test_sca_initiate(self):
        sca_aliases = ["sca", "csm"]
        scanner = self.build_scan_object()
        target_id = self.get_csm_target()
        for alias in sca_aliases:
            command = scanner.initiate_scan(target_id, alias)
            assert command["id"]

    def test_sca_retrieve(self):
        sca_aliases = ["sca", "csm"]
        scanner = self.build_scan_object()
        target_id = self.get_csm_target()
        for alias in sca_aliases:
            report = scanner.last_scan_results(target_id, alias)
            assert report["id"]

    def test_fim_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        command = scanner.initiate_scan(target_id, 'fim')
        assert command["id"]

    def test_fim_retrieve(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        report = scanner.last_scan_results(target_id, 'fim')
        assert report["id"]

    def test_svm_initiate(self):
        svm_aliases = ["svm", "sva"]
        scanner = self.build_scan_object()
        target_id = self.get_svm_target()
        for alias in svm_aliases:
            command = scanner.initiate_scan(target_id, alias)
            assert command["id"]

    def test_svm_retrieve(self):
        svm_aliases = ["svm", "sva"]
        scanner = self.build_scan_object()
        target_id = self.get_svm_target()
        for alias in svm_aliases:
            report = scanner.last_scan_results(target_id, alias)
            assert report["id"]

    def test_sam_initiate(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        command = scanner.initiate_scan(target_id, "sam")
        assert command["id"]

    def test_sam_retrieve(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.last_scan_results(target_id, "sam")
        assert report["id"]

    def test_scan_history(self):
        scanner = self.build_scan_object()
        report = scanner.scan_history()
        assert report[0]["id"]

    """
    def test_scan_history_by_serverid(self):
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(server_id=target_id)
        assert report[0]["server_id"] == target_id
    """

    def test_scan_history_by_single_scan_type(self):
        scan_type = "sam"
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(module=scan_type)
        assert report[0]["module"] == scan_type

    def test_scan_history_by_multi_scan_type(self):
        scan_types = ["sam", "svm"]
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(module=scan_types)
        assert report[0]["module"] in scan_types

    def test_scan_history_by_single_status(self):
        scan_status = "completed_clean"
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(status=scan_status)
        assert report[0]["status"] == scan_status

    def test_scan_history_by_multi_status(self):
        scan_status = ["completed_clean", "completed_with_errors"]
        scanner = self.build_scan_object()
        target_id = self.get_sam_target()
        report = scanner.scan_history(status=scan_status)
        assert report[0]["status"] in scan_status

    """
    def test_scan_details(self):
        scanner = self.build_scan_object()
        target_id = self.get_fim_target()
        report = scanner.scan_history(server_id=target_id)
        details = scanner.scan_details(report[0]["id"])
        assert "id" in details
    """

    def test_fim_findings_details(self):
        target_fim_scan_id = self.get_fim_scan_with_findings()
        scanner = self.build_scan_object()
        details = scanner.scan_details(target_fim_scan_id)
        findings = details["findings"]
        target_finding = findings[0]["id"]
        target_findings_body = scanner.findings(target_fim_scan_id,
                                                target_finding)
        assert "id" in target_findings_body
