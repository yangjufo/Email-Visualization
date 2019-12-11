#!/bin/bash

source_folder=/home/ubuntu/sites/emails.jianyang995.com

cd $source_folder/Email-Visualization
git reset *
git pull
sed -i 's/DEBUG = True/DEBUG = False/' ./emailVisualization/settings.py 

$source_folder/env/bin/pip install -r requirements.txt
$source_folder/env/bin/python manage.py collectstatic --noinput


sudo service nginx reload
$source_folder/env/bin/gunicorn --bind unix:/tmp/emails.jianyang995.com.socket emailVisualization.wsgi:application&
