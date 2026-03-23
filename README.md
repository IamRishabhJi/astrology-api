# Vedic Astrology Calculation API

A professional REST API for Vedic Astrology birth chart calculations with complete support for divisional charts, planet positions, nakshatra calculations, and Vimshottari Dasha system.

## Overview

This API provides comprehensive Vedic astrology calculations including:
- **D1 (Rashi) Chart**: Main zodiac chart
- **D9 (Navamsa) Chart**: Spouse and higher purpose chart
- **D10 (Dashamsa) Chart**: Career and professional growth chart
- **Planet Positions**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- **Nakshatra & Pada**: Lunar mansion and quarter calculations
- **Retrograde & Combust**: Planetary state analysis
- **Vimshottari Dasha**: 120-year Vedic timing system with 4 hierarchy levels

## Features

✅ Complete birth chart calculations  
✅ Accurate planet positions (Swiss Ephemeris)  
✅ Divisional chart support (D1, D9, D10)  
✅ Nakshatra calculations (27 nakshatras)  
✅ Dasha hierarchy (Mahadasha, Antardasha, Pratyantar Dasha, Sookshma Dasha)  
✅ Current active dasha detection  
✅ RESTful API with FastAPI  
✅ Comprehensive error handling  
✅ Docker deployment ready  
✅ CORS enabled for frontend integration  

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd astrology-calculations
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
python run_server.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

The API will be available at `http://localhost:12909`

## Project Structure

```
astrology-calculations/
├── app.py                 # Main FastAPI application
├── cli.py                 # Command-line interface
├── config.py              # Configuration settings
├── run_server.py          # Server startup script
├── run_everything.py      # All-in-one runner
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── LICENSE                # License information
│
├── calculations/          # Core calculation modules
│   ├── positioning.py     # Lagna and coordinate calculations
│   ├── planets.py         # Planet position calculations
│   ├── divisional_charts.py  # D1, D9, D10 chart calculations
│   └── dasha.py           # Dasha system calculations
│
├── models/
│   ├── schemas.py         # Pydantic request/response models
│   └── __init__.py
│
├── core/                  # Core utilities
│   └── __init__.py
│
├── ephemeris/             # Ephemeris data files
│   ├── sepl_*.se1         # Planet ephemeris
│   ├── semo_*.se1         # Moon ephemeris
│   └── seas_*.se1         # Asteroid ephemeris
│
└── tests/
    ├── test_api.py        # API endpoint tests
    └── __init__.py
```

## API Endpoints

### System Endpoints

**Health Check**
```
GET /api/health
```
Returns API status and version.

**API Information**
```
GET /api/info
```
Returns available features and all endpoints.

**Documentation**
```
GET /api/docs
GET /api/redoc
```
Interactive API documentation (Swagger UI and ReDoc).

### Calculation Endpoints

**Complete Birth Chart**
```
POST /api/calculate
```
Calculate complete birth chart with D1, D9, D10 charts and current dasha.

**Dasha Hierarchy**
```
POST /api/dasha-calculator
```
Calculate complete Dasha hierarchy (all 120 years) with 4 levels of dasha periods.

**Dasha Documentation**
```
GET /api/docs/dasha-calculator
```
Comprehensive documentation for the Dasha Calculator endpoint.

## Request Example

```json
{
  "day": 9,
  "month": 11,
  "year": 2007,
  "hour": 15,
  "minute": 26,
  "second": 0,
  "latitude": 31.626,
  "longitude": 75.5762,
  "timezone_offset": 5.5,
  "place_name": "Amritsar",
  "country": "India"
}
```

## Response Example

```json
{
  "status": "success",
  "message": "Birth chart calculated successfully",
  "birth_data": {
    "date": "09-11-2007",
    "time_ist": "15:26",
    "time_utc": "09:56",
    "place": "Amritsar",
    "latitude": 31.626,
    "longitude": 75.5762,
    "timezone_offset": 5.5
  },
  "lagna": {
    "degree": 187.45,
    "sign": 6,
    "sign_name": "Virgo",
    "formatted": "6°27'00\""
  },
  "planets": [...],
  "d1_chart": {...},
  "d9_chart": {...},
  "d10_chart": {...},
  "current_dasha": {...}
}
```

## Usage Examples

### Python Client

```python
import requests

url = "http://localhost:8000/api/calculate"
payload = {
    "day": 9,
    "month": 11,
    "year": 2007,
    "hour": 15,
    "minute": 26,
    "latitude": 31.626,
    "longitude": 75.5762,
    "timezone_offset": 5.5,
    "place_name": "Amritsar"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Lagna: {data['lagna']['sign_name']} {data['lagna']['degree']}")
print(f"Moon Sign: {data['planets'][1]['sign_name']}")
print(f"Current Mahadasha: {data['current_dasha']['mahadasha']['lord']}")
```

### cURL

```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "day": 9,
    "month": 11,
    "year": 2007,
    "hour": 15,
    "minute": 26,
    "latitude": 31.626,
    "longitude": 75.5762,
    "timezone_offset": 5.5,
    "place_name": "Amritsar"
  }'
```

## Configuration

Configuration settings are defined in `config.py`. Key settings include:
- Ephemeris path
- Server host and port
- CORS settings
- Logging configuration

## Dependencies

See `requirements.txt` for complete list. Key dependencies:
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **pyswisseph**: Swiss Ephemeris library (planet calculations)
- **Python-dateutil**: Date handling

## Testing

Run tests with:
```bash
pytest tests/
```

## Technical Specifications

- **Calculation Precision**: Day/Hour level (minute-level available)
- **Ephemeris**: Swiss Ephemeris (seconds-level accuracy)
- **Dasha System**: Vimshottari (120-year cycle)
- **Planets**: 9 (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
- **Nakshatras**: 27
- **Processing Time**: < 2 seconds per request
- **Response Size**: 50-200 KB per full calculation

## Error Handling

The API returns standard HTTP status codes and error messages:
- **400 Bad Request**: Invalid input parameters
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side calculation errors

All errors include descriptive messages to help identify and fix issues.

## Production Deployment

The API is production-ready with:
- ✅ Comprehensive error handling
- ✅ Input validation
- ✅ Consistent response structures
- ✅ Fast response times
- ✅ Scalable stateless design
- ✅ Security measures (input sanitization)
- ✅ Extensive testing

### Deploy to Production

```bash
# Using Docker
docker-compose up -d

# The API will be available at the configured port
# Update docker-compose.yml for production settings
```

## API Documentation

Full interactive documentation available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Dasha Calculator Docs**: http://localhost:8000/api/docs/dasha-calculator

## Vedic Astrology Concepts

### Dasha System (Vimshottari)
The Vimshottari Dasha is a 120-year cycle divided into 9 main periods (Mahadashas). Each Mahadasha is further divided into:
- **Antardasha** (sub-period): 9 per Mahadasha
- **Pratyantar Dasha** (sub-sub-period): 81 total
- **Sookshma Dasha** (micro-period): 729 total

### Divisional Charts
- **D1 (Rashi)**: Main chart for overall life
- **D9 (Navamsa)**: Spouse, higher purpose, spiritual inclination
- **D10 (Dashamsa)**: Career, profession, achievement

### Nakshatras
27 lunar mansions that the Moon passes through during its 27.3-day month cycle.

## Support & Contact

For issues, questions, or feature requests, please open an issue in the repository.

## License

See [LICENSE](LICENSE) file for details.

## Version

Current Version: 1.0.0  
Last Updated: 2026

---

**Disclaimer**: This API provides astrological calculations based on Vedic principles. Results should be interpreted by qualified astrologers and not used as sole basis for life decisions.
