"""Exercise drift detection, including imported toolkit entries and descriptions."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('check_t3_tools', Path(__file__).resolve().parents[1] / 'scripts/check-t3-tools.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ToolNamesTest(unittest.TestCase):
    def test_definitions_and_removed_names(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            toolkit = root / 'apps/server/src/mcp/toolkits/example'
            toolkit.mkdir(parents=True)
            (toolkit / 'tools.ts').write_text('import { InboxTool } from "./inbox.ts";\nTool.make("task_status", {});')
            (toolkit / 'inbox.ts').write_text('export const InboxTool = Tool.make("t3_issue_inbox", {});')
            skills = root / 'skills'
            skills.mkdir()
            skill = skills / 'SKILL.md'
            skill.write_text('description: Use t3_issue_inbox\nRead `task_status`; `action: "merge_back"`.')
            checker.check(root, skills)
            for missing in ('t3_removed_tool', 'removed_tool'):
                skill.write_text(f'Call `{missing}`.')
                with self.assertRaisesRegex(ValueError, f'Undefined T3 tools: {missing}'):
                    checker.check(root, skills)
            with self.assertRaisesRegex(ValueError, 'No toolkit definitions'):
                checker.check(root / 'absent', skills)


if __name__ == '__main__':
    unittest.main()
