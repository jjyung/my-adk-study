import unittest

from agent import get_user_info, set_user_info


class _FakeToolContext:
    def __init__(self):
        self.state = {}


class UserInfoToolsTest(unittest.TestCase):
    def test_get_user_info_returns_fixed_shape_on_empty_state(self):
        tool_context = _FakeToolContext()

        result = get_user_info(tool_context)

        self.assertEqual(result, {"name": None, "occupation": None})

    def test_set_user_info_updates_fields_independently(self):
        tool_context = _FakeToolContext()

        after_name = set_user_info("name", "小明", tool_context)
        after_occupation = set_user_info("occupation", "資料工程師", tool_context)

        self.assertEqual(after_name, {"name": "小明", "occupation": None})
        self.assertEqual(after_occupation, {"name": "小明", "occupation": "資料工程師"})
        self.assertEqual(
            tool_context.state["user:info"], {"name": "小明", "occupation": "資料工程師"}
        )

    def test_set_user_info_rejects_invalid_field(self):
        tool_context = _FakeToolContext()

        with self.assertRaises(ValueError) as ctx:
            set_user_info("company", "OpenAI", tool_context)  # type: ignore[arg-type]

        self.assertIn("Invalid field", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
