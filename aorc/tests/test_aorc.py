import unittest
from aorc_app.aorc_doit import add_to_prefix_list_juniper, add_to_prefix_list_nokia, rem_from_prefix_list_juniper, rem_from_prefix_list_nokia


class Testaorc(unittest.TestCase):
    def test_add_to_prefix_list_nokia(self):
        x = add_to_prefix_list_nokia(nokia_name="nokia_name", prefixes=["192.168.1.0/24"], prefix_list="", entry_num=1, next_hop="192.168.0.1", new=True )
        print(x)


if __name__ == '__main__':
    unittest.main()
