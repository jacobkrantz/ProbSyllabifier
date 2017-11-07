from abc import ABCMeta, abstractmethod


# intention for class: a generic 'run.py' can instantiate each class that
# implements 'AbstractSyllabRunner'. The methods abstracted below can
# in theory be called for any syllab comparator (NIST, CELEX). The 'run.py'
# will be very simple, containing only a menu and calling system to each of
# these classes.
class AbstractSyllabRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def train_hmm(self):
        pass

    @abstractmethod
    def test_hmm(self):
        pass

    @abstractmethod
    def syllabify(self, observation):
        pass

    @abstractmethod
    def syllabify_file(self, file_in, file_out, comparator):
        pass
