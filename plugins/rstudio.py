from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
from starcluster.plugins.ipcluster import _authorize_port as authorize_port

class RStudioServerInstaller(ClusterSetup):
    '''Install R and RStudio Server'''
    def __init__(self):
        log.info('Installing Rstudio Server on port 8787 of each node')
        self.debian_pkgs="r-base-core gdebi-core libapparmor1"
        self.pkg_file="rstudio-server-0.98.507-amd64.deb"
        self.root_url="http://download2.rstudio.org"
        self.url=self.root_url+'/'+self.pkg_file
        self.port=8787
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing %s on %s" % ("Rstudio Server", node.alias))
            node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
            node.ssh.execute("wget %s" % self.url)
            node.ssh.execute("sudo gdebi -n %s" % self.pkg_file)
            node.ssh.execute("rm %s" % self.pkg_file)
            node.ssh.execute("rstudio-server verify-installation")
            #the following assumes the rstudio user exists, usually done in config file
            node.ssh.execute("echo rstudio:beachworks | chpasswd")
            authorize_port("self_dummy_variable",node,self.port,"rstudio_server") 
