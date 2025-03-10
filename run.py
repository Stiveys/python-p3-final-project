#!/usr/bin/env python3
from culinary_compass.models import create_tables
from culinary_compass.cli import cli

if __name__ == "__main__":
    create_tables()
    cli()