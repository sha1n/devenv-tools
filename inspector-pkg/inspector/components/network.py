import urllib.request as request
from collections import namedtuple
from time import time
from typing import List

from inspector.api.collector import Collector
from inspector.api.context import Context

NetConnectivityInfo = namedtuple(typename="NetConnectivityInfo", field_names=["address", "ok", "time"])


class NetworkConnectivityInfoCollector(Collector):

    def __init__(self, ctx: Context):
        super().__init__(ctx)
        # fixme shai: get url list from configuration
        self._addresses = ["http://www.google.com"]

    def collect(self) -> List[NetConnectivityInfo]:
        return list((self._check_connectivity(address) for address in self._addresses))

    def _check_connectivity(self, address):
        try:
            self.ctx.logger.log("Checking connectivity to {}".format(address))
            start_time = time()
            request.urlopen(address, timeout=10)
            end_time = time()
            return NetConnectivityInfo(address=address, ok=True, time=end_time - start_time)
        except request.URLError:
            return NetConnectivityInfo(address=address, ok=False, time=-1)
