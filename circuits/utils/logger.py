from colorama import Fore, Style


class Logger:
    LEVELS = (
        "INFO",
        "ERRO",
        "DEBG",
        "WARN",
    )
    LEVEL_COLORS = {
        "INFO": Fore.GREEN,
        "ERRO": Fore.RED,
        "DEBG": Fore.BLUE,
        "WARN": Fore.YELLOW,
    }

    def __init__(self, format_skel: str = None):
        self.__origins = []
        self.__origins_offset = 0

        self.__streams = []
        self.__streams_offset = 0

        self.__level_offset = max(len(x) for x in self.LEVELS)

        self.__format_skel = (
            format_skel
            or f"{Style.DIM}{'[{}]'}{Style.RESET_ALL} {'{}{}'}{Fore.RESET} - {'{} : {}'}"
        )

    def log(
        self,
        stream: str,
        content: str,
        level: str = "INFO",
        *,
        origin: str = "No Origin",
    ):
        if origin not in self.__origins:
            self.register_origin(origin)

        print(
            self.__format_skel.format(
                origin.center(self.__origins_offset),
                self.LEVEL_COLORS.get(level),
                level.ljust(self.__level_offset),
                stream.ljust(self.__streams_offset),
                content,
            )
        )

    def get_logger(self, stream: str):
        self.register_stream(stream)
        return lambda *x, **y: self.log(stream, *x, **y)

    def register_origin(self, origin: str):
        self.__origins.append(origin)
        self.__origins_offset = max(len(x) for x in self.__origins)

    def register_stream(self, stream: str):
        self.__streams.append(stream)
        self.__streams_offset = max(len(x) for x in self.__streams)
