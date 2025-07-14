# libfake

First name , Surname and Email Fake Mode in Python with Library Fake.

It has happened repeatedly that a programmer wants to create different users in a project for the user parts of his project with fictitious names and emails that are close to reality, for necessary checks or initial presentation, or other similar cases. This library has been created to meet the needs of this category of functions in a specialized way and using standard and optimized Python methods, and all its components are visible as open source.
Using real and existing first and last names, all first and last names are created, and to use a large amount of this information for ease of use and to prevent the consumption of user resources, the required files are optimized and imported as a singleton, which is a trick that increases the speed of creation incomparably, along with other techniques used.

## Install

```bash
pip install libfake
```
in mac or linux use `pip3` : `pip3 install libfake`

---

## Usage

```python
from libfake import FakeName
fake = FakeName()
```

### First Name and Surname

```python
# Random First name
first_name = fake.get_firstname()
# Random Surname
surname = fake.get_surname()
```
### First name , Surname and Email

```python
first_name = fake.get_firstname()
surname = fake.get_surname()
# Generate email From first name and surname.
email = fake.generate_email(first_name, surname)
```

### Random Full Name 

```python
full_name = fake.get_full_name()
```

### Random Email

```python
random_email = fake.generate_email()
```

### Email for a Specific Name

```python
specific_email = fake.generate_email("Alice", "Wonderland")
```

### Custom Provider

```python
provider_custom = "example.com"
# Create a new, custom-configured instance (resets the singleton)
custom_fake = fake.get_details(first_name="Alice", surname="Smith", provider=provider_custom)
# return dict details , if need just email:
custom_email = custom_fake.get('email')
```


## Programmer

Programmer and Owner By : [Pymmdrza](https://github.com/Pymmdrza)
