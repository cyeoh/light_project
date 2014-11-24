import re
import telnetlib

class CGateDisconnect(Exception):
    def __init__(self, msg):
        self.msg = msg


class CGate(object):

    def __init__(self, host, host_port, project_name, network_num, default_subnet=56):
        self.host = host
        self.host_port = host_port
        self.project_name = project_name
        self.network_num = network_num
        self.default_subnet = str(default_subnet)
        self.conn = None

    def send_cmd(self, cmd):
        self.conn.write(cmd + '\n')

        # Expect 2xx on success, 4xx otherwise
        ret = self.conn.expect(['\n2\d\d .*', '\n3\d\d .*', '\n4\d\d .*'])

        if ret[0] > 1:
            print "Error running cmd: ", cmd
            raise CGateDisconnect(cmd)

        return ret[2].strip()
        
    def connect(self):
        self.conn = telnetlib.Telnet(self.host, self.host_port)

        ret = self.conn.read_until('201 Service ready:')

        ret = self.send_cmd('project load ' + self.project_name)
        ret = self.send_cmd('project use ' + self.project_name)
        ret = self.send_cmd('net open 254')

    def _create_id(self, id, subnet):
        if subnet:
            return '%(net)/%(subnet)/%(id)s' % {
                'net': self.network_num,
                'subnet': subnet,
                'id': id}
        else:
            return '%(net)s/%(subnet)s/%(id)s' % {
                'net': self.network_num,
                'subnet': self.default_subnet,
                'id': id}

    def on(self, id, subnet=None):
        self.send_cmd('on ' + self._create_id(id, subnet))

    def off(self, id, subnet=None):
        self.send_cmd('off ' + self._create_id(id, subnet))

    def level(self, id, subnet=None):
        ret = self.send_cmd('get ' + self._create_id(id, subnet) + ' level')
        m = re.search('level=(\d+)', ret)
        return m.group(1)


class CGateMonitor(object):
    def __init__(self, host, host_port=20025):
        self.host = host
        self.host_port = host_port
        self.conn = None

    def connect(self):
        self.conn = telnetlib.Telnet(self.host, self.host_port)

    def get_next(self):
        "Returns tuple of (id, on|off)"
        re_on = 'lighting on ' + '//\w+/\d+/\d+/\d+'
        re_off = 'lighting off ' + '//\w+/\d+/\d+/\d+'
        re_both = 'lighting (on|off) ' + '//\w+/\d+/\d+/(\d+)'

        
        ret = self.conn.expect([re_on, re_off])

        m = re.search(re_both, ret[2].strip())
        return (m.group(2), m.group(1))
