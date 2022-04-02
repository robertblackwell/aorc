import sys
import os
import curses
import subprocess
from typing import Any, Dict
from typing import Dict
from aorc.state import AorcState
from aorc.aorc_doit import *
from simple_curses import View
import simple_curses.validator as validator


def state_from_view_values(old_state: AorcState, view_values: Dict[str, Any]) -> AorcState:
    new_state = old_state.copy()
    vals = view_values
    new_state.__dict__.update(vals)
    return new_state


def run_config_action(app, view: View, context):
    
    config_keys = [ 
        "config_exception_file",
        "config_v14_command_file",
        "config_quick_push_file",
        "config_save_file",
        "config_pid_file", 
        "config_policy_name",
    ]
    # this next statement also performs validation at the field level
    invalid_values = {}
    view_values: Dict[str, str] = view.get_values()

    def check_value_for(k, a_validator):
        v = view_values[k]
        if len(v) == 0 or a_validator.validate(view_values[k]) is None:
            invalid_values[k] = view_values[k]

    def make_error_msg():
        err_msg = []
        for k in invalid_values.keys():
            msg = "field {} has invalid value (not a valid file path) the value=[{}]".format(k, invalid_values[k])
            err_msg.append(msg)
        return ": ".join(err_msg)


    check_value_for("config_exception_file", validator.Path())
    check_value_for("config_v14_command_file", validator.Path())
    check_value_for("config_quick_push_file", validator.Path())
    check_value_for("config_save_file", validator.Path())
    check_value_for("config_pid_file", validator.Path())

    if len(invalid_values) > 0:
        app.msg_error("{}".format(make_error_msg()))
        pass
    else:
        # process the data
        app.msg_info("Config save - success {}".format(view_values))
        pass
    

    new_state = state_from_view_values(app.state, view_values)
    app.state = new_state

