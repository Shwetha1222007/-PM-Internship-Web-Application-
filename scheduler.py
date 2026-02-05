"""
Background Scheduler for PM Internship Scheme
Runs periodic checks for expired selections and automatic promotions
"""

import schedule
import time
import threading
from auto_status_manager import run_status_check
from ai_auto_selector import process_all_companies
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
        
        # Schedule the status check to run every hour (for 48-hour deadline monitoring)
        schedule.every(1).hours.do(run_status_check)
        
        # Schedule AI processing to run every 30 minutes (for new applications)
        schedule.every(30).minutes.do(self._safe_ai_process)
        
        # Run AI processing immediately on startup
        self._safe_ai_process()
        
        # Also run status check on startup
        run_status_check()
        
        # Start the scheduler in a background thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info("Background scheduler started - AI processing every 30 min, status check every hour")
    
    def _safe_ai_process(self):
        """Safely run AI processing with error handling"""
        try:
            logger.info("Running scheduled AI processing...")
            process_all_companies()
        except Exception as e:
            logger.error(f"Error in scheduled AI processing: {str(e)}")
    
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
