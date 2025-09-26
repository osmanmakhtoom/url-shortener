import asyncio
import logging
import signal
from typing import Any

from app.workers.counter_sync_worker import CounterSyncWorker
from app.workers.visit_worker import VisitWorker

logger = logging.getLogger("WorkerManager")


class WorkerManager:
    def __init__(self) -> None:
        self.workers: list[Any] = []
        self.running = True

    async def start(self) -> None:
        """Start all workers."""
        # Initialize workers
        visit_worker = VisitWorker()
        counter_worker = CounterSyncWorker()

        self.workers = [visit_worker, counter_worker]

        # Start workers
        tasks = []
        for worker in self.workers:
            task = asyncio.create_task(self._start_worker(worker))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def _start_worker(self, worker: Any) -> None:
        """Start a single worker with retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await worker.start()
                break
            except Exception as e:
                logger.error(
                    f"Worker {worker.__class__.__name__} attempt {attempt + 1} failed: {e}"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(5 * (attempt + 1))
                else:
                    logger.error(
                        f"Worker {worker.__class__.__name__} failed after {max_retries} attempts"
                    )

    async def stop(self) -> None:
        """Stop all workers gracefully."""
        self.running = False
        logger.info("Stopping workers...")

        for worker in self.workers:
            if hasattr(worker, "stop"):
                await worker.stop()

        logger.info("All workers stopped")


async def main() -> None:
    manager = WorkerManager()

    # Setup signal handlers
    def signal_handler(signum: int, frame: Any) -> None:
        asyncio.create_task(manager.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await manager.start()
    except KeyboardInterrupt:
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())
