from dotenv import load_dotenv
from pathlib import Path
import typing


def load_dotenv_if_available(file_path: typing.Optional[str] = None):
    env_file_path = file_path or Path(__file__).parent / ".env"
    load_dotenv(env_file_path)
