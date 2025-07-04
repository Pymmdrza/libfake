DEFAULT_EMAIL_PROVIDERS = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com",
    "icloud.com", "aol.com", "mail.com", "protonmail.com"
]

# These formats will be populated with a context dictionary
# Available keys: {first}, {last}, {f_initial}, {l_initial}, {year}, {num}
DEFAULT_EMAIL_FORMATS = [
    "{first}.{last}@{provider}",
    "{first}{last}{num}@{provider}",
    "{f_initial}{last}@{provider}",
    "{first}_{last}@{provider}",
    "{last}{num}@{provider}",
    "{first}.{l_initial}{year}@{provider}",
]
