"""
Simple startup script for Astrology API Server

Run this file directly to start the API server:
    python run_server.py

Or use it as a module:
    from run_server import start_server
    start_server()
"""
import sys
import os


def main():
    """Start the API server"""
    print("\n" + "="*70)
    print("  🌟 VEDIC ASTROLOGY API SERVER - STARTUP 🌟")
    print("="*70)
    
    # Check if ephemeris folder exists
    if not os.path.exists('./ephemeris'):
        print("\n⚠️  WARNING: './ephemeris' folder not found!")
        print("   Make sure the ephemeris data files are in the 'ephemeris' directory.")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("   Startup cancelled.")
            return
    
    print("\n📦 Importing dependencies...")
    try:
        import uvicorn
        from app import app
        print("   ✓ All dependencies imported successfully")
    except ImportError as e:
        print(f"\n❌ ERROR: Missing required dependency: {e}")
        print("\n   Install dependencies using:")
        print("   pip install -r requirements.txt")
        return
    
    print("\n" + "="*70)
    print("✨ SERVER STARTING...")
    print("="*70)
    print("\n📍 API Documentation: http://localhost:12909/api/docs")
    print("💾 Health Check: http://localhost:12909/api/health")
    print("ℹ️  API Info: http://localhost:12909/api/info")
    print("\n⏸️  Press Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    # Start the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=12909,
        reload=True,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("  🛑 SERVER STOPPED")
        print("="*70 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}\n")
        sys.exit(1)
