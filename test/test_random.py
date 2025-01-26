# import asyncio
# import aiohttp
# import pytest
# from codetiming import Timer
# urls = [
#     'https://www.google.com',
#     'https://www.facebook.com',
#     'https://www.twitter.com'
# ]
# import psutil
from src.random_scripts import Dog, run_print
# from src.random_scripts import loop_through_files
#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.ensure_future(fetch(session, url)) for url in urls]
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             print(response)
#
#
# if __name__ == "__main__":
#     t = Timer(name="class")
#     t.start()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     t.stop()
#
#
#
#
# def test_check_vpn_connection():
#     # Get a list of network interfaces
#     interfaces = psutil.net_if_addrs()
#
#     # Check if any interface has an address in the private IP address range (e.g., 10.x.x.x, 172.16.x.x, 192.168.x.x)
#     for interface, addresses in interfaces.items():
#         for address in addresses:
#             ip_address = address.address
#             if ip_address.startswith(('10.', '172.16.', '192.168.', '172.30')):
#                 print(' VPN connection found')
#                 # return True  # VPN connection found
#     return  # No VPN connection found
#
#
#
#
# import requests
#
# def test_check_url_access():
#     try:
#         response = requests.head("https://hapi.demo-step.bf-cnt.com/")
#         if response.status_code == 200:
#             print(f"You can access ")
#             return True
#         else:
#             print(f"Failed to access. Status code: {response.status_code}")
#             return False
#     except requests.ConnectionError:
#         print(f"Failed to access. Connection error.")
#         return False
#
#
# def test_class_inheritance():
#     # Create an instance of the Dog class
#     dog = Dog("Buddy", "Labrador")
#     talk = dog.speak()  # Output: Buddy is speaking
#
#     # Access attributes from both parent and child classes
#     print(dog.name)   # Output: Buddy
#     print(dog.breed)  # Output: Labrador
#     print(talk)  # Output: Buddy is speaking
#
#
# def test_loop_through_files():
#     test = loop_through_files()
#     print('ok')


# import pandas as pd
# from src.random_scripts import DataFrameSchema
#
#
# def test_pandantic():
#
#     example_df_invalid = pd.DataFrame(
#         data={
#             "example_str": ["foo", "bar", "baz"],
#             "example_int": [2, 4, 12],
#         }
#     )
#
#     df_raised_error = DataFrameSchema.parse_df(
#         dataframe=example_df_invalid,
#         errors="raise",
#     )
#
#     assert 1==1
