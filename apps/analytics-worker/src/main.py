import asyncio
import json
import logging

import asyncpg
import boto3

from src.config import settings
from src.models import ClickEvent
from src.processor import process

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def get_sqs_client():
    return boto3.client(
        "sqs",
        endpoint_url=settings.sqs_endpoint,
        region_name=settings.aws_default_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


async def run():
    db = await asyncpg.connect(settings.database_url)
    sqs = get_sqs_client()
    log.info("analytics-worker started")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=settings.sqs_queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=settings.poll_wait_seconds,
            )
            messages = response.get("Messages", [])

            for msg in messages:
                try:
                    data = json.loads(msg["Body"])
                    event = ClickEvent.from_dict(data)
                    await process(event, db)
                    sqs.delete_message(
                        QueueUrl=settings.sqs_queue_url,
                        ReceiptHandle=msg["ReceiptHandle"],
                    )
                    log.info("processed click", extra={"short_code": event.short_code})
                except Exception as e:
                    log.error("failed to process message", extra={"error": str(e)})

        except Exception as e:
            log.error("sqs poll error", extra={"error": str(e)})
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(run())
