#!/usr/bin/env python3
from culinary_compass.models import create_tables
from culinary_compass.cli import cli

if __name__ == "__main__":
    # Create database tables if they don't exist
    # This ensures the application can run without manual setup
    create_tables()

    # Start the CLI application
    # This will parse command-line arguments and execute the appropriate function
    cli()