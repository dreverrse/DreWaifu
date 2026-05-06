# Health check / monitoring task
import logging
from datetime import datetime
from config import TZ

logger = logging.getLogger(__name__)


async def health_check(context):
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Bot sehat. Waktu: {now}")
