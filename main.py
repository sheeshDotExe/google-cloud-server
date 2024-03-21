from pong_server import Server


def main() -> None:
    Server(port=443).run()


if __name__ == "__main__":
    main()
