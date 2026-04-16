from app.contracts.openapi import get_openapi_schema
from app.contracts.store import save_baseline


def main():
    schema = get_openapi_schema()
    save_baseline(schema)
    print("Baseline OpenAPI saved.")


if __name__ == "__main__":
    main()