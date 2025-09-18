"""
Run all ETL jobs.
"""
import asyncio
from typing import Dict, Any, List
import structlog

from .prices import PricesETL
from .benchmarks import BenchmarksETL
from .tesla_metrics import TeslaMetricsETL

logger = structlog.get_logger()

class ETLRunner:
    """Runner for all ETL jobs."""
    
    def __init__(self):
        self.jobs = [
            PricesETL(),
            BenchmarksETL(),
            TeslaMetricsETL(),
        ]
    
    async def run_all(self, force: bool = False) -> Dict[str, Any]:
        """Run all ETL jobs."""
        logger.info("Starting ETL pipeline")
        
        results = []
        total_start_time = asyncio.get_event_loop().time()
        
        for job in self.jobs:
            if job.should_run(force):
                try:
                    with job:
                        result = await job.run()
                        results.append(result)
                        logger.info(f"ETL job {job.name} completed: {result['status']}")
                except Exception as e:
                    logger.error(f"ETL job {job.name} failed: {e}")
                    results.append({
                        "job_name": job.name,
                        "status": "failed",
                        "error": str(e)
                    })
            else:
                logger.info(f"ETL job {job.name} skipped")
                results.append({
                    "job_name": job.name,
                    "status": "skipped",
                    "reason": "Not scheduled to run"
                })
        
        total_duration = asyncio.get_event_loop().time() - total_start_time
        
        # Summary
        successful = len([r for r in results if r["status"] == "success"])
        failed = len([r for r in results if r["status"] == "failed"])
        skipped = len([r for r in results if r["status"] == "skipped"])
        
        summary = {
            "total_jobs": len(self.jobs),
            "successful": successful,
            "failed": failed,
            "skipped": skipped,
            "total_duration_seconds": total_duration,
            "results": results
        }
        
        logger.info(f"ETL pipeline completed: {successful} successful, {failed} failed, {skipped} skipped")
        
        return summary

async def main():
    """Main function to run ETL jobs."""
    runner = ETLRunner()
    results = await runner.run_all(force=True)
    
    print("ETL Pipeline Results:")
    print(f"Total Jobs: {results['total_jobs']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Duration: {results['total_duration_seconds']:.2f} seconds")
    
    for result in results['results']:
        print(f"\n{result['job_name']}: {result['status']}")
        if result['status'] == 'success':
            print(f"  Loaded: {result['loaded']} records")
            print(f"  Duration: {result['duration_seconds']:.2f} seconds")
        elif result['status'] == 'failed':
            print(f"  Error: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())

