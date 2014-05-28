#template engine
import json
from mako.template import Template

def make_params():
    #start with defaults
    params = {"NODE_INSTANCE_TYPE":"r3.2xlarge","USER_NAME_LIST":''}
    
    #Read json data from parameter file
    JSONDC=json.JSONDecoder()
    PARS=JSONDC.decode(open('params.json','rU').read())

    if PARS["REGION"] == "east":
        params["AVAILABILITY_ZONE"]="us-east-1a"
        params["NODE_IMAGE_ID"] = "ami-6b211202"
        params["AWS_REGION_NAME"]="us-east-1"
        params["AWS_REGION_HOST"]="ec2.us-east-1.amazonaws.com"
    else :
        params["AVAILABILITY_ZONE"]="us-west-2a"
        params["NODE_IMAGE_ID"] = "ami-dfd0a0ef"
        params["AWS_REGION_NAME"]="us-west-2"
        params["AWS_REGION_HOST"]="ec2.us-west-2.amazonaws.com"

    #over-write params with these    
    for k,v in PARS.iteritems():
        key=k.upper()
        params[key]=v
    return params
        
def render_config(params):
    #render the template with parameters from param
    config_template=Template(open('config.template','rU').read())
    #uses dictionary unpacking, **
    return config_template.render(**params)

def make():
    params=make_params()
    config=render_config(params)
    f=open('config','w')
    f.write(config)
    f.close()
    
if __name__ == "__main__":
    make()
