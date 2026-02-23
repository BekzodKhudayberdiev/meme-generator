class QuoteModel:
    """A quote with a body and an author."""

    def __init__(self, body: str, author: str) -> None:
        self.body = body
        self.author = author

    def __str__(self) -> str:
        return f'"{self.body}" - {self.author}'

    def __repr__(self) -> str:
        return f'QuoteModel(body={self.body!r}, author={self.author!r})'
