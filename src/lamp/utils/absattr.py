from abc import ABCMeta, abstractproperty, abstractmethod


class AbsAttrPassThrough(object):
    __metaclass__ = ABCMeta

    _PASS_THROUGH_ATTRS = []

    def __getattr__(self, attr):
        if attr in self._PASS_THROUGH_ATTRS:
            try:
                return getattr(self._datasource, attr)
            except AttributeError as e:
                raise e
        else:
            raise AttributeError('class %s does not have attr: %s' % (self.__class__, attr))

    @abstractproperty
    def _datasource(self):
        pass
