import json
import logging


class DefaultJsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': record.created,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        return json.dumps(log_data)


class DetailedJsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_number": record.lineno,
            "logger_name": record.name,
            "process_name": record.processName,
            "process_id": record.process,
            "thread_name": record.threadName,
            "thread_id": record.thread,
            "extra_info": record.__dict__.get("extra", {}),
        }
        return json.dumps(log_data)
