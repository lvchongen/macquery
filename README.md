# Mac address lookup API


You can read this document by ![contents](https://github.com/lvchongen/macquery/blob/master/README.pdf)


### Usage

##### Command Line 

The queryMac.py is used python3, so if you want to run it in your real environment. You need to install python3 and required libs.

```

git clone https://github.com/lvchongen/macquery.git

cd macquery

pip install -r ./requirement.txt

python queryMac.py mac-address  # like 44:38:39:ff:ef:57
```

After running the scripts and pass the mac-address, it would give up results as below:

![mac_real_result](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-06-mac_real_result.png)


##### Virtual Python Environment

If you want to use virtual environment, please install the [virtualenv](https://pypi.org/project/virtualenv/) firstly. 

```

git clone https://github.com/lvchongen/macquery.git

virtualenv -p python3 ./venv3

source ./venv3/bin/activate

cd macquery

pip install -r ./requirement.txt

python queryMac.py mac-address  # like 44:38:39:ff:ef:57

```


##### Docker Container Execution

If you want to query mac-address by using docker. I package this script into the docker image. The dockerfile is below:

```
FROM python:3.7

MAINTAINER chlv lvchongen@gmail.com

ADD queryMac.py /

RUN pip install requests

RUN pip install beautifulsoup4

ENTRYPOINT [ "python", "/queryMac.py"]
```


You can build this image and start container to do mac-address query:

```
git clone https://github.com/lvchongen/macquery.git

cd macquery

docker build -t testpython .     # You c gan use different tag for docker image
 
docker run --rm testpython:latest mac-address  # like 44:38:39:ff:ef:57

```

After running the container it would give us results and delete the unused container.

![mac_docker](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-06-mac_docker.png)







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



### Linux Toolbox

Linux has many commands that can be called in the termincal directly, because system stores the commands under the path `/usr/bin,/usr/local/bin,/usr/sbin`. So if we want to add python scripts to "toolbox" can be called anywhere in terminal. We need to copy/link the script to one of above folders.



##### Method 1: link file to /usr/local/bin

1. Add the execute path to scrpts

	`#!/usr/bin/env python`
	
2. Change the permission of python script file.

	```
	cp queryMac.py queryTool.py
	
	chmod +x quertTool.py

3. Link the script to path `/usr/local/bin`:

	`sudo ln -s $PWD/queryTool.py /usr/local/bin/queryMac`
	
4.	Test this command like 	

	![mac_query](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-06-mac_local.png)
	
	
##### Method 2: using *python setup.py install*

1.	Create setup.py file contains below content:

	```
	from setuptools import setup

	setup(
	    scripts = [
	        'scripts/queryMac.py'  #This is the path of the scripts
	    ]
	)
	```

2. Execute command `python setup.py install` 

3. Test this command like:

	![mac_setup](https://lvchongen-1255888772.cos.ap-chengdu.myqcloud.com/2020-09-06-mac_setup.png)
