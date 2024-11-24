import grpc

from grpc_core.protos import service_pb2_grpc

async def get_grpc_traffic_client():
    channel = grpc.aio.insecure_channel('localhost:50051')
    client = service_pb2_grpc.TrafficStub(channel)
    return client