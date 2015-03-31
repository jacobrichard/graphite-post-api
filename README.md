# graphite-post-api
This is an extension of the django graphite-webapp to recieve post requests with data and hand htem off to carbon. 

# Installation
* Drop api/ into the graphite webapp directory (/opt/graphite/webapp/graphite/)
* Add graphite.api to INSTALLED_APPS in app_settings.py
* Add the API settings to local_settings.py
* Include ('^api/?', include('graphite.api.urls')) in urls.py
