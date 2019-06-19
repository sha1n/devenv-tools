import urllib.request as request
from collections import namedtuple
from time import time
from typing import List

from inspector.api.collector import Collector
from inspector.api.context import Context
from inspector.api.validator import Validator, ValidationResult, Status
from inspector.util.diag import timeit_if

NetConnectivityInfo = namedtuple(typename="NetConnectivityInfo", field_names=["address", "ok", "time"])


class UrlConnectivityInfoCollector(Collector):

    def __init__(self):
        # fixme shai: get url list from configuration
        self._addresses = ["http://www.google.com"]

    def collect(self, ctx: Context) -> List[NetConnectivityInfo]:
        ctx.logger.progress("Checking network connectivity...")
        return list((self._check_connectivity(address, ctx) for address in self._addresses))

    @timeit_if(more_than_sec=1)
    def _check_connectivity(self, address, ctx):
        try:
            ctx.logger.progress("Checking connectivity to {}".format(address))
            start_time = time()
            request.urlopen(address, timeout=10)
            end_time = time()
            return NetConnectivityInfo(address=address, ok=True, time=end_time - start_time)
        except request.URLError:
            return None


class UrlConnectivityInfoValidator(Validator):
    def validate(self, input_data, ctx: Context) -> ValidationResult:
        if input_data is None:
            ctx.logger.error("Network connectivity check returned no data!")
            return ValidationResult(input_data, Status.ERROR)

        for check in input_data:
            if check.time > 1:
                ctx.logger.warn(
                    "Network connectivity check to {} took over {} seconds".format(check.address, check.time))

        return ValidationResult(input_data, Status.OK)
