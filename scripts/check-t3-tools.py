#!/usr/bin/env python3
"""Check inline tool references against a T3 checkout's toolkit definitions."""
import re
import sys
from pathlib import Path


def check(checkout, skills):
    tool_files = sorted((checkout / 'apps/server/src/mcp/toolkits').glob('*/tools.ts'))
    if not tool_files:
        raise ValueError(f'No toolkit definitions found in {checkout}')
    defined = set()
    for path in tool_files:
        source = path.read_text()
        defined.update(re.findall(r'Tool\.make\(\s*["\']([^"\']+)["\']', source))
        # Some toolkit entries (including the issue inbox) are imported tools.
        for symbols, module in re.findall(r'import\s*\{([^}]+)\}\s*from\s*["\'](\.[^"\']+)["\']', source):
            imported = path.parent / module
            if imported.is_file():
                for symbol, name in re.findall(r'(\w+)\s*=\s*Tool\.make\(\s*["\']([^"\']+)["\']', imported.read_text()):
                    if symbol in re.findall(r'\b\w+\b', symbols):
                        defined.add(name)
    mentioned = set()
    for path in skills.rglob('*.md'):
        source = path.read_text()
        mentioned.update(re.findall(r'`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`', source))
        mentioned.update(re.findall(r'\b(?:t3|notebook)_[a-z0-9]+(?:_[a-z0-9]+)*\b', source))
    if not mentioned:
        raise ValueError(f'No tool references found in {skills}')
    print('\n'.join(sorted(mentioned)))
    missing = mentioned - defined
    if missing:
        raise ValueError('Undefined T3 tools: ' + ', '.join(sorted(missing)))
    print(f'PASS: {len(mentioned)} T3 tool names checked against {len(tool_files)} toolkit files')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python scripts/check-t3-tools.py /path/to/t3code')
    try:
        check(Path(sys.argv[1]), Path(__file__).resolve().parents[1] / 't3-code-plugin/skills')
    except ValueError as error:
        sys.exit(str(error))
