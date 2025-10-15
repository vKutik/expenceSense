"""
Observer Pattern for Real-time Updates
Simple event system for notifying components of changes
"""
from typing import List, Callable, Dict, Any
from abc import ABC, abstractmethod
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Observer(ABC):
    """Abstract observer interface"""
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Update method called when event occurs"""
        pass


class Event:
    """Simple event class"""
    
    def __init__(self, event_type: str, data: Dict[str, Any], timestamp: str = None):
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or datetime.now().isoformat()


class EventManager:
    """Simple event manager for observer pattern"""
    
    def __init__(self):
        self._observers: Dict[str, List[Observer]] = {}
        self._event_history: List[Event] = []
    
    def subscribe(self, event_type: str, observer: Observer) -> None:
        """Subscribe observer to event type"""
        if event_type not in self._observers:
            self._observers[event_type] = []
        
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)
            logger.info(f"Observer subscribed to {event_type}")
    
    def unsubscribe(self, event_type: str, observer: Observer) -> None:
        """Unsubscribe observer from event type"""
        if event_type in self._observers:
            try:
                self._observers[event_type].remove(observer)
                logger.info(f"Observer unsubscribed from {event_type}")
            except ValueError:
                pass
    
    def notify(self, event: Event) -> None:
        """Notify all observers of an event"""
        event_type = event.event_type
        
        # Store event in history
        self._event_history.append(event)
        
        # Notify observers
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                try:
                    observer.update(event_type, event.data)
                except Exception as e:
                    logger.error(f"Error notifying observer: {e}")
        
        logger.info(f"Event {event_type} notified to {len(self._observers.get(event_type, []))} observers")
    
    def get_event_history(self, event_type: str = None) -> List[Event]:
        """Get event history, optionally filtered by type"""
        if event_type:
            return [event for event in self._event_history if event.event_type == event_type]
        return self._event_history.copy()


class ExpenseObserver(Observer):
    """Observer for expense-related events"""
    
    def __init__(self, name: str = "ExpenseObserver"):
        self.name = name
        self.notifications = []
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle expense events"""
        notification = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data,
            'observer': self.name
        }
        self.notifications.append(notification)
        
        # Log specific events
        if event_type == 'expense_created':
            logger.info(f"{self.name}: New expense created for user {data.get('user_id')}")
        elif event_type == 'expense_deleted':
            logger.info(f"{self.name}: Expense {data.get('expense_id')} deleted")
        elif event_type == 'user_created':
            logger.info(f"{self.name}: New user {data.get('user_id')} registered")


class StatisticsObserver(Observer):
    """Observer for statistics updates"""
    
    def __init__(self, name: str = "StatisticsObserver"):
        self.name = name
        self.last_update = None
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Handle statistics events"""
        self.last_update = datetime.now().isoformat()
        
        if event_type in ['expense_created', 'expense_deleted']:
            logger.info(f"{self.name}: Statistics need update for user {data.get('user_id')}")


class LoggingObserver(Observer):
    """Observer for logging all events"""
    
    def __init__(self, name: str = "LoggingObserver"):
        self.name = name
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log all events"""
        logger.info(f"{self.name}: Event {event_type} - {data}")


class NotificationObserver(Observer):
    """Observer for sending notifications"""
    
    def __init__(self, name: str = "NotificationObserver"):
        self.name = name
        self.notifications_sent = 0
    
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """Send notifications for important events"""
        if event_type == 'expense_created':
            amount = data.get('amount', 0)
            if amount > 1000:  # Notify for large expenses
                self._send_high_expense_notification(data)
                self.notifications_sent += 1
        elif event_type == 'user_created':
            self._send_welcome_notification(data)
            self.notifications_sent += 1
    
    def _send_high_expense_notification(self, data: Dict[str, Any]) -> None:
        """Send notification for high expense"""
        logger.info(f"{self.name}: High expense alert - ${data.get('amount')} for user {data.get('user_id')}")
    
    def _send_welcome_notification(self, data: Dict[str, Any]) -> None:
        """Send welcome notification"""
        logger.info(f"{self.name}: Welcome notification sent to user {data.get('user_id')}")


# Global event manager instance
event_manager = EventManager()

# Initialize default observers
expense_observer = ExpenseObserver()
statistics_observer = StatisticsObserver()
logging_observer = LoggingObserver()
notification_observer = NotificationObserver()

# Subscribe observers to events
event_manager.subscribe('expense_created', expense_observer)
event_manager.subscribe('expense_deleted', expense_observer)
event_manager.subscribe('user_created', expense_observer)

event_manager.subscribe('expense_created', statistics_observer)
event_manager.subscribe('expense_deleted', statistics_observer)

event_manager.subscribe('expense_created', logging_observer)
event_manager.subscribe('expense_deleted', logging_observer)
event_manager.subscribe('user_created', logging_observer)

event_manager.subscribe('expense_created', notification_observer)
event_manager.subscribe('user_created', notification_observer)


def emit_event(event_type: str, data: Dict[str, Any]) -> None:
    """Convenience function to emit events"""
    event = Event(event_type, data)
    event_manager.notify(event)


def get_event_history(event_type: str = None) -> List[Event]:
    """Convenience function to get event history"""
    return event_manager.get_event_history(event_type)
