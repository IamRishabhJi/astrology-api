#!/usr/bin/env python3
"""
Complete startup script for Vedic Astrology API
Handles all initialization and runs the server on port 12909

This script is designed for containerized deployments
(Docker, Pterodactyl Panel, etc.)

Usage:
  python run_everything.py
  /usr/local/bin/python /home/container/run_everything.py
"""
import sys
import os
import subprocess
from pathlib import Path


def check_ephemeris():
    """Verify ephemeris files exist"""
    ephemeris_path = Path('./ephemeris')
    
    if not ephemeris_path.exists():
        print("\n⚠️  WARNING: './ephemeris' folder not found!")
        print("   Astrology calculations require ephemeris data files.")
        print("   Ensure the ephemeris/ directory with .se1 files is deployed.")
        return False
    
    # Check for key ephemeris files
    required_files = ['seas_00.se1', 'sepl_00.se1', 'semo_00.se1']
    missing_files = [f for f in required_files if not (ephemeris_path / f).exists()]
    
    if missing_files:
        print(f"\n⚠️  WARNING: Missing ephemeris files: {', '.join(missing_files)}")
        return False
    
    print("✓ Ephemeris files found")
    return True


def check_dependencies():
    """Verify all required Python packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'swisseph',
        'click',
        'requests',
    ]
    
    print("\n📦 Checking dependencies...")
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True


def print_header():
    """Print startup header"""
    print("\n" + "="*70)
    print("  🌟 VEDIC ASTROLOGY API - CONTAINER STARTUP 🌟")
    print("="*70)
    print(f"\n📍 Server Address: http://0.0.0.0:12909")
    print(f"📍 API Docs: http://your-domain.com:12909/api/docs")
    print(f"🖥️  Port: 12909")
    print("="*70)


def start_server():
    """Start the Astrology API server"""
    print("\n🚀 Starting server with Uvicorn...")
    print(f"   Host: 0.0.0.0")
    print(f"   Port: 12909")
    print(f"   Workers: 4 (production mode)")
    print(f"   Reload: False (production mode)\n")
    
    try:
        # Import after dependency check
        import uvicorn
        from config import settings
        from app import app
        
        # Run server with production settings
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            workers=1,  # Container typically runs single process
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to start server: {e}")
        print(f"\nStack trace:")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main startup routine"""
    print_header()
    
    # Step 1: Check ephemeris
    print("\n🔍 Verifying ephemeris data...")
    if not check_ephemeris():
        print("\n⚠️  Continuing without ephemeris validation...")
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies missing. Cannot start server.")
        sys.exit(1)
    
    # Step 3: Show configuration
    print("\n⚙️  Configuration:")
    print(f"   Working directory: {os.getcwd()}")
    print(f"   Python version: {sys.version.split()[0]}")
    print(f"   Python executable: {sys.executable}")
    
    # Step 4: Start server
    print("\n" + "="*70)
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
