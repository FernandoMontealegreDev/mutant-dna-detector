import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import pymysql

# Load environment variables from .env file if it exists
load_dotenv()

pymysql.install_as_MySQLdb()

# Alembic Config object, access values within the .ini file
config = context.config

# Configure logging based on the config file (if available)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata of models for automatic migration generation
target_metadata = None  # This can be set to your model's Base.metadata

# Construct the database URL from environment variables
db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '26115')}/{os.getenv('DB_NAME')}?ssl-mode=REQUIRED"

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    In offline mode, migrations are generated and run without connecting
    to the database. The SQL commands are written directly to the output.
    """
    context.configure(
        url=db_url,  # Database connection URL
        target_metadata=target_metadata,  # The metadata to use for generating migrations
        literal_binds=True,  # Use literal binds instead of parameterized SQL
        dialect_opts={"paramstyle": "named"},  # Parametrized style for SQL dialect
    )

    with context.begin_transaction():
        # Run migrations and apply them to the offline context
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    In online mode, a direct connection to the database is established
    and migrations are executed against the live database.
    """
    # Create an engine with the provided database URL
    connectable = engine_from_config(
        {"sqlalchemy.url": db_url},  # The database connection URL
        prefix="sqlalchemy.",  # Configuration prefix for SQLAlchemy options
        poolclass=pool.NullPool,  # Use a connection pool with no pooling (for direct connections)
    )

    # Connect to the database and run migrations
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            # Run migrations in the online context
            context.run_migrations()

# Determine the mode (offline or online) and execute the corresponding migration method
if context.is_offline_mode():
    run_migrations_offline()  # Execute migrations offline
else:
    run_migrations_online()  # Execute migrations online