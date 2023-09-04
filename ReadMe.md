1. **Setting up Cloud environment to configure apache webserver to run the Flask Application:-**

Steps to setup Flask app using apache on GCloud:-

Execute the following in the Gcloud VM instance:
```
sudo apt-get install apache2 libapache2-mod-wsgi-py3 python3-pip
sudo ufw app list
sudo ufw allow in "Apache"
sudo service apache2 start
```

```
sudo a2dissite 000-default
sudo a2enmod wsgi
cd /var/www/
```

Create the directory to store the Flask application files:
```
sudo mkdir -p FlaskApp/FlaskApp
sudo chown -R $USER:$USER FlaskApp
cd FlaskApp/FlaskApp
mkdir static templates
Create and write the required code in __init__.py
sudo pip3 install virtualenv
virtualenv venv
```

Edit the FlaskApp.conf file within apache2 directory by using the following instructions:
```
sudo nano /etc/apache2/sites-available/FlaskApp.conf
```

Edit the file to contain:
```
<VirtualHost *:80>
ServerName External_IP_address_of_GCloud_instance
ServerAdmin admin@mywebsite.com
WSGIDaemonProcess FlaskApp python-path=/var/www/FlaskApp:/var/www/FlaskApp/FlaskApp/venv/lib/python3.8/site-packages
WSGIProcessGroup FlaskApp
WSGIScriptAlias /var/www/FlaskApp/flaskapp.wsgi
<Directory /var/www/FlaskApp/FlaskApp/>
Order allow,deny
Allow from all
</Directory>
Alias /static /var/www/FlaskApp/FlaskApp/static
<Directory /var/www/FlaskApp/FlaskApp/static/>
Order allow,deny
Allow from all
</Directory>
ErrorLog ${APACHE_LOG_DIR}/error.log
LogLevel warn
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Additional commands to be executed:
```
sudo a2ensite FlaskApp
sudo service apache2 reload
```

Configure flaskapp.wsgi to provide path to the web application code:
```
nano cd /var/www/FlaskApp
```

Add the following to the file flaskapp.wsgi
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")
from FlaskApp import app as application
application.secret_key = 'key'
```

Restart the apache webserver using the command:
```
sudo service apache2 restart
```

The Flask application will now be up and running on the GCloud virtual machine, to request any endpoint of the application, use the external IP of the GCloud instance followed by the endpoint resource.  <br/><br/><br/>
  

2. **Starting MQTT subscriber on GCloud:-**

Additionally, to enable the subscriber for the heartbeat data and the weight data from the Raspberry Pi, execute the two programs on the GCloud VM using the following steps:-

- Install the required libraries by executing the following command:
```
pip install -r requirements.txt
```

Start the heartbeat service, by executing:
```
cd /var/www/FlaskApp/FlaskApp
python3 main_limit.py
cd /heartbeat
python3 heartbeat_receive.py
```

This will ensure that the MQTT subscriber on GCloud has subscribed to the required topics and is listening for any data.  <br/><br/><br/>
  

3. **Starting the User Interface system:-**

After downloading the User interface scripts, execute the following commands to start the user interface:

- Navigate to the folder with the UI scripts
- Install the required libraries by executing the following command:
```
pip install -r requirements.txt
```

- Open the file main.py and replace the server IP with the GCloud external IP address after the GCloud VM is setup and after the apache webserver is running
- Execute the main.py file by running:
```
python3 main.py
```

- Once it is running, navigate to 127.0.0.1:5000 in the browser to access the user end Flask application using which the Google cloud flask app can be queried/requested.

**Additional information regarding input and output files:-**

We make use of .csv files on the Cloud and as well as on the User Interface side to store the ingredient values and the Raspberry Pi status.

The files are generated and updated by the written programs, no additional input or output files are required to be manually created.

We have added the generated csv files in the codebase, the response.csv and history.csv contain the ingredients values and the timestamp as stored on the Google Cloud and the User end respectively. An additional file named pi_active.csv is used on Google Cloud for storing the heart beat messages from the Pi with the timestamp, we use only the last value, but other values may be used for debugging and monitoring purposes.