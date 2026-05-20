"""Smoke test: importing the package shouldn't blow up."""


def test_import():
    import haggle  # noqa: F401
