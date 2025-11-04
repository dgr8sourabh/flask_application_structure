from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os
import urllib

is_local = os.environ.get("ENV") == "local"
Base = declarative_base()


def get_connection_string(db_name):
    # db_type = os.getenv(f"{db_name}_DB_TYPE")
    # server = os.getenv(f"{db_name}_DB_SERVER")
    # database = os.getenv(f"{db_name}_DB_DATABASE")
    # username = os.getenv(f"{db_name}_DB_USERNAME", "")
    # password = os.getenv(f"{db_name}_DB_PASSWORD", "")
    # driver = os.getenv(f"{db_name}_DB_DRIVER")
    #
    # if not is_local:
    #     params = urllib.parse.quote_plus(
    #         f"Driver={driver};"
    #         f"Server=tcp:{server},1433;"
    #         f"Database={database};"
    #         f"TrustServerCertificate=no;"
    #         f"Connection Timeout=30;"
    #         f"Authentication=ActiveDirectoryMsi"
    #     )
    # else:
    #     params = urllib.parse.quote_plus(
    #         f"Driver={driver};"
    #         f"Server=tcp:{server},1433;"
    #         f"Database={database};"
    #         f"TrustServerCertificate=no;"
    #         f"Connection Timeout=30;"
    #         f"Uid={username};"
    #         f"Pwd={password}"
    #     )

    # connection_string = f"{db_type}+pyodbc:///?odbc_connect={params}"
    connection_string = f"sqlite:///E:\\Project_Folder\\flask_application_structure\\local_database.db"
    return connection_string


def create_engine_session(db_name):
    engine = create_engine(
        get_connection_string(db_name),
        # fast_executemany=True,
        pool_size=10,
        max_overflow=20,
    )
    session = scoped_session(
        sessionmaker(bind=engine)
    )  # creating a configured "session" class & an instance
    Base.metadata.create_all(engine)
    return engine, session


def get_engine(db_name):
    engine_obj, _ = create_engine_session(db_name)
    return engine_obj


def get_session(db_name):
    _, session = create_engine_session(db_name)
    return session


@contextmanager
def session_scope(db_name):
    session = get_session(db_name)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.remove()
        session.close()
