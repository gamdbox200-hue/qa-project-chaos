POST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "number"}
    },
    "required": ["id", "title", "userId"] # Поля, которые должны быть обязательно
}