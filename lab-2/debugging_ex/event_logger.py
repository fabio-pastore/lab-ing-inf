import datetime
import time
import uuid
import copy

class EventLogger:
    def __init__(self, max_logs=1000, retention_days=30):
        self.events = []
        self.stats = {}
        self.max_logs = max_logs
        self.retention_days = retention_days

    def _remove_old_events(self):
        tmp_list = self.events.copy()
        curr_date = datetime.datetime.now()
        for event in tmp_list:
            if (curr_date - event["timestamp"]).days > self.retention_days:
                self.events.remove(event)
    
    def log_event(self, event, level="INFO", source=None, user=None, details=None,
                        timestamp=None):
        
        if timestamp is None:
            timestamp = datetime.datetime.now() # not as a default argument

        ## added check to remove outdated events before trying to insert a new one
        self._remove_old_events()
        
        ## used to be: self.events.append(event_obj) AFTER object creation. First check if we can add events then create event_obj and append it to the list
        if len(self.events) < self.max_logs:

            event_id = str(uuid.uuid4())
                    
            event_obj = {
                "id": event_id,
                "event": event,
                "level": level.upper(),
                "source": source,
                "user": user,
                "details": copy.deepcopy(details),
                "timestamp": timestamp,
            }

            self.events.append(event_obj)
