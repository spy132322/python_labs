## ЛАБА 07
### pyproject.toml
```toml
[project]
name = "lab07-tests"
version = "0.1.0"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["libs"]

[project.optional-dependencies]
dev = [
"pytest>=8.0",
"pytest-cov>=4.0",
"black>=24.0",
"ruff>=0.6",
]


[tool.black]
line-length = 88
target-version = ["py311"]


[tool.pytest.ini_options]
minversion = "7.0"
addopts = "--strict-markers --maxfail=1"
```

### Сборка пакета

![Compile](/labs/lab07/images/p1.jpg)

### pip list

![List](/labs/lab07/images/p2.png)

### black

![black](/labs/lab07/images/p3.png)

### cover me

![cov](/labs/lab07/images/p4.png)
