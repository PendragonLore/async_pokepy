def _fmt_param(thing: str) -> str:
    return "-".join(thing.lower().split())


def _pretty_format(thing: str) -> str:
    if thing.lower() in ("oh-ho", "porygon-z"):
        return thing.capitalize()
    return thing.replace("-", " ").title()
