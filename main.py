from uvicorn import run


def main():
    print("Hello from fast-api-uv!")
    run("web.app:app", reload=True)


if __name__ == "__main__":
    main()
