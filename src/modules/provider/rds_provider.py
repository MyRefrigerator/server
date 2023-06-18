from mysql.connector import pooling

# Modules
from src.modules.provider.config_provider import configProvider

rdsProviderconfig = configProvider.rdsConfig
rdsProviderPoolConfig = {
    'host': rdsProviderconfig.HOST,
    'user': rdsProviderconfig.USER,
    'password': rdsProviderconfig.PASSWORD,
    'database': rdsProviderconfig.DATABASE_NAME
}
rds_pool = pooling.MySQLConnectionPool(
    pool_name = "sample",
    pool_size = 10,
    **rdsProviderPoolConfig
)

class RdsProvider():
    
    def get_connection(self) -> pooling.PooledMySQLConnection:
        return rds_pool.get_connection()