import typing

from aiser.identifiable_entities import IdentifiableEntity


class IdentifiableGroupValidator:
    @staticmethod
    def group_is_valid(identifiable_entities: typing.List[IdentifiableEntity]) -> bool:
        if len(identifiable_entities) == 1:
            return True
        return all(entity.get_id() is not None for entity in identifiable_entities)

    @staticmethod
    def assert_group_is_valid(identifiable_entities: typing.List[IdentifiableEntity], group_name: str) -> None:
        if not IdentifiableGroupValidator.group_is_valid(identifiable_entities):
            raise ValueError(
                f"{group_name} is not valid. If there are more than a single entity, all of them must have an ID."
            )
