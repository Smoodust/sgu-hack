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
                "description": "Возвращает список всех доступных логов",
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
                                                "type": "object"
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
                "description": "Возвращает конкретный лог по его идентификатору",
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
                                            "type": "object"
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
                "summary": "Получить все графики",
                "description": "Возвращает список всех доступных графиков",
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
                                                "type": "object"
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
        "/graphs/period": {
            "post": {
                "summary": "Получить графики за период",
                "description": "Возвращает графики за указанный временной период",
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
                                                "type": "object"
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
                "description": "Возвращает графики для указанного пакета",
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
                                                "type": "object"
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
                "description": "Возвращает графики для указанного пакета за определенный период",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "package": {
                                        "type": "string"
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
                                                "type": "object"
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
                "description": "Анализирует лог с помощью AI и возвращает подозрительные строки",
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
                                        "log": {
                                            "type": "string",
                                            "description": "Содержимое лога"
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
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
