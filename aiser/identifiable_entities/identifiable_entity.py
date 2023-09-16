import typing


class IdentifiableEntity:
    def __init__(self, entity_id: typing.Optional[str] = None):
        super().__init__()
        self._id = entity_id

    def accepts_id(self, entity_id: str) -> bool:
        if self._id is None:
            return True
        return self._id == entity_id

    def get_id(self) -> typing.Optional[str]:
        return self._id

