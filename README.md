starcluster
===========

Starcluster setup configs and some plugins

To Install:

git clone https://github.com/dave31415/starcluster

Make sure you wan't to get rid of old configuration and type

rm -rf ~/.starcluster

mv starcluster ~/.starcluster

Now you have the right configuration.

Install the StarCluster package

sudo easy_install StarCluster

cd ~/.starcluster

cp params_default.json params.json

Edit the params.json file with your AWS credentials and preferences

Edit the config.template file if needed

Install mako template engine if you don't have it installed

sudo pip install Mako

Create a new config file with info from your private params.json

python make_config.py

Now, run starcluster normally 

starcluster start -c small myclustername

cat .gitignore

Notice that you will not be adding and committing your private credentials or
your actual config file back to the repo. Edit and version the template only
so you can share in a public repo without making your credentials public. 
 


