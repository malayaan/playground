[tool.black]
line-length = 300
exclude = '''
/(
    \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | site-packages
)/
'''