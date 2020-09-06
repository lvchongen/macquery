# Mac address lookup API



### Background

People can access the website [macaddress.io](https://macaddress.io) and search the vendor information by providing mac address. 

*	Open the URL in browser and input the MAC address in the serach field.

	![mac_interface](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_interface.png)
	
*	After click the search button, the browser will give user all informaction about the mac address in redirected url.

	![mac_info](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_info.png)
	
	
	
### Interface analysis


1.	We can use develop tools to capture the http request and response in Chrome. After clicking the search button, the website will request this api as below.

	![mac_request](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_request.png)
	
2.	The post request need two major parameters: **_token** and **mac-address-value**. The **mac-address-value** is provided by user, and I need to know where is the **_token**. Actually, the token should be genearted by backend because token is the key to access backend. So I try to find it in source code of the html. And the token will be changed every time of accessing.

	![mac_source](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_source.png)
	
3. From a safety perspective, the backend should know whether the request has permission. In this website the cookie is the major key. We can get the cookie infomation from first response header as below.
	
	![mac_cookie](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_cookie.png)

	
4. After accessing the API **mac-address-lookup**, browser will navigate to redirected url that contains the search results. The status code of http is used to describe the redirect。

	![mac_redirect](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_redirect.png)
	
	And, the redirect url can be found in lookup api's response header。
	
	![mac_location](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-05-mac_location.png)




**Based on above desciptions, we know the stpes to query mac information.**


1.	Access the website [macaddress.io](https://macaddress.io) to get token. 

2.	Use mac-address and website to request api **mac-address-lookup** and get redirect url from response header.

3. Access the redirect url and get mac information.

