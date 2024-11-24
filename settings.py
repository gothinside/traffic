import os
from dotenv import load_dotenv

load_dotenv()

GRPC_HOST=os.getenv("GRPC_HOST")
GRPC_PORT = os.getenv("GRPC_PORT")

SERVER_HOST=os.getenv("SERVER_HOST")
SERVER_PORT=os.getenv("SERVER_PORT")

DB_URL=os.getenv("DB_URL")