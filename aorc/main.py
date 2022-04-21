import sys
import os
import curses
import subprocess
__version__ = "0.4.0"

# print(sys.path)
test_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(project_dir, "simple_curses")
project_dir = os.path.abspath("../")
if not project_dir in sys.path:
    # print("Adding to sys.path")
    sys.path.append(project_dir)
    sys.path.append(src_dir)

from simple_curses import *

# from simple_curses .view import View, BannerView
# from simple_curses.widget_base import MenuItem
# from simple_curses.banner_widget import BannerWidget, HelpWidget, BlockTextWidget
# from simple_curses.text_widget import TextWidget, IntegerWidget, IPAddressWidget, PathWidget
# from simple_curses.multi_line_widget import IPNetworkCIDR
# from simple_curses.toggle_widget import ToggleWidget

# from simple_curses.appbase import AppBase

from aorc.state import AorcState
from aorc.actions import program_cancel, run_add_prefix_new, view_cancel, run_add_prefix_notnew, run_remove_prefix_disconnect, run_remove_prefix_notdisconnect
from aorc.config_actions import run_config_action


def test_screen_size(stdscr, required_height, required_width):
    h, w = stdscr.getmaxyx()
    if h < required_height or w < required_width:
        raise Exception(
            "SCreen is too small must be at least {} high and {} wide currently is high: {} wide: {}".format(
                required_height, required_width, h, w))


def menu_action_0(app, view, context):
    app.msg_info("menu action 0")


def menu_action_11(app, view, context):
    v = view.get_values()
    s = ""
    if v is not None:
        for k in v.keys():
            s += "v[{}] = {}, ".format(k, v[k])

    app.msg_info("menu action 1-1 {}".format(v))
    # run a command with elements of v as arguments


def menu_action_12(app, view, context):
    app.msg_info("menu action 1-2")


def menu_action_13(app, view, context):
    app.msg_info("menu action 1-3 app:{} view:{} context:{}".format(app, view.__dict__, context))


def config_action(app, view, context):
    app.msg_info("Config:: {}".format(app.state.__dict__))


class App(AppBase):
    """
    Here we define a class called App (name is not important - BUT MUST inherit from AppBase)
    The purpose of this class is to provide a shell inside of which we can define:
    - one or more Views
    - the arrangement of text and data entry fields inside each of those views 
      -   the __init__() function for the custom App class must be exactly as given below
      -   def register_views() - this function is where you define your views and their
          component widgets.
          NOTE: the last line of this function MUST be included:
                self.views = [view_banner, view_help, view_data_entry_01]
    """

    def __init__(self, stdscr, body_height, width, msg_height=20, context=None, input_timeout_ms=2):
        # do not mosify this line

        self.state = AorcState()

        super().__init__(stdscr, body_height, width, msg_height=10, context=context)

    def register_views(self):
        # start of customization
        data = self.state

        view_banner = BannerView(self, "bview_01", "Banner View", self.stdscr, self.body_win, BannerWidget(self))
        view_help = BannerView(self, "help_01", "Help   View", self.stdscr, self.body_win, HelpWidget(self))

        ##########################################################
        # add prefixes with a new install
        ##########################################################
        add_prefixes_new_install_widgets = [

            TextWidget(self, "cust_name", "Cust name           ", 23, data),
            BlockTextWidget(self, [
                    "Order Type:",
                    "    Either enter a Business Org Id or", 
                    "    select one of", 
                    "    Marvel order or DM order"
            ]),
            TextWidget(self, "bus_org_id",        "Business Org ID ", 23, data),
            ToggleWidget(self, "is_marvel_order", "Marvel Order ?  ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_dm_order",     "DM order     ?  ", 3, data, ['No ', "Yes"]),
            BlockTextWidget(self, [" "," "]),

            ToggleWidget(self, "is_aorc_capitalized",
                                                  "Is aorc capitalized            ", 3, data, ['No ', "Yes"]),

            IntegerWidget(self, "nokia_entry_nbr",
                                                  "New install Nokia entry number ", 23, data),
            IPAddressWidget(self, "next_hop_ip",  "New install Next hop IP        ", 23, data),

            IPNetworkCIDR(app=self, key="prefixes", label="Prefixes", content_width=50,
                          content_height=20, data=data),
        ]

        add_prefixes_new_install_menu = [
            # MenuItem(self, "Validate", 13, 3, 0, validate, "context for menu 1"),
            MenuItem(self, "Exit Program", 14, 3, 0, program_cancel, ""),
            MenuItem(self, "Cancel", 7, 3, 0, view_cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, run_add_prefix_new, "context for menu 3")
        ]
        add_prefixes_new_install_view = View(self, "add_new_install", "Add prefix - New Install", self.stdscr,
                                             self.body_win, add_prefixes_new_install_widgets,
                                             add_prefixes_new_install_menu)

        ##########################################################
        # add prefixes but NOT with a new install
        ##########################################################
        add_prefixes_not_new_install_widgets = [

            TextWidget(self, "cust_name", "Cust name           ", 23, data),
            TextWidget(self, "bus_org_id", "Business Org ID     ", 23, data),
            ToggleWidget(self, "is_marvel_order", "Is a Marvel Order   ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_dm_order", "Is a DM order       ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_aorc_capitalized",
                         "Is aorc capitalized ", 3, data, ['No ', "Yes"]),

            IntegerWidget(self, "nokia_entry_nbr",
                          "New install Nokia entry number ", 23, data),
            IPAddressWidget(self, "next_hop_ip", "New install Next hop IP        ", 23, data),

            IPNetworkCIDR(app=self, key="prefixes", label="Prefixes", content_width=50,
                          content_height=20, data=data),
        ]

        add_prefixes_not_new_install_menu = [
            # MenuItem(self, "Validate", 13, 3, 0, validate, "context for menu 1"),
            MenuItem(self, "Exit Program", 14, 3, 0, program_cancel, ""),
            MenuItem(self, "Cancel", 7, 3, 0, view_cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, run_add_prefix_notnew, "context for menu 3")
        ]
        add_prefixes_not_new_install_view = View(self, "add_not_new_install", "Add prefix - NOT - New Install",
                                                 self.stdscr, self.body_win,
                                                 add_prefixes_not_new_install_widgets,
                                                 add_prefixes_not_new_install_menu)

        ##########################################################
        # remove prefixes with a disconnect
        ##########################################################
        remove_prefixes_with_disconnect_widgets = [

            TextWidget(self, "cust_name", "Cust name           ", 23, data),
            TextWidget(self, "bus_org_id", "Business Org ID     ", 23, data),
            ToggleWidget(self, "is_marvel_order", "Is a Marvel Order   ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_dm_order", "Is a DM order       ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_aorc_capitalized",
                         "Is aorc capitalized ", 3, data, ['No ', "Yes"]),

            IntegerWidget(self, "nokia_entry_nbr",
                          "New install Nokia entry number ", 23, data),
            IPAddressWidget(self, "next_hop_ip", "New install Next hop IP        ", 23, data),

            IPNetworkCIDR(app=self, key="prefixes", label="Prefixes", content_width=50,
                          content_height=20, data=data),
        ]

        remove_prefixes_with_disconnect_menu = [
            # MenuItem(self, "Validate", 13, 3, 0, validate, "context for menu 1"),
            MenuItem(self, "Exit Program", 14, 3, 0, program_cancel, ""),
            MenuItem(self, "Cancel", 7, 3, 0, view_cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, run_remove_prefix_disconnect, "context for menu 3")
        ]
        remove_prefixes_with_disconnect_view = View(self, "add_not_new_install", "Remove prefixes with disconnect",
                                                    self.stdscr, self.body_win,
                                                    remove_prefixes_with_disconnect_widgets,
                                                    remove_prefixes_with_disconnect_menu)

        ##########################################################
        # remove prefixes but NOT with a disconnect
        ##########################################################
        remove_prefixes_not_disconnect_widgets = [

            TextWidget(self, "cust_name", "Cust name           ", 23, data),
            TextWidget(self, "bus_org_id", "Business Org ID     ", 23, data),
            ToggleWidget(self, "is_marvel_order", "Is a Marvel Order   ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_dm_order", "Is a DM order       ", 3, data, ['No ', "Yes"]),
            ToggleWidget(self, "is_aorc_capitalized",
                         "Is aorc capitalized ", 3, data, ['No ', "Yes"]),

            IntegerWidget(self, "nokia_entry_nbr",
                          "New install Nokia entry number ", 23, data),
            IPAddressWidget(self, "next_hop_ip", "New install Next hop IP        ", 23, data),

            IPNetworkCIDR(app=self, key="prefixes", label="Prefixes", content_width=50,
                          content_height=20, data=data),
        ]

        remove_prefixes_not_with_disconnect_menu = [
            # MenuItem(self, "Validate", 13, 3, 0, validate, "context for menu 1"),
            MenuItem(self, "Exit Program", 14, 3, 0, program_cancel, ""),
            MenuItem(self, "Cancel", 7, 3, 0, view_cancel, "context for menu 2"),
            MenuItem(self, "Ok-Run", 7, 3, 0, run_remove_prefix_notdisconnect, "context for menu 3")
        ]

        remove_prefixes_not_with_disconnect_view = View(self, "add_not_new_install",
                                                        "Remove prefixes - NOT - with disconnect", self.stdscr,
                                                        self.body_win,
                                                        remove_prefixes_not_disconnect_widgets,
                                                        remove_prefixes_not_with_disconnect_menu)

        ##########################################################
        # aorc constants configuration
        ##########################################################
        config_widgets = [

            BlockTextWidget(self, [
                "The following are paths to files that will be created",
                "by this program"
            ]),

            PathWidget(self, "config_exception_file", "Exception File Path    ", 70, data),
            PathWidget(self, "config_v14_command_file", "V14 Command File Path  ", 70, data),
            PathWidget(self, "config_quick_push_file", "Quick Push File Path   ", 70, data),
            PathWidget(self, "config_save_file", "Save File Path         ", 70, data),
            PathWidget(self, "config_pid_file", "PID File Path          ", 70, data),

            BlockTextWidget(self, [
                ""
            ]),

            BlockTextWidget(self, [
                "This next field is string constant used by the program NOT a file path",
            ]),

            TextWidget(self, "config_policy_name", "DDOS Policy Name Constant ", 70, data),

        ]

        config_menu = [
            MenuItem(self, "Exit Program", 14, 3, 0, program_cancel, ""),
            MenuItem(self, "Cancel", 7, 3, 0, view_cancel, "context for menu 2"),
            MenuItem(self, "Save", 7, 3, 0, run_config_action, "context for menu 3")
        ]

        config_view = View(self, "config", "AORC Config values", self.stdscr, self.body_win,
                           config_widgets,
                           config_menu)

        # end of customization

        # the next line is required - do not change
        self.views = [
            add_prefixes_new_install_view,
            # add_prefixes_not_new_install_view,
            # remove_prefixes_with_disconnect_view,
            # remove_prefixes_not_with_disconnect_view,
            config_view,
            view_banner,
            # view_help,
        ]


def main(stdscr):
    data = "dummy context"
    required_height = 36
    required_width = 128
    test_screen_size(stdscr, required_height, required_width)
    curses.curs_set(2)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    app = App(stdscr, body_height=required_height, width=required_width, context=data)
    app.run()


curses.wrapper(main)
