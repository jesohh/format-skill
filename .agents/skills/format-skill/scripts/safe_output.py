from pathlib import Path

def new_output(path, source=None):
    if not path:
        raise ValueError("Explicit new output path required (--out for edits)")
    dest = Path(path)
    if dest.exists() or dest.is_symlink():
        raise FileExistsError(f"Refusing to overwrite: {dest}")
    if source and dest.resolve() == Path(source).resolve():
        raise ValueError("Output must differ from input")
    return str(dest)
