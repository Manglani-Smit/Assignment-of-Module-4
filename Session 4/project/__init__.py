import pymysql
pymysql.install_as_MySQLdb()

# 1. Version check bypass
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.check_database_version_supported = lambda self: None

# 2. RETURNING syntax error fix (MariaDB 10.4 compatibility)
from django.db.backends.mysql.features import DatabaseFeatures
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)