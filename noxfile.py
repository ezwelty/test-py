"""Nox sessions."""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

# By default, avoid modifying source files with black
nox.options.sessions = "lint", "mypy", "tests"
nox.options.reuse_existing_virtualenvs = True
package = "glimpse"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.8")
def black(session: Session) -> None:
    """Format code with black."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", "--skip-string-normalization", *args)


@nox.session(python=["3.8"])
def lint(session: Session) -> None:
    """Lint code with flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-black",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def tests(session: Session) -> None:
    """Run the test suite and type-check at runtime."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "coverage[toml]", "pytest", "pytest-cov", "typeguard", "xdoctest"
    )
    session.run("pytest", f"--typeguard-packages={package}", "--xdoctest", *args)


@nox.session(python=["3.8"])
def mypy(session: Session) -> None:
    """Type-check with mypy."""
    args = session.posargs or locations
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.8"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest", "pygments")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build documentation with sphinx."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session, "sphinx", "sphinx_rtd_theme", "sphinx_autodoc_typehints"
    )
    session.run("sphinx-build", "docs", "docs/_build")
