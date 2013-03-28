tweet
======

Django Application to tweet in twitter

User roles
==========
Authors - who compose tweets and that will be automatically moderated and send from a single twitter test account  
Editors - who will who review tweets that fails moderation

Installation
============
Fork application  
pip install -r requirements.txt  
python manage.py syncdb  
Configure twitter_settings.py with your twitter account details (Make sure that your twitter applicaton has Read, Write and Access direct messages)  
That's it


Test Data
=========
If you want to test application right away, then  
python manage.py loaddata test_data  
It will create test users for you, find below for user credentials  
author / 123456  
editor / 123456  
cmadmin / qburst (django admin)
