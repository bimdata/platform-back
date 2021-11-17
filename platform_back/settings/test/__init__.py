from split_settings.tools import include

_base_settings = [
    "../platform_back/components/common.py",
    "../platform_back/components/swagger.py",
    "./*.py",
]

# Include settings:
include(*_base_settings)
