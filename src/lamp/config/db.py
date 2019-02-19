import os

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
database = os.environ['POSTGRES_DB']

DATABASE_CONNECTION_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, password, host, port, database)

