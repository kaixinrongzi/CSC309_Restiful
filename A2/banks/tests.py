from django.test import TestCase
import requests

# Create your tests here.
# def main():
#     url_register = f"http://localhost:8000/accounts/register/"
#     data_register = {"username": "hacker3091", "password1": "csc309pw", "password2": "csc309pw"}
#     url_login = f"http://localhost:8000/accounts/login/"
#     data_login = {"username": "hacker3092", "password": "csc309pw"}
#     url_add_bank = f"http://localhost:8000/banks/add/"
#     data_add_bank = {"name": "Utm1", "description": "First Bank of UTM", "inst_num": "123",
#                      "swift_code": "UTMCSCC1"}
#     data_add_branch_1 = {"name": "UtmBranch1", "transit_num": "12345", "address": "UTM",
#                          "email": "branch@utoronto.ca"}
#     data_add_branch_2 = {"name": "UtmBranch1", "transit_num": "12345", "address": "UTM",
#                          "email": "branch@utoronto.ca", "capacity": 10}
#
#     res1 = requests.post(url_register, data=data_register)
#     res2 = requests.post(url_login, data=data_login, allow_redirects=False)
#     # cls.cookies = res2.cookies.get_dict()
#     res3 = requests.post(url_add_bank, data=data_add_bank, allow_redirects=False, cookies=cls.cookies)
#     # bank_id = re.search(r"/banks/([0-9]*)/details/", res3.headers["Location"]).group(1)
#
#     # url_add_branch = f"http://localhost:{PORT}/banks/" + bank_id + "/branches/add/"
#     #
#     # res4 = requests.post(url_add_branch, data=data_add_branch_1, allow_redirects=False, cookies=cls.cookies)

