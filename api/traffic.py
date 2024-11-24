from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from grpc_core.client import get_grpc_traffic_client
from grpc_core.protos import service_pb2
from typing import Optional
from datetime import datetime
import logging
import typing as t
from google.protobuf.json_format import MessageToDict

router = APIRouter(tags = ['traffic'])

@router.get("/traffic/")
async def get_traffic(
    customer_id: Optional[int] = None,
    ip: Optional[str] = None,
    after: Optional[datetime] = None,
    before: Optional[datetime] = None,
    client: t.Any = Depends(get_grpc_traffic_client),
) -> JSONResponse:
    """
    Эндпоинт для получения информации о трафике.

    Параметры:
    - customer_id: ID клиента для фильтрации
    - ip: IP-адрес для фильтрации
    - after: Начальная дата для фильтрации
    - before: Конечная дата для фильтрации

    Возвращает JSON-ответ с данными о трафике или ошибкой.
    """
    before_str = before.strftime("%Y-%m-%d %H:%M:%S") if before else None
    after_str = after.strftime("%Y-%m-%d %H:%M:%S") if after else None

    request = service_pb2.TrafficRequest(
        CustomerID=customer_id, IP=ip, Before=before_str, After=after_str
    )
    try:
        response = await client.GetTraffic(request)
        return JSONResponse(
            MessageToDict(
                response,
                preserving_proto_field_name=True,
                use_integers_for_enums=False,
                always_print_fields_with_no_presence=True
            )
        )
    except Exception as e:
        logging.error(f"Error fetching traffic: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)