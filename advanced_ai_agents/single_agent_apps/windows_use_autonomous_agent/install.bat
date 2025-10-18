@echo off
echo ================================================
echo   Windows Use Agent - Complete Installer
echo ================================================
echo.
echo Installing ALL dependencies from pyproject.toml...
echo (Core + GUI + Voice + Advanced Features)
echo.

pip install -e .

echo.
echo ================================================
echo   ✅ Installation Complete!
echo ================================================
echo.
echo 📦 Installed everything including:
echo   ✓ Core agent framework (langchain, windows-use)
echo   ✓ Desktop GUI (customtkinter)
echo   ✓ Voice input (SpeechRecognition, sounddevice)
echo   ✓ Smart workflow engine (watchdog, schedule)
echo   ✓ Context awareness (psutil, pywin32)
echo   ✓ Security layer (cryptography)
echo   ✓ Ecosystem integrations (requests, dotenv)
echo.
echo 🚀 Next steps:
echo   1. Copy .env-example to .env
echo   2. Add your GOOGLE_API_KEY to .env
echo   3. Run: start.bat
echo.
echo 📚 Documentation: docs/QUICKSTART.md
echo.
pause
