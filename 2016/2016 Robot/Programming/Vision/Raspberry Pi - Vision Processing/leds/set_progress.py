import Pyro4
import sys

ledService = Pyro4.Proxy('PYRONAME:ledService')
ledService.setProgress(int(sys.argv[1]))