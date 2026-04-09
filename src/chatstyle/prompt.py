from __future__ import annotations

import click


def ask_text(message: str, *, default: str = "", password: bool = False):
    return click.prompt(
        message,
        default=default,
        show_default=bool(default),
        hide_input=password,
        err=True,
    )


def ask_path(message: str, *, default: str = ""):
    return click.prompt(
        message,
        default=default,
        show_default=bool(default),
        type=click.Path(),
        err=True,
    )


def ask_confirm(message: str, *, default: bool = True):
    return click.confirm(message, default=default, err=True)


def ask_select(message: str, choices: list[str]):
    if not choices:
        raise click.ClickException("No choices available for selection.")

    try:
        import questionary
    except ImportError:
        for index, choice in enumerate(choices, start=1):
            click.echo(f"  {index}. {choice}", err=True)
        selected_index = click.prompt(
            message,
            type=click.IntRange(1, len(choices)),
            show_choices=False,
            err=True,
        )
        return choices[selected_index - 1]

    selected = questionary.select(
        message,
        choices=choices,
        qmark="",
        pointer=">",
        use_arrow_keys=True,
        use_jk_keys=True,
        instruction="",
    ).ask()
    if selected is None:
        raise click.Abort()
    return selected
