#!/usr/bin/env python3
"""
A/B Testing Desktop Application
Main entry point for the application

This application provides a comprehensive GUI for analyzing A/B test results
with statistical methods and interactive visualizations.
"""

import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    try:
        app = MainWindow()
        app.run()
    except ImportError as e:
        print("Error: Missing required dependencies.")
        print("Please install the required packages by running:")
        print("pip install -r requirements.txt")
        print(f"\nSpecific error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while starting the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
