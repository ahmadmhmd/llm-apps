"""
New entry point for the refactored Windows Use Agent application.

This is the MVC-based version with professional UI.
To run the original version, use: python main_desktop_gui.py
To run the new version, use: python main_new.py
"""

from views.main_window import MainWindow


def main():
    """Main entry point."""
    print("🚀 Starting Windows Use Enterprise AI...")
    print("📂 MVC Architecture Active")
    print("🎨 Professional UI Loaded")
    print("-" * 50)
    
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
