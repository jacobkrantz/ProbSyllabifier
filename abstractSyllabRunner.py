from abc import ABCMeta, abstractmethod

# intention for class: a generic 'run.py' can instantiate each class that
# implements 'AbstractSyllabRunner'. The methods abastracted below can
# in theory be called for any syllab comparator (NIST, CELEX). The 'run.py'
# will be very simple, containing only a menu and calling system to each of
# these classes.
class AbstractSyllabRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def trainHMM(self):
        pass

    @abstractmethod
    def testHMM(self):
        pass

    @abstractmethod
    def compareResults(self):
        pass
