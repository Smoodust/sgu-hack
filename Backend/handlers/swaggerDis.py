from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from datetime import datetime

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="SGU Hackathon 2025",
        description="API для системы мониторинга и анализа логов",
        version="1.0.0",    
        routes=app.routes,
    )

    # Добавляем детальные описания для каждого эндпоинта
    openapi_schema["paths"] = {
        "/logs": {
            "get": {
                "summary": "Получить все логи",
                "description": "Возвращает список всех доступных логов с информацией о времени обновления и времени с последней ошибки",
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "logs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "branch": {"type": "string"},
                                                    "arch": {"type": "string"},
                                                    "name": {"type": "string"},
                                                    "hash": {"type": "string"},
                                                    "version": {"type": "string"},
                                                    "url": {"type": "string"},
                                                    "updated": {"type": "string", "format": "date-time"},
                                                    "tbfs_since": {"type": "string", "format": "date-time"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/logs/{id}": {
            "get": {
                "summary": "Получить лог по ID",
                "description": "Возвращает конкретный лог по его идентификатору с полной информацией",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Идентификатор лога"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "log": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "branch": {"type": "string"},
                                                "arch": {"type": "string"},
                                                "name": {"type": "string"},
                                                "hash": {"type": "string"},
                                                "version": {"type": "string"},
                                                "url": {"type": "string"},
                                                "updated": {"type": "string", "format": "date-time"},
                                                "tbfs_since": {"type": "string", "format": "date-time"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/graphs": {
            "get": {
                "summary": "Графики количества неисправленных пакетов за последний месяц",
                "description": "Возвращает статистику по количеству неисправленных пакетов за последний месяц, включая кластерный анализ",
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "graphs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "time": {"type": "string", "format": "date"},
                                                    "count": {"type": "integer"}
                                                }
                                            },
                                            "description": "Данные для построения графиков"
                                        },
                                        "count_logs": {
                                            "type": "integer",
                                            "description": "Общее количество логов"
                                        },
                                        "graphs_cluster": {
                                            "type": "array",
                                            "items": {
                                                "type": "number"
                                            },
                                            "description": "Данные для кластерного анализа"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/graphs/period": {
            "post": {
                "summary": "Получить графики за период",
                "description": "Возвращает графики за указанный временной период с кластерным анализом",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "startDate": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-03-20:10:00:00"
                                    },
                                    "endDate": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-03-20:11:00:00"
                                    }
                                },
                                "required": ["startDate", "endDate"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "graphs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "time": {"type": "string", "format": "date"},
                                                    "count": {"type": "integer"}
                                                }
                                            }
                                        },
                                        "count_logs": {
                                            "type": "integer"
                                        },
                                        "graphs_cluster": {
                                            "type": "array",
                                            "items": {
                                                "type": "number"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/graphs/package/{package}": {
            "get": {
                "summary": "Получить графики по пакету",
                "description": "Возвращает графики для указанного пакета с кластерным анализом",
                "parameters": [
                    {
                        "name": "package",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Название пакета"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "graphs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "time": {"type": "string", "format": "date"},
                                                    "count": {"type": "integer"}
                                                }
                                            }
                                        },
                                        "count_logs": {
                                            "type": "integer"
                                        },
                                        "graphs_cluster": {
                                            "type": "array",
                                            "items": {
                                                "type": "number"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/graphs/packageANDperiod": {
            "post": {
                "summary": "Получить графики по пакету и периоду",
                "description": "Возвращает графики для указанного пакета за определенный период с кластерным анализом",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "package": {
                                        "type": "string",
                                        "description": "Название пакета"
                                    },
                                    "startDate": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-03-20:10:00:00"
                                    },
                                    "endDate": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-03-20:11:00:00"
                                    }
                                },
                                "required": ["package", "startDate", "endDate"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "graphs": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "time": {"type": "string", "format": "date"},
                                                    "count": {"type": "integer"}
                                                }
                                            }
                                        },
                                        "count_logs": {
                                            "type": "integer"
                                        },
                                        "graphs_cluster": {
                                            "type": "array",
                                            "items": {
                                                "type": "number"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/logs/analyze/{id}": {
            "get": {
                "summary": "Анализ лога",
                "description": "Анализирует лог с помощью AI и возвращает подозрительные строки и результаты анализа",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Идентификатор лога для анализа"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "object",
                                            "description": "Результат анализа лога"
                                        },
                                        "log_url": {
                                            "type": "string",
                                            "description": "URL лога"
                                        },
                                        "badLines": {
                                            "type": "array",
                                            "items": {
                                                "type": "object"
                                            },
                                            "description": "Список подозрительных строк в логе"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Лог не найден"
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        },
        "/clusters/description": {
            "post": {
                "summary": "Получить описание кластеров",
                "description": "Возвращает описание ошибок для указанных кластеров",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "cluster_dict": {
                                        "type": "object",
                                        "description": "Словарь с ID кластеров и их логами"
                                    }
                                },
                                "required": ["cluster_dict"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Успешный ответ",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "result": {
                                            "type": "string",
                                            "description": "Описание ошибок в кластерах"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Внутренняя ошибка сервера"
                    }
                }
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
