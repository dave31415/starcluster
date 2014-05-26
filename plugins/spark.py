from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SparkInstaller(ClusterSetup):
    '''Install Spark'''
    def __init__(self):
        log.info('Installing Spark')
        self.spark_dir="spark-0.9.1-bin-hadoop1"
        self.url="http://d3kbcqa49mib13.cloudfront.net/%s.tgz" % self.spark_dir

    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Installing %s on %s" % ("Spark", node.alias))
            node.ssh.execute("wget %s &> wget.log" % self.url)
            node.ssh.execute("sleep 2")
            node.ssh.execute("tar xfvz %s.tgz" % self.spark_dir)
            node.ssh.execute("echo %s > %s/conf/slaves" % (node.alias,self.spark_dir))
        self.open_up_all_ports(node)
        master.ssh.execute("%s/sbin/start-all.sh" % self.spark_dir)
        
    def open_up_all_ports(self,node,protocols=['tcp','udp','icmp']):
        #this might not be very secure, revisit
        log.info("Opening up all ports for Spark!")
    
        group = node.cluster_groups[0]

        if 'tcp' in protocols:
            node.ec2.conn.authorize_security_group(group_id=group.id, ip_protocol='tcp', 
            from_port=1,to_port=65535, cidr_ip='0.0.0.0/0')
        
        if 'udp' in protocols:
            node.ec2.conn.authorize_security_group(group_id=group.id, ip_protocol='udp', 
            from_port=1,to_port=65535, cidr_ip='0.0.0.0/0')
        
        if 'icmp' in protocols:
            node.ec2.conn.authorize_security_group(group_id=group.id, ip_protocol='icmp', 
            from_port=-1,to_port=-1, cidr_ip='0.0.0.0/0')
        
                
