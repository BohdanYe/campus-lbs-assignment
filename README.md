# Campus Services & Accessibility Finder

## Overview

Campus Services & Accessibility Finder is a location-based services application developed for the Location-Based Services module.

The application helps users explore campus facilities, walking routes, and different campus zones using an interactive spatial web application.

## Current Features

- PostgreSQL with PostGIS
- Django web application
- Docker Compose deployment
- Spatial Point data for campus facilities
- Spatial LineString data for routes
- Spatial Polygon data for zones
- Spatial GiST indexes
- Django administration interface

## Planned Features

- CRUD REST API
- Nearest facility search
- Radius search
- Point-in-polygon search
- Route and zone intersection search
- Interactive Leaflet map
- Responsive Bootstrap interface

## Technology Stack

- Python
- Django
- Django REST Framework
- GeoDjango
- PostgreSQL
- PostGIS
- Leaflet
- Bootstrap 5
- Docker
- Docker Compose
- pgAdmin

## Spatial Data Model

### Place
Geometry: Point

Represents campus facilities such as libraries, cafes, study areas, printers, and bicycle parking.

### Route
Geometry: LineString

Represents walking, cycling, and accessible routes.

### Zone
Geometry: Polygon

Represents campus boundaries, pedestrian areas, study areas, accessible zones, and green spaces.

## Development Status

Part 1 completed:

- Docker environment
- PostGIS database
- Django project
- Spatial models
- Database migrations
- Spatial indexes