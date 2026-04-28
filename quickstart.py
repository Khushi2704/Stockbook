"""
Quick Start Script
Run this to verify installation and get started with Stockbook
"""
import os
import sys
import platform


def print_banner():
    """Print welcome banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                     STOCKBOOK MEDICAL STORE SYSTEM                        ║
║                      Professional & Production-Ready                      ║
║                                                                           ║
║                          Quick Start Guide                                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"✓ Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ ERROR: Python 3.7+ required")
        return False
    
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    dependencies = {
        'PyQt5': 'PyQt5',
    }
    
    missing = []
    
    for name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"  ✓ {name} installed")
        except ImportError:
            print(f"  ✗ {name} NOT installed")
            missing.append(name)
    
    if missing:
        print(f"\n✗ Missing dependencies: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        return False
    
    return True


def check_database():
    """Check database setup"""
    print("\n📊 Checking database...")
    
    try:
        from database.db import init_database
        init_database()
        print("  ✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False


def show_menu():
    """Show main menu"""
    print("\n" + "="*70)
    print("MAIN MENU")
    print("="*70)
    print("\n1. Start Application")
    print("2. Run Tests")
    print("3. Generate Setup Guide")
    print("4. Generate Developer Guide")
    print("5. Generate Deployment Checklist")
    print("6. Build Executable")
    print("7. Exit")
    print("\n" + "="*70)


def start_application():
    """Start the main application"""
    print("\n🚀 Starting Stockbook Application...")
    print("  Default credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n  ⚠️  Please change password after first login!")
    
    try:
        from main import main
        main()
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        input("Press Enter to return to menu...")


def run_tests():
    """Run test suite"""
    print("\n🧪 Running Test Suite...")
    print("="*70)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test.py"], cwd=os.path.dirname(__file__))
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False


def generate_setup_guide():
    """Generate setup guide"""
    print("\n📋 Generating Setup Guide...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "SETUP_GUIDE.py"], cwd=os.path.dirname(__file__))
        print("✓ Setup guide generated")
    except Exception as e:
        print(f"✗ Error: {e}")


def generate_developer_guide():
    """Generate developer guide"""
    print("\n👨‍💻 Generating Developer Guide...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "DEVELOPER_GUIDE.py"], cwd=os.path.dirname(__file__))
        print("✓ Developer guide generated")
    except Exception as e:
        print(f"✗ Error: {e}")


def generate_deployment_checklist():
    """Generate deployment checklist"""
    print("\n📋 Generating Deployment Checklist...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "DEPLOYMENT_CHECKLIST.py"], cwd=os.path.dirname(__file__))
        print("✓ Deployment checklist generated")
    except Exception as e:
        print(f"✗ Error: {e}")


def build_executable():
    """Build executable"""
    print("\n🔨 Building Executable...")
    print("This will take a few minutes...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "build.py"], cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("\n✓ Build successful!")
            print("Executable created in: dist/Stockbook.exe")
        else:
            print("\n✗ Build failed")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main entry point"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print_banner()
    
    # Run checks
    print("🔍 Running system checks...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
    ]
    
    passed = 0
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"✗ {name} check failed: {e}")
    
    print(f"\n✓ {passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        print("\n✓ System is ready to use!")
    else:
        print("\n⚠️  Some checks failed. Please fix issues before continuing.")
        input("Press Enter to exit...")
        return
    
    # Show menu
    while True:
        show_menu()
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            start_application()
        elif choice == "2":
            run_tests()
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            generate_setup_guide()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            generate_developer_guide()
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            generate_deployment_checklist()
            input("\nPress Enter to return to menu...")
        elif choice == "6":
            build_executable()
            input("\nPress Enter to return to menu...")
        elif choice == "7":
            print("\n👋 Thank you for using Stockbook!")
            print("Visit again soon!")
            break
        else:
            print("✗ Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
