starcluster
===========

Starcluster setup configs and some plugins

git clone THIS_REPO
mv starcluster ~/.starcluster

Edit the params.json file with your AWS credentials and preferences

Edit the config.template file if needed

Install mako template engine if you don't have it installed
sudo pip install Mako

Create a new config file with info from your private params.json
python make_config.py

Now, run starcluster normally 

starcluster start -c small myclustername
