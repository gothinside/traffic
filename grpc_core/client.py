import grpc

from grpc_core.protos import service_pb2_grpc
from settings import GRPC_HOST, GRPC_PORT

async def get_grpc_traffic_client():
    channel = grpc.aio.insecure_channel(f'{GRPC_HOST}:{GRPC_PORT}')
    client = service_pb2_grpc.TrafficStub(channel)
    return client