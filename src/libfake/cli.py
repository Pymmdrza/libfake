#!/usr/bin/env python3
"""
Command Line Interface for LibFake
Provides easy access to fake data generation from command line
"""

import argparse
import json
import sys
from typing import Optional, List, Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich import box
from rich.tree import Tree
from rich.align import Align

from .core import FakeName
from .exceptions import DataFileError
from ._version import __version__, __author__, __description__

# Initialize rich console
console = Console()

# Color scheme
COLORS = {
    "primary": "cyan",
    "secondary": "blue",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "info": "magenta",
    "muted": "dim white",
}


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="libfake",
        description="🎭 Generate realistic fake names and emails with style",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
✨ Examples:
  libfake --firstname                    Generate a random first name
  libfake --surname                      Generate a random surname  
  libfake --fullname                     Generate a full name
  libfake --email                        Generate an email address
  libfake --generate                     Generate complete profile (name + email)
  libfake --generate --count 5           Generate 5 profiles
  libfake --firstname --count 10         Generate 10 first names
  libfake --json                         Output in JSON format
  libfake --details                      Get detailed profile information
  libfake --bulk --count 5               Generate 5 random mixed data types
  libfake --random                       Generate random surprise data
  libfake --firstname --uppercase        Generate uppercase first name
  libfake --fullname --separator ", "    Use custom separator for multiple items

🎨 Styling options:
  libfake --generate --theme elegant     Use elegant theme
  libfake --details --no-color           Disable colors
        """,
    )

    # Main generation options
    generation_group = parser.add_mutually_exclusive_group()
    generation_group.add_argument(
        "--firstname",
        "--first",
        action="store_true",
        help="Generate a random first name",
    )
    generation_group.add_argument(
        "--surname", "--last", action="store_true", help="Generate a random surname"
    )
    generation_group.add_argument(
        "--fullname",
        "--full",
        action="store_true",
        help="Generate a full name (first + surname)",
    )
    generation_group.add_argument(
        "--email", action="store_true", help="Generate an email address"
    )
    generation_group.add_argument(
        "--generate",
        "--gen",
        action="store_true",
        help="Generate complete profile (name + email)",
    )
    generation_group.add_argument(
        "--details", action="store_true", help="Get detailed profile information"
    )
    generation_group.add_argument(
        "--bulk",
        action="store_true",
        help="Generate bulk data (names, emails, profiles)",
    )
    generation_group.add_argument(
        "--random", action="store_true", help="Generate random data (surprise me!)"
    )

    # Output options
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of items to generate (default: 1)",
    )
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--separator",
        "-s",
        type=str,
        default="\n",
        help="Separator for multiple outputs (default: newline)",
    )
    parser.add_argument(
        "--uppercase", "-u", action="store_true", help="Convert names to uppercase"
    )
    parser.add_argument(
        "--lowercase", "-l", action="store_true", help="Convert names to lowercase"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Quiet mode - only output the generated data",
    )

    # Styling options
    parser.add_argument(
        "--theme",
        type=str,
        choices=["default", "elegant", "minimal", "colorful"],
        default="default",
        help="Visual theme for output (default: default)",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    parser.add_argument(
        "--no-box", action="store_true", help="Disable box borders around output"
    )

    # Custom input options
    parser.add_argument(
        "--custom-first", type=str, help="Use specific first name for email generation"
    )
    parser.add_argument(
        "--custom-surname", type=str, help="Use specific surname for email generation"
    )
    parser.add_argument(
        "--provider", type=str, help="Use specific email provider (e.g., gmail.com)"
    )

    # Data source options
    parser.add_argument(
        "--first-names-file", type=str, help="Path to custom first names file"
    )
    parser.add_argument(
        "--surnames-file", type=str, help="Path to custom surnames file"
    )

    # Version
    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def generate_data(fake_gen: FakeName, args: argparse.Namespace) -> list:
    """Generate the requested data based on arguments."""
    import random

    results = []

    for _ in range(args.count):
        if args.firstname:
            name = fake_gen.get_firstname()
            results.append(format_case(name, args))
        elif args.surname:
            name = fake_gen.get_surname()
            results.append(format_case(name, args))
        elif args.fullname:
            name = fake_gen.get_full_name()
            results.append(format_case(name, args))
        elif args.email:
            results.append(
                fake_gen.generate_email(
                    first_name=args.custom_first, surname=args.custom_surname
                )
            )
        elif args.generate:
            details = fake_gen.get_details(
                first_name=args.custom_first,
                surname=args.custom_surname,
                provider=args.provider,
            )
            if args.json:
                results.append(details)
            else:
                # Store as dict for table display but also store formatted string option
                details["_display_format"] = "profile"
                name = format_case(details["full_name"], args)
                details["full_name"] = name  # Update with formatted case
                results.append(details)
        elif args.details:
            details = fake_gen.get_details(
                first_name=args.custom_first,
                surname=args.custom_surname,
                provider=args.provider,
            )
            # Apply case formatting to name fields
            details["first_name"] = format_case(details["first_name"], args)
            details["surname"] = format_case(details["surname"], args)
            details["full_name"] = format_case(details["full_name"], args)
            results.append(details)
        elif args.bulk:
            # Generate bulk data (mix of everything)
            data_types = ["firstname", "surname", "fullname", "email", "details"]
            data_type = random.choice(data_types)

            if data_type == "firstname":
                name = fake_gen.get_firstname()
                results.append(format_case(name, args))
            elif data_type == "surname":
                name = fake_gen.get_surname()
                results.append(format_case(name, args))
            elif data_type == "fullname":
                name = fake_gen.get_full_name()
                results.append(format_case(name, args))
            elif data_type == "email":
                results.append(fake_gen.generate_email())
            else:  # details
                details = fake_gen.get_details()
                details["first_name"] = format_case(details["first_name"], args)
                details["surname"] = format_case(details["surname"], args)
                details["full_name"] = format_case(details["full_name"], args)
                results.append(details)
        elif args.random:
            # Random generation - surprise the user!
            options = [
                lambda: format_case(fake_gen.get_firstname(), args),
                lambda: format_case(fake_gen.get_surname(), args),
                lambda: format_case(fake_gen.get_full_name(), args),
                lambda: fake_gen.generate_email(),
                lambda: fake_gen.get_details(),
            ]
            result = random.choice(options)()
            if isinstance(result, dict):
                result["first_name"] = format_case(result["first_name"], args)
                result["surname"] = format_case(result["surname"], args)
                result["full_name"] = format_case(result["full_name"], args)
            results.append(result)
        else:
            # Default behavior - generate a full name
            name = fake_gen.get_full_name()
            results.append(format_case(name, args))

    return results


def format_case(text: str, args: argparse.Namespace) -> str:
    """Apply case formatting to text based on arguments."""
    if args.uppercase:
        return text.upper()
    elif args.lowercase:
        return text.lower()
    return text


def get_theme_colors(theme: str) -> Dict[str, str]:
    """Get color scheme for the specified theme."""
    themes = {
        "default": {
            "primary": "cyan",
            "secondary": "blue",
            "success": "green",
            "accent": "magenta",
        },
        "elegant": {
            "primary": "gold1",
            "secondary": "purple",
            "success": "green3",
            "accent": "deep_pink2",
        },
        "minimal": {
            "primary": "white",
            "secondary": "bright_black",
            "success": "green",
            "accent": "yellow",
        },
        "colorful": {
            "primary": "bright_cyan",
            "secondary": "bright_magenta",
            "success": "bright_green",
            "accent": "bright_yellow",
        },
    }
    return themes.get(theme, themes["default"])


def create_header(title: str, subtitle: str = "", theme: str = "default") -> Panel:
    """Create a styled header panel."""
    colors = get_theme_colors(theme)

    header_text = Text()
    header_text.append("🎭 ", style="bold")
    header_text.append(title, style=f"bold {colors['primary']}")

    if subtitle:
        header_text.append(f"\n{subtitle}", style=f"{colors['secondary']}")

    return Panel(
        Align.center(header_text),
        box=box.DOUBLE,
        border_style=colors["primary"],
        padding=(0, 1),
    )


def create_profile_table(
    profiles: List[Dict], theme: str = "default", show_index: bool = True
) -> Table:
    """Create a styled table for profile data."""
    colors = get_theme_colors(theme)

    table = Table(
        box=box.ROUNDED,
        border_style=colors["secondary"],
        header_style=f"bold {colors['primary']}",
    )

    if show_index:
        table.add_column("ID", style=colors["accent"], justify="center", width=4)
    table.add_column("👤 Name", style=f"bold {colors['success']}", min_width=20)
    table.add_column("📧 Email", style=colors["primary"], min_width=25)

    for i, profile in enumerate(profiles, 1):
        if isinstance(profile, dict):
            name = profile.get("full_name", "Unknown")
            email = profile.get("email", "Unknown")
        else:
            name = str(profile)
            email = "N/A"

        row_data = [name, email]
        if show_index:
            row_data.insert(0, str(i))

        table.add_row(*row_data)

    return table


def create_simple_list(items: List[str], title: str, theme: str = "default") -> Panel:
    """Create a styled list panel."""
    colors = get_theme_colors(theme)

    content = Text()
    for i, item in enumerate(items, 1):
        if i > 1:
            content.append("\n")
        content.append(f"{i:2d}. ", style=colors["accent"])
        content.append(str(item), style=colors["primary"])

    return Panel(
        content,
        title=f"[bold {colors['success']}]{title}[/]",
        border_style=colors["secondary"],
        padding=(1, 2),
    )


def create_json_panel(data: Any, theme: str = "default") -> Panel:
    """Create a styled JSON panel."""
    colors = get_theme_colors(theme)

    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)

    return Panel(
        syntax,
        title=f"[bold {colors['primary']}]📄 JSON Output[/]",
        border_style=colors["secondary"],
        padding=(1, 1),
    )


def create_details_panel(profile: Dict, theme: str = "default") -> Panel:
    """Create a detailed profile panel."""
    colors = get_theme_colors(theme)

    content = Text()
    content.append("👤 ", style="bold")
    content.append("Full Name: ", style=f"bold {colors['secondary']}")
    content.append(
        f"{profile.get('full_name', 'N/A')}\n", style=f"bold {colors['success']}"
    )

    content.append("📧 ", style="bold")
    content.append("Email: ", style=f"bold {colors['secondary']}")
    content.append(f"{profile.get('email', 'N/A')}\n", style=colors["primary"])

    content.append("👤 ", style="bold")
    content.append("First Name: ", style=f"bold {colors['secondary']}")
    content.append(f"{profile.get('first_name', 'N/A')}\n", style=colors["accent"])

    content.append("👤 ", style="bold")
    content.append("Surname: ", style=f"bold {colors['secondary']}")
    content.append(f"{profile.get('surname', 'N/A')}", style=colors["accent"])

    return Panel(
        content,
        title=f"[bold {colors['primary']}]📋 Profile Details[/]",
        border_style=colors["secondary"],
        padding=(1, 2),
    )


def format_output(results: list, args: argparse.Namespace) -> None:
    """Format and display the output using rich styling."""
    if args.no_color:
        console._color_system = None

    theme = args.theme if not args.no_color else "minimal"
    colors = get_theme_colors(theme)

    # Handle quiet mode
    if args.quiet:
        if args.json:
            if len(results) == 1 and not isinstance(results[0], dict):
                print(json.dumps({"result": results[0]}, indent=2, ensure_ascii=False))
            elif len(results) == 1:
                print(json.dumps(results[0], indent=2, ensure_ascii=False))
            else:
                print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            separator = args.separator.replace("\\n", "\n")
            print(separator.join(str(result) for result in results))
        return

    # Show header
    if not args.no_box:
        console.print(
            create_header(
                "LibFake Generator", f"Generated {len(results)} item(s)", theme
            )
        )
        console.print()

    # Handle JSON output
    if args.json:
        if len(results) == 1 and not isinstance(results[0], dict):
            data = {"result": results[0]}
        elif len(results) == 1:
            data = results[0]
        else:
            data = results

        if args.no_box:
            console.print_json(json.dumps(data, ensure_ascii=False))
        else:
            console.print(create_json_panel(data, theme))
        return

    # Handle different output types
    if not results:
        console.print(Panel("[bold red]No data generated[/]", border_style="red"))
        return

    # Check if all results are profile dictionaries
    if all(isinstance(result, dict) and "full_name" in result for result in results):
        if len(results) == 1 and not results[0].get("_display_format") == "profile":
            # Single detailed profile
            console.print(create_details_panel(results[0], theme))
        else:
            # Multiple profiles as table or single profile table
            console.print(
                create_profile_table(results, theme, show_index=len(results) > 1)
            )
    else:
        # Simple list of strings/names
        if args.no_box:
            for i, result in enumerate(results, 1):
                console.print(f"{i:2d}. {result}", style=colors["primary"])
        else:
            # Determine title based on content type
            if hasattr(args, "firstname") and args.firstname:
                title = "🎭 First Names"
            elif hasattr(args, "surname") and args.surname:
                title = "🎭 Surnames"
            elif hasattr(args, "email") and args.email:
                title = "📧 Email Addresses"
            elif hasattr(args, "fullname") and args.fullname:
                title = "👤 Full Names"
            else:
                title = "🎲 Generated Data"

            console.print(create_simple_list(results, title, theme))


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Configure console based on args
    if args.no_color:
        console._color_system = None

    # If no specific action is chosen, show help
    if not any(
        [
            args.firstname,
            args.surname,
            args.fullname,
            args.email,
            args.generate,
            args.details,
            args.bulk,
            args.random,
        ]
    ):

        # Show a beautiful help screen
        if not args.no_color:
            theme = args.theme
            colors = get_theme_colors(theme)

            help_content = Text()
            help_content.append("Welcome to ", style="bold white")
            help_content.append("LibFake", style=f"bold {colors['primary']}")
            help_content.append("! 🎭\n\n", style="bold white")
            help_content.append(
                "Generate realistic fake data with style.\n", style=colors["secondary"]
            )
            help_content.append(
                "Use --help for detailed options.", style=colors["accent"]
            )

            console.print(
                Panel(
                    Align.center(help_content),
                    title="[bold cyan]🎭 LibFake Generator[/]",
                    border_style=colors["primary"],
                    box=box.DOUBLE,
                )
            )
            console.print(
                "\n💡 Quick start examples:", style=f"bold {colors['success']}"
            )

            examples = [
                ("libfake --generate", "Generate a complete profile"),
                ("libfake --firstname --count 5", "Generate 5 first names"),
                ("libfake --details --json", "Get profile in JSON format"),
            ]

            for cmd, desc in examples:
                console.print(
                    f"  • [bold {colors['primary']}]{cmd}[/] - {desc}",
                    style=colors["secondary"],
                )

        parser.print_help()
        return

    try:
        # Show loading spinner for better UX
        if not args.quiet and not args.no_color:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True,
            ) as progress:
                task = progress.add_task("🎭 Generating fake data...", total=None)

                # Initialize the fake name generator
                fake_gen = FakeName(
                    first_names_path=args.first_names_file,
                    surnames_path=args.surnames_file,
                )

                # Generate the requested data
                results = generate_data(fake_gen, args)
                progress.update(task, description="✨ Data generated successfully!")
        else:
            # Initialize without spinner
            fake_gen = FakeName(
                first_names_path=args.first_names_file, surnames_path=args.surnames_file
            )
            results = generate_data(fake_gen, args)

        # Format and output the results
        format_output(results, args)

        # Show footer with additional info (only in non-quiet mode)
        if not args.quiet and not args.no_color and not args.no_box:
            colors = get_theme_colors(args.theme)
            footer_text = Text()
            footer_text.append("✨ Powered by ", style=colors["secondary"])
            footer_text.append("LibFake", style=f"bold {colors['primary']}")
            footer_text.append(f" v{__version__}", style=colors["accent"])

            console.print()
            console.print(
                Panel(
                    Align.center(footer_text),
                    border_style=colors["secondary"],
                    box=box.SIMPLE,
                )
            )

    except DataFileError as e:
        error_text = Text()
        error_text.append("❌ Data File Error: ", style="bold red")
        error_text.append(str(e), style="red")

        if not args.no_color and not args.no_box:
            console.print(
                Panel(error_text, border_style="red", title="[bold red]Error[/]")
            )
        else:
            console.print(f"Error: {e}", style="red")
        sys.exit(1)

    except Exception as e:
        error_text = Text()
        error_text.append("💥 Unexpected Error: ", style="bold red")
        error_text.append(str(e), style="red")

        if not args.no_color and not args.no_box:
            console.print(
                Panel(
                    error_text, border_style="red", title="[bold red]Critical Error[/]"
                )
            )
        else:
            console.print(f"Unexpected error: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
