from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
import json

JSONDC=json.JSONDecoder()
PARS=JSONDC.decode(open('params.json','rU').read())
rstudio_passwd=PARS['RSTUDIO_PASSWD']
shiny_passwd=PARS['SHINY_PASSWD']

def authorize_port(node,port,cidr = '0.0.0.0/0'):
    group = node.cluster_groups[0]
    node.ec2.conn.authorize_security_group(group_id=group.id, ip_protocol='tcp', 
        from_port=port,to_port=port, cidr_ip=cidr)

class RInstaller(ClusterSetup):
    '''Install R'''
    def __init__(self):
        log.info('Installing R and some packages')
        self.cran=['codetools','Rcpp','RJSONIO','bitops','caTools','digest','xtable']
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing %s on %s" % ("R", node.alias))
            node.ssh.execute("wget https://raw.githubusercontent.com/dave31415/downloads/master/install_R_on_ubuntu.sh &> wget.log")
            node.ssh.execute("wget https://raw.githubusercontent.com/dave31415/downloads/master/install_R_packages.R &> wget.log")
            node.ssh.execute("chmod u+x install_R_on_ubuntu.sh")
            node.ssh.execute("./install_R_on_ubuntu.sh")
            
class RStudioServerInstaller(ClusterSetup):
    '''Install R and RStudio Server'''
    def __init__(self):
        log.info('Installing Rstudio Server on port 8787 of each node')
        
        self.port=8787
        self.debian_pkgs="gdebi-core libapparmor1"
        self.pkg_file="rstudio-server-0.98.507-amd64.deb"
        self.root_url="http://download2.rstudio.org"
        self.url=self.root_url+'/'+self.pkg_file
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            #R and Rstudio
            log.info("Installing %s on %s" % ("Rstudio Server", node.alias))
            node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
            node.ssh.execute("wget %s &> wget.log"% self.url)
            node.ssh.execute("sudo gdebi -n %s" % self.pkg_file)
            node.ssh.execute("rm %s" % self.pkg_file)
            node.ssh.execute("rstudio-server verify-installation")
            #the following assumes the rstudio user exists, usually done in config file
            node.ssh.execute("echo rstudio:%s | chpasswd"%rstudio_passwd)
        #only need to authorize the group once
        authorize_port(node,self.port)
            
class ShinyServerInstaller(ClusterSetup):
    '''Install Shiny and R if not installed'''
    def __init__(self):
        log.info('Installing Shiny Server on port 3838 of each node and a webserver')
        self.port=3838
        self.debian_pkgs="gdebi-core"
        self.pkg_file="shiny-server-1.1.0.10000-amd64.deb"
        self.root_url="http://download3.rstudio.org/ubuntu-12.04/x86_64"
        self.url=self.root_url+'/'+self.pkg_file
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            #R and Rstudio
            log.info("Installing %s on %s" % ("Shiny Server", node.alias))
            if True:
                node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
                #having trouble with this line, quotes
                node.ssh.execute("wget %s &> wget.log" % self.url)
                node.ssh.execute("sudo gdebi -n %s" % self.pkg_file)
                node.ssh.execute("rm %s" % self.pkg_file)
                #the following assumes the shiny user exists, usually done in config file
                node.ssh.execute("echo shiny:%s | chpasswd"%shiny_passwd)
            if True:
                #shiny gives you a free webserver
                node.ssh.execute("mkdir -p /srv/shiny-server/www")
                node.ssh.execute("mkdir -p /srv/shiny-server/www/temp")
                node.ssh.execute("mkdir -p /srv/shiny-server/www/info")
                node.ssh.execute(
                "echo \<html\>\<p\>Hello World from %s\</p\>\</html\> > /srv/shiny-server/www/temp/index.html" % node.alias)
            
        #only need to authorize the group once so do it at end
        authorize_port(node,self.port) 
        
