from pong_server import Server


def main() -> None:
    Server(port=4444).run()


if __name__ == "__main__":
    main()
