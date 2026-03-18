import logging
import datetime
import functools


from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Callable, Any


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_app_logger(name: str = "convert") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # чтобы не дублировать хендлеры при повторном импорте
        return logger

    logger.setLevel(logging.DEBUG) 
    
    
    log_file = LOG_DIR / "convert.log"

    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",   # каждый день в полночь
        interval=1,
        backupCount=7,     # храним, например, 7 дней
        encoding="utf-8",
    )
    # добавляем суффикс к архивным файлам, например convert.log.20260314
    handler.suffix = "%Y%m%d"

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

logger = get_app_logger("convert")

def log_operation(operation_name: str = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Получаем название операции
            op_name = operation_name or func.__name__
            
            # Получаем текущее время
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Логируем начало операции
            logger.info("[START] %s called args=%s kwargs=%s", op_name, args, kwargs)
            
            # Логируем параметры
            if args:
                logger.debug(f"[{timestamp}] [INPUT] Параметры: {args}")
            if kwargs:
                logger.debug(f"[{timestamp}] [INPUT] Ключевые параметры: {kwargs}")
            
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Логируем успешный результат
                if result is not None:
                    logger.debug(f"[{timestamp}] [SUCCESS] Результат: {result}")
                else:
                    logger.debug(f"[{timestamp}] [SUCCESS] Операция выполнена успешно")
                
                return result
                
            except Exception as e:
                # Логируем ошибку
                logger.error(f"[{timestamp}] [ERROR] Ошибка в операции {op_name}: {str(e)}")
                raise
                
        return wrapper
    return decorator