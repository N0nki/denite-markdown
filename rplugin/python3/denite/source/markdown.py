import re
from .base import Base

class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'markdown'
        self.kind = 'file'

    def on_init(self, context):
        context['__bufnr'] = str(self.vim.call('bufnr', '%'))

    def gather_candidates(self, context):
        return [self._convert(context, header) for header in self._find_headers()]

    def _convert(self, context, header):
        return {
                'word': header['text'],
                'action__path': self.vim.call('bufname', context['__bufnr']),
                'action__line': header['lnum']
                }

    def _find_headers(self):
        headers = []
        codeblock = r'^`{3,}.*$'
        in_codeblock = False
        for i in range(1, self.vim.call('line', '$') + 1):
            line = self.vim.call('getline', i)
            if re.match(codeblock, line):
                in_codeblock = not in_codeblock
            match = re.match(r'^(#+)\s*(.+)$', line)
            if match and not in_codeblock:
                level = match.group(1)
                text = (len(level) - 1) * '  ' + match.group(2)
                headers.append({
                    'level': level,
                    'text': text,
                    'lnum': i
                    })
        return headers
