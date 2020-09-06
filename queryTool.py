#!/usr/bin/env python

import requests
import json
import sys

from bs4 import BeautifulSoup



def queryMac(mac_address):
	execute_session = requests.Session()

	# Get Token from main page
	base_response = execute_session.get('https://macaddress.io/')   
	base_soup = BeautifulSoup(base_response.text, 'html.parser')
	token = base_soup.find('input', {"name":"_token"}).attrs.get("value")

	# Get redirect url from query api
	base_url = "https://macaddress.io/mac-address-lookup"
	post_data = {
		"_token":token,
		"mac-address-value": mac_address
	}
	originResponse = execute_session.post(url=base_url, data=(post_data), allow_redirects=False)
	redirect_url = originResponse.headers["Location"]

	# Get mac information from redirect url
	redirect_response = execute_session.get(redirect_url)
	redirect_soup = BeautifulSoup(redirect_response.text, 'html.parser')

	mac_data_str = redirect_soup.find("mac-address-report-component").attrs.get("data")
	mac_data_json = json.loads(mac_data_str)

	company_name = mac_data_json["vendorDetails"]["companyName"]
	company_address = mac_data_json["vendorDetails"]["companyAddress"]
	country_name = mac_data_json["vendorDetails"]["countryName"]

	print("【Company Name】: " + company_name)
	print("【Company Address】: " + company_address)
	print("【Country Name】: " + country_name)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please input correct count mac-address")
        sys.exit(0)
    mac_address = sys.argv[1]
    queryMac(mac_address)
