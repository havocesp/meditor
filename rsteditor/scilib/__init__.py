from .input import _SciImSupport

try:
    from .scilexerrest import QsciLexerRest
    print('[INFO] Use C++ rst lexer')
except Exception:
    from .scilexerrest_py import QsciLexerRest
    print('[INFO] Use PYTHON rst lexer')
