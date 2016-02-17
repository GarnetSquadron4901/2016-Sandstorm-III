import Pyro4
import sys

ledService = Pyro4.Proxy('PYRONAME:ledService')
ledService.run()