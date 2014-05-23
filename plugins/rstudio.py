from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class RStudioServerInstaller(ClusterSetup):
    '''Install R and RStudio Server'''
    def __init__(self):
        log.info('Installing Rstudio Server on port 8787 of each node')
        self.debian_pkgs="r-base-core gdebi-core libapparmor1"
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing %s on %s" % ("Rstudio Server", node.alias))
            node.ssh.execute('sudo apt-get -y install %s' % self.debian_pkgs)
            node.ssh.execute("wget http://download2.rstudio.org/rstudio-server-0.98.507-amd64.deb")
            node.ssh.execute("sudo gdebi -n rstudio-server-0.98.507-amd64.deb")
            node.ssh.execute("rstudio-server verify-installation")
            #TODO: might be a more elegant/secure way to do this
            node.ssh.execute("echo rstudio:beachworks:1008:1000:RStudio:/home/rstudio:/bin/bash > deleteme")
            node.ssh.execute("newusers deleteme")
            node.ssh.execute("rm -f deleteme")
