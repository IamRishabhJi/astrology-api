#!/usr/bin/env python
"""
Astrology CLI Tool
Command-line interface for Vedic Astrology calculations

Usage:
    python cli.py calculate --day 9 --month 11 --year 2007 --hour 15 --minute 26 --lat 31.326 --lon 75.5762
    python cli.py server --port 8000
    python cli.py batch input.csv output.csv
    python cli.py test
"""
import click
import requests
import json
import csv
from datetime import datetime
from pathlib import Path
import subprocess
import sys


@click.group()
@click.version_option(version="1.0.0", prog_name="Astrology CLI")
def cli():
    """Vedic Astrology CLI Tool - Calculate birth charts and manage API"""
    pass


@cli.command()
@click.option('--day', type=int, required=True, help='Day of birth (1-31)')
@click.option('--month', type=int, required=True, help='Month of birth (1-12)')
@click.option('--year', type=int, required=True, help='Year of birth')
@click.option('--hour', type=int, required=True, help='Hour of birth (0-23)')
@click.option('--minute', type=int, default=0, help='Minute of birth (0-59)')
@click.option('--lat', type=float, required=True, help='Birth latitude')
@click.option('--lon', type=float, required=True, help='Birth longitude')
@click.option('--place', type=str, default='Unknown', help='Birth place name')
@click.option('--tz', type=float, default=5.5, help='Timezone offset from UTC')
@click.option('--api-url', type=str, default='http://217.154.212.188:12909', help='API URL')
@click.option('--output', type=click.Path(), help='Save output to JSON file')
def calculate(day, month, year, hour, minute, lat, lon, place, tz, api_url, output):
    """Calculate birth chart for given date, time, and location"""
    click.echo(f"\n{'='*70}")
    click.echo("  🌟 VEDIC ASTROLOGY CALCULATION 🌟")
    click.echo(f"{'='*70}\n")
    
    payload = {
        "day": day,
        "month": month,
        "year": year,
        "hour": hour,
        "minute": minute,
        "latitude": lat,
        "longitude": lon,
        "place_name": place,
        "timezone_offset": tz
    }
    
    click.echo(f"📍 Calculating for: {place}")
    click.echo(f"📅 Date: {day:02d}-{month:02d}-{year}")
    click.echo(f"🕐 Time: {hour:02d}:{minute:02d} (TZ: {tz:+.1f})\n")
    
    try:
        with click.spinner(text="Processing..."):
            response = requests.post(f"{api_url}/api/calculate", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results
            lagna = data["lagna"]
            click.echo("✅ Calculation successful!\n")
            click.secho("LAGNA (ASCENDANT):", fg="green", bold=True)
            click.echo(f"  Sign: {lagna['sign_name']}")
            click.echo(f"  Degree: {lagna['formatted']}\n")
            
            click.secho("PLANETS:", fg="green", bold=True)
            for planet in data["planets"][:5]:  # Show first 5
                click.echo(f"  {planet['planet']:10} - {planet['sign']:20} ({planet['nakshatra']})")
            click.echo()
            
            click.secho("DIVISIONAL CHARTS:", fg="green", bold=True)
            click.echo(f"  D1 Lagna: {data['d1_chart']['lagna_sign_name']}")
            click.echo(f"  D9 Lagna: {data['d9_chart']['lagna_sign_name']}")
            click.echo(f"  D10 Lagna: {data['d10_chart']['lagna_sign_name']}\n")
            
            click.secho("CURRENT DASHA:", fg="green", bold=True)
            dasha = data["current_dasha"]
            click.echo(f"  Mahadasha: {dasha['mahadasha']['lord']} ({dasha['mahadasha']['duration_years']:.1f} yrs)")
            click.echo(f"  Antardasha: {dasha['antardasha']['lord']} ({dasha['antardasha']['duration_years']:.2f} yrs)\n")
            
            # Save to file if requested
            if output:
                with open(output, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                click.echo(f"📄 Output saved to: {output}")
            
            click.echo(f"{'='*70}\n")
        else:
            click.secho(f"❌ Error: {response.status_code}", fg="red")
            click.echo(response.text)
    
    except requests.exceptions.ConnectionError:
        click.secho("❌ Error: Could not connect to API", fg="red")
        click.echo("Make sure the server is running: python run_server.py")
    except Exception as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")


@cli.command()
@click.option('--port', type=int, default=8000, help='Port to run server on')
@click.option('--host', type=str, default='0.0.0.0', help='Host to bind to')
@click.option('--reload/--no-reload', default=True, help='Enable auto-reload')
def server(port, host, reload):
    """Start the Astrology API server"""
    click.echo(f"\n{'='*70}")
    click.echo("  🌟 ASTROLOGY API SERVER 🌟")
    click.echo(f"{'='*70}\n")
    
    click.echo(f"📍 Starting server on {host}:{port}")
    click.echo("📖 Documentation: http://217.154.212.188:12909/api/docs")
    click.echo("💾 Health check: http://217.154.212.188:12909/api/health")
    click.echo("\n⏸️  Press Ctrl+C to stop\n")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app:app",
        f"--host={host}",
        f"--port={port}"
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        click.echo("\n\n🛑 Server stopped")


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--api-url', type=str, default='http://217.154.212.188:12909', help='API URL')
def batch(input_file, output_file, api_url):
    """Process batch calculations from CSV file
    
    Input CSV format:
    day,month,year,hour,minute,latitude,longitude,place
    9,11,2007,15,26,31.326,75.5762,Amritsar
    """
    click.echo(f"\n{'='*70}")
    click.echo("  📊 BATCH PROCESSING 📊")
    click.echo(f"{'='*70}\n")
    
    try:
        results = []
        total = 0
        success = 0
        
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            total = sum(1 for _ in reader)
        
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            with open(output_file, 'w', newline='') as out:
                writer = None
                
                with click.progressbar(reader, length=total, label="Processing") as bar:
                    for row in bar:
                        try:
                            payload = {
                                "day": int(row['day']),
                                "month": int(row['month']),
                                "year": int(row['year']),
                                "hour": int(row['hour']),
                                "minute": int(row.get('minute', 0)),
                                "latitude": float(row['latitude']),
                                "longitude": float(row['longitude']),
                                "place_name": row.get('place', 'Unknown'),
                                "timezone_offset": float(row.get('tz', 5.5))
                            }
                            
                            response = requests.post(f"{api_url}/api/calculate", json=payload, timeout=10)
                            
                            if response.status_code == 200:
                                data = response.json()
                                lagna = data["lagna"]
                                dasha = data["current_dasha"]["mahadasha"]
                                
                                result = {
                                    'place': row.get('place', 'Unknown'),
                                    'date': f"{int(row['day']):02d}-{int(row['month']):02d}-{row['year']}",
                                    'lagna_sign': lagna['sign_name'],
                                    'lagna_degree': lagna['formatted'],
                                    'mahadasha': dasha['lord'],
                                    'status': 'SUCCESS'
                                }
                                success += 1
                            else:
                                result = {
                                    'place': row.get('place', 'Unknown'),
                                    'date': f"{int(row['day']):02d}-{int(row['month']):02d}-{row['year']}",
                                    'status': 'FAILED'
                                }
                        
                        except Exception as e:
                            result = {
                                'place': row.get('place', 'Unknown'),
                                'status': f'ERROR: {str(e)}'
                            }
                        
                        results.append(result)
                        
                        if writer is None and results:
                            writer = csv.DictWriter(out, fieldnames=results[0].keys())
                            writer.writeheader()
                        
                        if writer:
                            writer.writerow(result)
        
        click.echo(f"\n✅ Processing complete!")
        click.echo(f"📊 Results: {success}/{total} successful")
        click.echo(f"📄 Output saved to: {output_file}\n")
    
    except Exception as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")


@cli.command()
def test():
    """Run test suite"""
    click.echo(f"\n{'='*70}")
    click.echo("  🧪 RUNNING TESTS 🧪")
    click.echo(f"{'='*70}\n")
    
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--cov=app", "--cov-report=html"]
    
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        click.secho("❌ Error: pytest not installed", fg="red")
        click.echo("Install with: pip install -r requirements-dev.txt")


@cli.command()
def doctor():
    """Check API health and configuration"""
    click.echo(f"\n{'='*70}")
    click.echo("  🔍 API HEALTH CHECK 🔍")
    click.echo(f"{'='*70}\n")
    
    checks = {
        "Ephemeris files": Path("./ephemeris").exists(),
        "Configuration": Path(".env").exists(),
        "Tests available": Path("tests/").exists(),
        "Docker support": Path("Dockerfile").exists(),
    }
    
    for check, status in checks.items():
        status_str = "✅" if status else "⚠️"
        click.echo(f"{status_str} {check}")
    
    try:
        response = requests.get("http://217.154.212.188:12909/api/health", timeout=5)
        if response.status_code == 200:
            click.echo("\n✅ API Server is running")
        else:
            click.echo("\n⚠️  API Server responded with error")
    except:
        click.echo("\n⚠️  API Server is not running")
    
    click.echo()


@cli.command()
def version():
    """Show version information"""
    click.echo("Astrology API v1.0.0")
    click.echo("Vedic Astrology Calculation Engine")


if __name__ == "__main__":
    cli()
