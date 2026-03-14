import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.config import MONGO_COLLECTION, MONGO_DB, MONGO_URI

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:  # pragma: no cover - dependency fallback
    MongoClient = None

    class PyMongoError(Exception):
        pass


class OperationsLogger:
    def __init__(self) -> None:
        self._logger = logging.getLogger("operacoes")
        self._uri = MONGO_URI
        self._db_name = MONGO_DB
        self._collection_name = MONGO_COLLECTION
        self._collection = None

    def _get_collection(self):
        if self._collection is not None:
            return self._collection
        if not self._uri or MongoClient is None:
            return None

        client = MongoClient(self._uri, serverSelectionTimeoutMS=1500)
        self._collection = client[self._db_name][self._collection_name]
        return self._collection

    def log(self, payload: dict) -> None:
        payload["data_hora"] = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()
        collection = self._get_collection()

        if collection is None:
            self._logger.info("operacao=%s payload=%s", payload.get("operacao"), payload)
            return

        try:
            collection.insert_one(payload)
        except PyMongoError as exc:
            self._logger.error("falha_log_mongo=%s payload=%s", str(exc), payload)


operations_logger = OperationsLogger()
