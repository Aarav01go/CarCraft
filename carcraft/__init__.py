"""
CarCraft Dealership Suite
Initialization: setup PyMySQL as MySQLdb compatibility bridge and Python 3.14 context copy compatibility.
"""
try:
    import pymysql
    pymysql.version_info = (2, 2, 8, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Python 3.14 compatibility for Django BaseContext.__copy__
try:
    from django.template.context import BaseContext
    def _patched_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        if hasattr(self, 'dicts'):
            duplicate.dicts = self.dicts[:]
        return duplicate
    BaseContext.__copy__ = _patched_context_copy
except Exception:
    pass
