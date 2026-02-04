"""
Background Scheduler for PM Internship Scheme
Runs periodic checks for expired selections and automatic promotions
"""

import schedule
import time
import threading
from auto_status_manager import run_status_check
import logging

logger = logging.getLogger(__name__)


class BackgroundScheduler:
    """
    Background scheduler that runs periodic tasks
    """
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the background scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        
        # Schedule the status check to run every hour
        schedule.every(1).hours.do(run_status_check)
        
        # Also run immediately on startup
        run_status_check()
        
        # Start the scheduler in a background thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info("Background scheduler started - checking every hour")
    
    def _run_scheduler(self):
        """Internal method to run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if there are pending tasks
    
    def stop(self):
        """Stop the background scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Background scheduler stopped")


# Global scheduler instance
_scheduler = None


def get_scheduler():
    """Get or create the global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def start_background_scheduler():
    """Start the background scheduler"""
    scheduler = get_scheduler()
    scheduler.start()


def stop_background_scheduler():
    """Stop the background scheduler"""
    scheduler = get_scheduler()
    scheduler.stop()


if __name__ == "__main__":
    # For testing - run the scheduler
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("Starting background scheduler...")
    print("Press Ctrl+C to stop")
    
    start_background_scheduler()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        stop_background_scheduler()
        print("Scheduler stopped.")
