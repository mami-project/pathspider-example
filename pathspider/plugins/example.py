import sys
import collections
import logging

from pathspider.base import SynchronizedSpider
from pathspider.base import PluggableSpider
from pathspider.base import NO_FLOW

from pathspider.observer import simple_observer

Connection = collections.namedtuple("Connection", ["host", "state"])
SpiderRecord = collections.namedtuple("SpiderRecord", ["ip", "rport", "port",
                                                       "host", "config",
                                                       "connstate"])

class Example(SynchronizedSpider, PluggableSpider):

    """
    An example PATHspider plugin.
    """

    def config_zero(self):
        logger = logging.getLogger("example")
        logger.debug("Configuration zero")

    def config_one(self):
        logger = logging.getLogger("example")
        logger.debug("Configuration one")

    def connect(self, job, pcs, config):
        sock = tcp_connect(job)
        return Connection(sock, 1)

    def post_connect(self, job, conn, pcs, config):
        rec = SpiderRecord(job[0], job[1], job[2], config, True)
        return rec

    def create_observer(self):
        logger = logging.getLogger("example")
        try:
            return simple_observer()
        except:
            logger.error("Observer would not start")
            sys.exit(-1)

    def merge(self, flow, res):
        if flow == NO_FLOW:
            flow = {"dip": res.ip,
                    "sp": res.port,
                    "dp": res.rport,
                    "observed": False}
        else:
            flow['observed'] = True

        self.outqueue.put(flow)

    @staticmethod
    def register_args(subparsers):
        parser = subparsers.add_parser('example', help="Example starting point for development")
        parser.set_defaults(spider=Example)
