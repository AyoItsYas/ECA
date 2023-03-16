class Logger:
    LEVELS = [
        "INFO",
        "ERRR",
        "DEBG",
        "WARN",
    ]

    def __init__(self, format_skel: str = None):
        self.__streams = []
        self.__streams_offset = 0
        self.__level_offset = max(len(x) for x in self.LEVELS)

        self.__format_spec = format_skel or "{} - {} : {}"

    def log(
        self,
        stream: str,
        content: str,
        level: str = "INFO",
    ):
        print(
            self.__format_spec.format(
                level.ljust(self.__level_offset),
                stream.ljust(self.__streams_offset),
                content,
            )
        )

    def get_logger(self, stream: str):
        self.register_stream(stream)
        return lambda *x, **y: self.log(stream, *x, **y)

    def register_stream(self, stream: str):
        self.__streams.append(stream)
        self.__streams_offset = max(len(x) for x in self.__streams)
