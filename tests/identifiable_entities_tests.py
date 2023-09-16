import unittest

from aiser.identifiable_entities import IdentifiableEntity, IdentifiableGroupValidator


class IdentifiableEntitiesValidatorTestCase(unittest.TestCase):
    def test_multiple_entities_with_ids_are_acceptable(self):
        group = [
            IdentifiableEntity(entity_id="1"),
            IdentifiableEntity(entity_id="2"),
        ]
        self.assertTrue(IdentifiableGroupValidator.group_is_valid(group))

    def test_multiple_entities_with_some_ids_are_not_acceptable(self):
        group = [
            IdentifiableEntity(),
            IdentifiableEntity(entity_id="1"),
            IdentifiableEntity(entity_id="2"),
        ]
        self.assertFalse(IdentifiableGroupValidator.group_is_valid(group))


if __name__ == '__main__':
    unittest.main()
