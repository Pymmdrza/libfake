#!/usr/bin/env python3
"""
Test script to verify CLI functionality
"""

import subprocess
import sys
import json


def run_command(cmd):
    """Run a command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def test_cli_commands():
    """Test various CLI commands."""
    print("Testing LibFake CLI...")
    print("=" * 50)

    # Test help
    print("1. Testing help command:")
    code, out, err = run_command("python -m libfake --help")
    if code == 0:
        print("✓ Help command works")
    else:
        print("✗ Help command failed")
        print(f"Error: {err}")

    # Test first name generation
    print("\n2. Testing first name generation:")
    code, out, err = run_command("python -m libfake --firstname")
    if code == 0 and out:
        print(f"✓ Generated first name: {out}")
    else:
        print("✗ First name generation failed")
        print(f"Error: {err}")

    # Test surname generation
    print("\n3. Testing surname generation:")
    code, out, err = run_command("python -m libfake --surname")
    if code == 0 and out:
        print(f"✓ Generated surname: {out}")
    else:
        print("✗ Surname generation failed")
        print(f"Error: {err}")

    # Test full name generation
    print("\n4. Testing full name generation:")
    code, out, err = run_command("python -m libfake --fullname")
    if code == 0 and out:
        print(f"✓ Generated full name: {out}")
    else:
        print("✗ Full name generation failed")
        print(f"Error: {err}")

    # Test email generation
    print("\n5. Testing email generation:")
    code, out, err = run_command("python -m libfake --email")
    if code == 0 and out:
        print(f"✓ Generated email: {out}")
    else:
        print("✗ Email generation failed")
        print(f"Error: {err}")

    # Test profile generation
    print("\n6. Testing profile generation:")
    code, out, err = run_command("python -m libfake --generate")
    if code == 0 and out:
        print(f"✓ Generated profile: {out}")
    else:
        print("✗ Profile generation failed")
        print(f"Error: {err}")

    # Test JSON output
    print("\n7. Testing JSON output:")
    code, out, err = run_command("python -m libfake --details --json")
    if code == 0 and out:
        try:
            data = json.loads(out)
            print(f"✓ Generated JSON: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print("✗ Invalid JSON output")
            print(f"Output: {out}")
    else:
        print("✗ JSON generation failed")
        print(f"Error: {err}")

    # Test multiple generation
    print("\n8. Testing multiple generation:")
    code, out, err = run_command("python -m libfake --firstname --count 3")
    if code == 0 and out:
        lines = out.split("\n")
        print(f"✓ Generated {len([l for l in lines if l.strip()])} names")
        print(f"Output: {out}")
    else:
        print("✗ Multiple generation failed")
        print(f"Error: {err}")


if __name__ == "__main__":
    test_cli_commands()
