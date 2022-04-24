import pathlib
import os
from typing import Any 



class AorcState:
    """
    State object for the aorc application
    """
    
    def __init__(self):
        self.ORDERTYPE_MARVEL = 10
        self.ORDERTYPE_DM = 11
        self.ORDERTYPE_BOID = 12
        self.cust_name = ""
        self.bus_org_id = ""
        self.is_marvel_order = False
        self.is_dm_order = False
        self.is_aorc_capitalized = False
        self.nokia_entry_nbr = 0
        self.next_hop_ip = "192.168.192.168"
        self.prefixes = []
        self.order_type = self.ORDERTYPE_BOID

        aorc_dir = os.path.dirname(__file__)
        self.config_exception_file = "{}".format(os.path.join(aorc_dir, "stuff/ddos2_exceptions"))
        self.config_v14_command_file = "{}".format(os.path.join(aorc_dir, "stuff/ddos2_v14_command_push"))
        self.config_quick_push_file = "{}".format(os.path.join(aorc_dir, "stuff/ddos2_quick_push"))
        self.config_save_file = "{}".format(os.path.join(aorc_dir, "stuff/save"))
        
        self.config_pid_file = "{}".format(os.path.join(aorc_dir, "stuff/ddos2_script.pid"))
        self.config_policy_name = "ddos2-dynamic-check"

        # self.config_exception_file = "{}".format(self.config_exception_file_path)
        # self.config_v14_command_file = "{}".format(self.config_v14_command_file_path)
        # self.config_quick_push_file = "{}".format(self.config_quick_push_path) 
        # self.config_save_file = "{}".format(self.config_save_file_path)
        # self.config_pid_file = "{}/stuff/ddos2_script.pid".format(aorc_dir)
        # self.config_policy_name = "ddos2-dynamic-check"

    def __getitem__(self, key) -> Any:
        return getattr(self, key)


    def __setitem__(self, key, value: Any):
        setattr(self, key, value)


    def copy(self):
        other = AorcState()
        for k in self.__dict__.keys():
            other[k] = self.__dict__[k]
        return other
