import os
import subprocess

class RsyncScheduler():
    # sync download according 
    """
    threshold: unit in bytes
    """
    def __init__(self, schedule_size_threshold, shareconfig, serverconfig):
        # self.buffered_syncsize = 0
        self.schedule_size_threshold = schedule_size_threshold
        self.__buffered_syncsize = 0
        self.selected_server = self.initialize_server(serverconfig)
        self.share_config = shareconfig
        print(self.selected_server)
        self.upsync()

    def upsync(self):
        selected_server = self.selected_server
        server_storage_root = selected_server["server-storage-root"]
        server_login_user = selected_server["login-user"]
        server_ip = selected_server["server-ip"]
        server_port = selected_server["server-port"]
        local_folder = self.share_config['local-path']
        cmd = 'rsync -av --stats --delete -e \
                "ssh -p %s" %s \
                %s@%s:%s \
                --exclude=.DS_Store' % (
                        server_port, self._processed(local_folder),
                        server_login_user, server_ip,
                        self._processed(server_storage_root))
        print(cmd)
        # return
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        ## Wait for cmd to terminate. Get return returncode ##
        p_status = p.wait()
        output_str = output.decode('utf-8')
        print(output.decode('utf-8'))
        print(err)
        print(p_status)

    def update_syncsize(self, size):
        # self.buffered_syncsize = self.buffered_sync + size
        self.__buffered_syncsize += size
        if self.__buffered_syncsize > self.schedule_size_threshold:
            # schedule and update
            self.__buffered_syncsize = 0
            self.schedule_upsync()

    def check_remote_status():
        # TODO:
        # ping remote server, check if it's online
        os.system('ping %s -c 1 -t 10')

    def initialize_server(self, serverconfig):
        print("initializing server")
        server_ips = serverconfig["server-optional-ip"]
        server_storage_root = serverconfig["server-storage-root"]
        server_login_user = serverconfig["login-user"]

        def testdir(username, ip, port, dirname):
            cmd_return_val = os.system('ssh %s@%s -p %s "ls %s"' %
                    (username, ip, port, self._processed(dirname)))
            if cmd_return_val == 0:
                return True
            else:
                return False

        for server_ip in server_ips:
            print("testing %s" % server_ip)
            if ':' not in server_ip:
                port = '22'
                ip = server_ip
            else:
                ip, port = server_ip.split(':')

            if testdir(server_login_user, ip, port, server_storage_root):
                selected_config_template = serverconfig.copy()
                selected_config_template.pop('server-optional-ip')
                selected_config_template['server-ip'] = ip
                selected_config_template['server-port'] = port
                return selected_config_template

        return None

    def _processed(self, dirname):
        space_padded_dirname = dirname.replace(' ', '\ ')
        if space_padded_dirname[-1] == '/':
            return space_padded_dirname[:-1]
        else:
            return space_padded_dirname

    def schedule_upsync(self):
        # TODO: implememnt
        print("upsync scheduled")

    @property
    def buffered_syncsize(self):
        return self.__buffered_syncsize
