from app.contracts.openapi import get_openapi_schema


def test_openapi_generation():
    schema = get_openapi_schema()

    assert "openapi" in schema
    assert "paths" in schema