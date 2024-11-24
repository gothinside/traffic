import grpc
from concurrent.futures import ThreadPoolExecutor
from grpc import aio
from sqlalchemy import select, func
import grpc_core.protos.service_pb2_grpc as pb2_grpc
import grpc_core.protos.service_pb2 as pb2
from models import Traffic, Customers
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from settings import GRPC_PORT, GRPC_HOST

class TrafficService(pb2_grpc.TrafficServicer):
    """
    Реализация сервиса Traffic, определённого в gRPC-протоколе.
    Этот сервис предоставляет данные о сетевом трафике для клиентов,
    используя асинхронный подход и взаимодействие с базой данных.

    Атрибуты:
        db: Асинхронный контекст для подключения к базе данных.
    """

    def __init__(self, db: sessionmaker[AsyncSession]):
        """
        Конструктор класса TrafficService.

        Параметры:
            db: Асинхронный объект для работы с базой данных (SessionFactory).
        """
        self.db = db

    async def GetTraffic(self, request, context) -> pb2.TrafficResponse:
        """
        Обрабатывает gRPC-запрос для получения данных о суммарном трафике клиентов.

        Параметры:
            request: TrafficRequest — запрос клиента с параметрами фильтрации.
            context: gRPC-контекст запроса.

        Возвращает:
            TrafficResponse — ответ с данными о трафике.
        """
        query = (
            select(Customers.name, func.sum(Traffic.received_traffic))
            .join(Traffic.customer)
        )

        if request.CustomerID:
            query = query.where(Customers.id == request.CustomerID)
        if request.Before:
            query = query.where(Traffic.date < request.Before)
        if request.After:
            query = query.where(Traffic.date > request.After)
        if request.IP:
            query = query.where(Traffic.ip == request.IP)

        async with self.db() as session:
            result = await session.execute(query.group_by(Customers.name))
            traffics = result.fetchall()

        response = [
            pb2.CustomerTrafficInfo(CustomerName=row[0], TrafficsSum=row[1])
            for row in traffics
        ]
        return pb2.TrafficResponse(Traffics=response)


class Server:
    """
    Класс, отвечающий за настройку и запуск gRPC-сервера.

    Атрибуты:
        server: Экземпляр асинхронного gRPC-сервера.
    """

    def __init__(self, db):
        """
        Конструктор класса Server.

        Параметры:
            db: Асинхронный объект для работы с базой данных (SessionFactory).
        """
        self.server = aio.server(ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_TrafficServicer_to_server(TrafficService(db), self.server)
        self.server.add_insecure_port(f'{GRPC_HOST}:{GRPC_PORT}')

    async def serve(self):
        """
        Запускает gRPC-сервер и ожидает завершения.
        """
        await self.server.start()
        print("Server started at localhost:50051")
        await self.server.wait_for_termination()

    async def stop(self):
        """
        Останавливает gRPC-сервер с задержкой для завершения активных запросов.
        """
        await self.server.stop(grace=True)
