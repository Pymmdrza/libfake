"""
LibFake Examples - Practical Usage Demonstrations
"""

import json
import subprocess
from libfake import FakeName


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print("=" * 60)


def demo_python_api():
    """Demonstrate Python API usage."""
    print_section("Python API Examples")

    # Initialize the generator
    fake = FakeName()

    print("1. Basic name generation:")
    print(f"   First name: {fake.get_firstname()}")
    print(f"   Surname: {fake.get_surname()}")
    print(f"   Full name: {fake.get_full_name()}")
    print(f"   Email: {fake.generate_email()}")

    print("\n2. Complete profile:")
    profile = fake.get_details()
    print(f"   {json.dumps(profile, indent=2, ensure_ascii=False)}")

    print("\n3. Custom email generation:")
    custom_email = fake.generate_email(first_name="John", surname="Doe")
    print(f"   Custom email: {custom_email}")

    print("\n4. Bulk generation:")
    print("   Five random profiles:")
    for i in range(5):
        profile = fake.get_details()
        print(f"   {i+1}. {profile['full_name']} <{profile['email']}>")


def demo_cli_commands():
    """Demonstrate CLI usage."""
    print_section("Command Line Interface Examples")

    commands = [
        ("Basic first name", "python -m libfake --firstname"),
        ("Basic surname", "python -m libfake --surname"),
        ("Full name", "python -m libfake --fullname"),
        ("Email address", "python -m libfake --email"),
        ("Complete profile", "python -m libfake --generate"),
        ("Multiple names", "python -m libfake --firstname --count 3"),
        ("JSON output", "python -m libfake --details --json"),
        ("Uppercase names", "python -m libfake --fullname --count 2 --uppercase"),
        (
            "Custom separator",
            "python -m libfake --firstname --count 3 --separator ', '",
        ),
        ("Random surprise", "python -m libfake --random --count 2"),
        ("Bulk mixed data", "python -m libfake --bulk --count 3"),
    ]

    for description, command in commands:
        print(f"\n{description}:")
        print(f"Command: {command}")
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                # Limit output length for display
                if len(output) > 200:
                    output = output[:200] + "..."
                print(f"Output: {output}")
            else:
                print(f"Error: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print("Error: Command timed out")
        except Exception as e:
            print(f"Error: {e}")


def demo_advanced_usage():
    """Demonstrate advanced usage scenarios."""
    print_section("Advanced Usage Examples")

    fake = FakeName()

    print("1. Database population simulation:")
    users = []
    for i in range(5):
        user = fake.get_details()
        user["id"] = i + 1
        user["username"] = user["email"].split("@")[0]
        users.append(user)

    print("   Sample user records:")
    for user in users[:3]:
        print(f"   ID: {user['id']}, Name: {user['full_name']}, Email: {user['email']}")

    print("\n2. Test data for different scenarios:")
    scenarios = [
        "User registration testing",
        "Email validation testing",
        "Name formatting testing",
        "Database stress testing",
        "API endpoint testing",
    ]

    for scenario in scenarios:
        profile = fake.get_details()
        print(f"   {scenario}: {profile['full_name']} ({profile['email']})")

    print("\n3. Different email formats:")
    for i in range(3):
        email = fake.generate_email()
        print(f"   Generated email {i+1}: {email}")


def main():
    """Main demonstration function."""
    print("LibFake - Comprehensive Usage Examples")
    print("This script demonstrates both Python API and CLI usage")

    try:
        demo_python_api()
        demo_cli_commands()
        demo_advanced_usage()

        print_section("Summary")
        print("LibFake provides flexible fake data generation for:")
        print("• Testing and development")
        print("• Database population")
        print("• API testing")
        print("• User interface mockups")
        print("• Educational purposes")
        print("\nFor more information, run: libfake --help")

    except ImportError:
        print("Error: LibFake is not installed.")
        print("Please install it first with: pip install -e .")
    except Exception as e:
        print(f"Error during demonstration: {e}")


if __name__ == "__main__":
    main()
