import sys
import os
import curses
import subprocess
# from aorc_app.aorc import App
from typing import Dict, Any, List
from simple_curses import *

from aorc.state import AorcState
from aorc.aorc_doit import *

def execute_command(app, cmd_ar: List[str]):
    """
    Execute a clli command and send the output (stdout and stderr) to the message box
        Parameters:
            app: AorcApp
            cmd_ar: List[str] is an array of strings, each element is components of the cli command 
                                see the subprocess module for details
    """
    out = subprocess.run(cmd_ar, capture_output=True)
    rc = out.returncode
    stdout_lines = out.stdout.decode("utf8").split("\n")
    stderr_lines = out.stderr.decode("utf8").split("\n")
    lines = stderr_lines + stdout_lines
    if rc == 0:
        app.msg_info("SUCCESS - Return is 0")
        for line in lines:
            app.msg_info(line)
    else:
        app.msg_error("FAILED - Return is {}".format(rc))
        for line in lines:
            app.msg_error(line)

def view_cancel(app, view, context):
    """dont update the state, then redisplay the same view with the old state"""
    old_state = app.state
    view.set_values(old_state)
    return

def program_cancel(app, view:View, context):
    """Exit the program"""
    app.msg_info("exit")
    sys.exit(0)

def state_from_view_values(old_state:AorcState, view_values: Dict[str, Any]) -> AorcState:
    """Create a new AorcState from the old state and the View values"""
    new_state = old_state.copy()
    vals = view_values
    new_state.__dict__.update(vals)
    return new_state


def run_add_prefix_new(app, view: View, context):
    """
    This function gets values from the view passed as second parameter.
    Validates those valees an either 
    -   prints an error message using app.msg_error
    -   or executes the required actions to perform add prefix with new insta;;
    """
    keys = [ 
        "cust_name",
        "bus_org_id",
        "is_marvel_order",
        "is_dm_order",
        "is_aorc_capitalized",
        "nokia_entry_nbr",
        "next_hop_ip",
        "prefixes",
        "dop1"
    ]
    # this next statement also performs validation at the field level
    invalid_values = {}
    view_values: Dict[str, str] = view.get_values()

    def check_dop1(k):
        v = view_values[k]
        iv = validator.Integer().validate(v)
        if iv is None or type(iv) == int and iv < 0 and iv in [app.state.DD_ONE, app.state.DD_TWO, app.state.DD_THREE]:
            invalid_values[k] = "{} should be positive number".format(v)


    def check_positive_int(k):
        v = view_values[k]
        iv = validator.Integer().validate(v)
        if iv is None or type(iv) == int and iv < 0:
            invalid_values[k] = "{} should be positive number".format(v)

    def check_prefixes(k):
        v = view_values[k]
        if type(v) != list:
            invalid_values[k] = "prefixes should be a list of string values got {}".format(type(v))
        else:
            vals = []
            for s in v:
                ip = validator.IPNetwork().validate(s)
                if ip is None:
                    vals.append(s)
            if len(vals) > 0:
                invalid_values[k] = vals

    def check_boolean(k):
        v = view_values[k]
        if type(v) != bool:
            invalid_values[k] = view_values[k]

    def check_value_for(k, a_validator):
        v = view_values[k]
        if len(v) == 0 or a_validator.validate(v) is None:
            invalid_values[k] = view_values[k]

    def make_error_msg():
        err_msg = []
        for k in invalid_values.keys():
            msg = "field {} has invalid value the value=[{}]".format(k, invalid_values[k])
            err_msg.append(msg)
        return ": ".join(err_msg)


    check_value_for("next_hop_ip", validator.IPAddress())
    check_positive_int("nokia_entry_nbr")
    check_boolean("is_marvel_order")
    check_boolean("is_dm_order")
    check_boolean("is_aorc_capitalized")
    check_prefixes("prefixes")

    if len(invalid_values) > 0:
        app.msg_error("{}".format(make_error_msg()))
        pass
    else:
        # process the data
        app.msg_info("Config save - success {}".format(view_values))
        pass
    new_state = state_from_view_values(app.state, view_values)
    app.state = new_state


def run_add_prefix_notnew(app, view, context):
    """
    This function gets values from the view passed as second parameter.
    Validates those valees an either 
    -   prints an error message using app.msg_error
    -   or executes the required actions to perform add prefix with new insta;;
    """
    keys = [ 
        "cust_name",
        "bus_org_id",
        "is_aorc_capitalized",
        "nokia_entry_nbr",
        "next_hop_ip",
        "prefixes",
        "order_type"
    ]
    # this next statement also performs validation at the field level
    invalid_values = {}
    view_values: Dict[str, str] = view.get_values()


    def check_order_type(ddk, boid_k):
        v = view_values[ddk]
        iv = validator.Integer().validate(v)
        if iv is not None and type(iv) == int and iv in [app.state.ORDERTYPE_MARVEL, app.state.ORDERTYPE_DM, app.state.ORDERTYPE_BOID]:
            if iv == app.state.ORDERTYPE_BOID:
                v2 = view_values[boid_k]
                if v2 is None or type(v2) != str or (type(v2) == str and len(v2) == 0):
                    invalid_values[ddk] = "Business Org Id required"
        else:
            invalid_values[ddk] = "{} order type is an invalid selection".format(v)


    def check_positive_int(k):
        v = view_values[k]
        iv = validator.Integer().validate(v)
        if iv is None or type(iv) == int and iv < 0:
            invalid_values[k] = "{} should be positive number".format(v)

    def check_prefixes(k):
        v = view_values[k]
        if type(v) != list:
            invalid_values[k] = "prefixes should be a list of string values got {}".format(type(v))
        else:
            vals = []
            for s in v:
                ip = validator.IPNetwork().validate(s)
                if ip is None:
                    vals.append(s)
            if len(vals) > 0:
                invalid_values[k] = vals

    def check_boolean(k):
        v = view_values[k]
        if type(v) != bool:
            invalid_values[k] = view_values[k]

    def check_value_for(k, a_validator):
        v = view_values[k]
        if len(v) == 0 or a_validator.validate(v) is None:
            invalid_values[k] = view_values[k]

    def make_error_msg():
        err_msg = []
        for k in invalid_values.keys():
            msg = "field {} has invalid value the value=[{}]".format(k, invalid_values[k])
            err_msg.append(msg)
        return ": ".join(err_msg)


    check_value_for("next_hop_ip", validator.IPAddress())
    check_positive_int("nokia_entry_nbr")
    check_boolean("is_aorc_capitalized")
    check_prefixes("prefixes")
    check_order_type("order_type", "bus_org_id")

    if len(invalid_values) > 0:
        app.msg_error("{}".format(make_error_msg()))
        pass
    else:
        # process the data
        app.msg_info("Config save - success {}".format(view_values))
        pass
    new_state = state_from_view_values(app.state, view_values)
    app.state = new_state

def run_remove_prefix_disconnect(app, view, context):
    run_add_prefix_new(app, view, context)

def run_remove_prefix_notdisconnect(app, view, context):
    run_add_prefix_new(app, view, context)

