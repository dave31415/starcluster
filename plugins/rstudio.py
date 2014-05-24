from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

def authorize_port(node,port):
    group = node.cluster_groups[0]
    world_cidr = '0.0.0.0/0'
    node.ec2.conn.authorize_security_group(group_id=group.id, ip_protocol='tcp', 
        from_port=port,to_port=port, cidr_ip=world_cidr)

class RStudioServerInstaller(ClusterSetup):
    '''Install R and RStudio Server'''
    def __init__(self):
        log.info('Installing Rstudio Server on port 8787 of each node')
        
        self.port=8787
        self.debian_pkgs="r-base-core gdebi-core libapparmor1"
        self.pkg_file="rstudio-server-0.98.507-amd64.deb"
        self.root_url="http://download2.rstudio.org"
        self.url=self.root_url+'/'+self.pkg_file
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            #R and Rstudio
            log.info("Installing %s on %s" % ("Rstudio Server", node.alias))
            node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
            node.ssh.execute("wget %s" % self.url)
            node.ssh.execute("sudo gdebi -n %s" % self.pkg_file)
            node.ssh.execute("rm %s" % self.pkg_file)
            node.ssh.execute("rstudio-server verify-installation")
            #the following assumes the rstudio user exists, usually done in config file
            node.ssh.execute("echo rstudio:beachworks | chpasswd")
            authorize_port(node,self.port)
            
class ShinyServerInstaller(ClusterSetup):
    '''Install Shiny and R if not installed'''
    def __init__(self):
        log.info('Installing Shiny Server on port 3838 of each node')
        
        self.port=3838
        self.debian_pkgs="r-base-core gdebi-core"
        self.pkg_file="shiny-server-1.1.0.10000-amd64.deb"
        self.root_url="http://download3.rstudio.org/ubuntu-12.04/x86_64"
        self.url=self.root_url+'/'+self.pkg_file
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            #R and Rstudio
            log.info("Installing %s on %s" % ("Rstudio Server", node.alias))
            node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
            node.ssh.execute(''' sudo su - -c "R -e \"install.packages('shiny', repos='http://cran.rstudio.com/')\"" ''')
            node.ssh.execute("wget %s" % self.url)
            node.ssh.execute("sudo gdebi -n %s" % self.pkg_file)
            node.ssh.execute("rm %s" % self.pkg_file)
            #the following assumes the shiny user exists, usually done in config file
            node.ssh.execute("echo shiny:beachworks | chpasswd")
            authorize_port(node,self.port)
                 