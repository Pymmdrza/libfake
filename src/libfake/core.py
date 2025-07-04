import os
import random
from typing import List, Optional

from .exceptions import DataFileError
from .formats import DEFAULT_EMAIL_PROVIDERS, DEFAULT_EMAIL_FORMATS


class FakeName:
    """
    A professional, singleton-based generator for realistic names and emails.

    This class is designed for high performance and configurability. It loads
    name data from files once and provides a simple API to generate synthetic data.
    """
    _instance: Optional['FakeName'] = None

    def __new__(cls, *args, **kwargs):
        force_reload = kwargs.get("force_reload", False)
        if cls._instance is None or force_reload:
            cls._instance = super(FakeName, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 first_names_path: Optional[str] = None,
                 surnames_path: Optional[str] = None,
                 email_providers: Optional[List[str]] = None,
                 email_formats: Optional[List[str]] = None,
                 force_reload: bool = False):
        """
        Initializes the FakeName instance.

        On first instantiation, it loads data. Subsequent calls return the
        existing instance unless `force_reload=True`.

        Args:
            first_names_path (Optional[str]): Path to a custom first names file.
            surnames_path (Optional[str]): Path to a custom surnames file.
            email_providers (Optional[List[str]]): A list of email provider domains.
            email_formats (Optional[List[str]]): A list of f-string-like email formats.
            force_reload (bool): If True, forces re-initialization.
        """
        # The hasattr check prevents re-initialization on subsequent calls
        # to the same singleton instance, unless force_reload is True.
        if hasattr(self, '_initialized') and not force_reload:
            return

        self._base_dir = os.path.dirname(os.path.abspath(__file__))

        f_path = first_names_path or os.path.join(self._base_dir, "data", "NAMES.DIC")
        s_path = surnames_path or os.path.join(self._base_dir, "data", "SURNAMES.DIC")

        self.first_names: List[str] = self._load_file(f_path)
        self.surnames: List[str] = self._load_file(s_path)

        self.email_providers: List[str] = email_providers or DEFAULT_EMAIL_PROVIDERS
        self.email_formats: List[str] = email_formats or DEFAULT_EMAIL_FORMATS
        self._initialized = True

    @staticmethod
    def _load_file(file_path: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except (IOError, FileNotFoundError) as e:
            raise DataFileError(path=file_path) from e

    @staticmethod
    def _clean_for_email(text: str) -> str:
        # ''.join(filter(str.isalnum, text)).lower()
        safe_chars = [char for char in text if char.isalnum()]
        return "".join(safe_chars).lower()

    def get_firstname(self) -> str:
        """Returns a random first name from the loaded list."""
        if not self.first_names:
            raise ValueError("First names list is empty.")
        return random.choice(self.first_names)

    def get_surname(self) -> str:
        """Returns a random surname from the loaded list."""
        if not self.surnames:
            raise ValueError("Surnames list is empty.")
        return random.choice(self.surnames)

    def get_full_name(self) -> str:
        """Generates a random full name."""
        return f"{self.get_firstname()} {self.get_surname()}"

    def generate_email(self, first_name: Optional[str] = None, surname: Optional[str] = None) -> str:
        """
        Generates a realistic email address.

        If names are not provided, random ones are used.
        """
        first = first_name or self.get_firstname()
        last = surname or self.get_surname()

        if not all([first, last, self.email_providers, self.email_formats]):
            raise ValueError("Missing data for email generation (names, providers, or formats).")

        clean_first = self._clean_for_email(first)
        clean_last = self._clean_for_email(last)

        context = {
            "first": clean_first,
            "last": clean_last,
            "f_initial": clean_first[0] if clean_first else '',
            "l_initial": clean_last[0] if clean_last else '',
            "provider": random.choice(self.email_providers),
            "year": random.randint(1980, 2015),
            "num": random.randint(1, 999)
        }

        chosen_format = random.choice(self.email_formats)
        return chosen_format.format(**context)

    def get_details(self, first_name: Optional[str] = None, surname: Optional[str] = None, provider: Optional[str] = None) -> dict:
        """
        Returns a dictionary with full name and email details.

        Args:
            first_name (Optional[str]): First name to use. If None, a random one is generated.
            surname (Optional[str]): Surname to use. If None, a random one is generated.
            provider (Optional[str]): Email provider to use. If None, a random one is chosen.

        Returns:
            dict: Contains 'first_name' and 'surname' , 'full_name' and 'email'.
            :param first_name:
            :param surname:
            :param provider:
        """
        first_name = first_name or self.get_firstname()
        surname = surname or self.get_surname()
        email = self.generate_email(first_name=first_name, surname=surname) if not provider else f"{first_name}.{surname}@{provider}"
        return {
            "first_name": first_name,
            "surname": surname,
            "full_name": f"{first_name} {surname}",
            "email": email
        }
