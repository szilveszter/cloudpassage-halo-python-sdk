#!/usr/bin/env python


def validate_servergroup_create_args(a):
    val_struct = {"firewall_policy_id": unicode,
                  "linux_firewall_policy_id": unicode,
                  "windows_firewall_policy_id": unicode,
                  "policy_ids": list,
                  "windows_policy_ids": list,
                  "fim_policy_ids": list,
                  "linux_fim_policy_ids": list,
                  "windows_fim_policy_ids": list,
                  "lids_policy_ids": list,
                  "tag": unicode,
                  "events_policy": unicode,
                  "alert_profiles": list}
    for k, v in a.items():
        if k in val_struct:
            if isinstance(v, val_struct[k]):
                continue
            else:
                raise TypeError("Type incorrect for %s.  Is %s.  Should be %s."
                                % (k, type(v), val_struct[k]))
        else:
            raise KeyError("Invalid server group attribute: %s") % k
    return(True)


def validate_servergroup_update_args(a):
    val_struct = {"firewall_policy_id": unicode,
                  "linux_firewall_policy_id": unicode,
                  "windows_firewall_policy_id": unicode,
                  "policy_ids": list,
                  "windows_policy_ids": list,
                  "fim_policy_ids": list,
                  "linux_fim_policy_ids": list,
                  "windows_fim_policy_ids": list,
                  "lids_policy_ids": list,
                  "tag": unicode,
                  "name": unicode,
                  "events_policy": unicode,
                  "alert_profiles": list}
    for k, v in a.items():
        if k in val_struct:
            if isinstance(v, val_struct[k]):
                continue
            elif ((val_struct[k] == unicode) and (v is None)):
                continue
            else:
                raise TypeError("Type incorrect for %s.  Is %s.  Should be %s."
                                % (k, type(v), val_struct[k]))
        else:
            raise KeyError("Invalid server group attribute: %s") % k
    return(True)
