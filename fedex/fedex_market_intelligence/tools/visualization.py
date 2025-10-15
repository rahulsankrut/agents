"""Map visualization tool using Google Maps."""

import json
from typing import List, Dict, Optional
from urllib.parse import urlencode

from fedex_market_intelligence.config import config

GOOGLE_MAPS_API_KEY = config.google_maps_api_key


def generate_map_visualization(
    locations: List[Dict[str, any]],
    center_location: Optional[str] = None,
    map_type: str = "demand_heatmap",
    zoom_level: int = 10
) -> str:
    """
    Generate Google Maps visualization URLs and embed codes.
    
    Args:
        locations: List of location dicts with 'lat', 'lng', 'label', and optional 'value' fields
        center_location: Center point for map (city name or lat/lng)
        map_type: Type of visualization - 'demand_heatmap', 'markers', 'comparison'
        zoom_level: Map zoom level (1-20)
    
    Returns:
        JSON string with map URLs and embed code
    """
    
    if not locations:
        return json.dumps({
            "error": "Please provide at least one location to visualize"
        }, indent=2)
    
    # Calculate center if not provided
    if not center_location and locations:
        # Use average of all coordinates
        avg_lat = sum(loc.get('lat', 0) for loc in locations) / len(locations)
        avg_lng = sum(loc.get('lng', 0) for loc in locations) / len(locations)
        center = f"{avg_lat},{avg_lng}"
    else:
        center = center_location or "39.8283,-98.5795"  # Center of US as fallback
    
    # Generate markers for Static Maps API
    markers = []
    for i, loc in enumerate(locations[:25]):  # Limit to 25 markers
        lat = loc.get('lat', 0)
        lng = loc.get('lng', 0)
        label = loc.get('label', str(i+1))
        value = loc.get('value', 0)
        
        # Convert value to number if it's a string
        try:
            value = float(value) if value else 0
        except (ValueError, TypeError):
            value = 0
        
        # Color code by value if present
        color = "red"
        if value > 0:
            if value > 1000:
                color = "red"  # High demand
            elif value > 500:
                color = "orange"  # Medium demand
            else:
                color = "yellow"  # Low demand
        
        markers.append(f"color:{color}|label:{label[:1]}|{lat},{lng}")
    
    # Check if API key is configured
    has_api_key = GOOGLE_MAPS_API_KEY is not None and len(str(GOOGLE_MAPS_API_KEY)) > 0
    
    # Build Static Maps API URL
    if has_api_key:
        static_map_params = {
            'center': center,
            'zoom': zoom_level,
            'size': '800x600',
            'maptype': 'roadmap',
            'markers': markers,
            'key': GOOGLE_MAPS_API_KEY
        }
        static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?{urlencode(static_map_params, doseq=True)}"
        embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={center}&zoom={zoom_level}"
    else:
        static_map_url = None
        embed_url = None
    
    # Generate Google Maps link (works without API key)
    google_maps_url = f"https://www.google.com/maps/@{center},{zoom_level}z"
    
    # Generate directions URL if comparing two locations (works without API key)
    directions_url = None
    if len(locations) >= 2:
        origin = f"{locations[0].get('lat', 0)},{locations[0].get('lng', 0)}"
        destination = f"{locations[1].get('lat', 0)},{locations[1].get('lng', 0)}"
        directions_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
    
    # Generate location summary
    location_summary = []
    for loc in locations[:10]:
        location_summary.append({
            'label': loc.get('label', 'Unknown'),
            'coordinates': f"{loc.get('lat', 0):.4f}, {loc.get('lng', 0):.4f}",
            'google_maps_link': f"https://www.google.com/maps/search/?api=1&query={loc.get('lat', 0)},{loc.get('lng', 0)}",
            'value': loc.get('value'),
            'description': loc.get('description', '')
        })
    
    # Create visualization based on API key availability
    if has_api_key:
        # Generate markdown-friendly output with clickable embed
        visualization_markdown = f"""## Map Visualization: {map_type.replace('_', ' ').title()}

**View Interactive Map**: [Open in Google Maps]({google_maps_url})

### Locations Plotted:
"""
        for i, loc in enumerate(location_summary, 1):
            visualization_markdown += f"{i}. **{loc['label']}** - [{loc['coordinates']}]({loc['google_maps_link']})\n"
        
        visualization_markdown += f"""
### Embed Code (for iframe):
```html
<iframe 
    width="800" 
    height="600" 
    style="border:0"
    loading="lazy"
    src="{embed_url}">
</iframe>
```

**Static Map Image URL**: [View Image]({static_map_url})
"""
        
        visualization_html = f"""<iframe width="800" height="600" style="border:0" loading="lazy" src="{embed_url}"></iframe>"""
        api_status = "configured"
    else:
        # Fallback: Generate markdown with clickable links
        visualization_markdown = f"""## Map Visualization: {map_type.replace('_', ' ').title()}

**View Map**: [Open in Google Maps]({google_maps_url})

### Locations:
"""
        for i, loc in enumerate(location_summary, 1):
            visualization_markdown += f"{i}. **{loc['label']}** - [{loc['coordinates']}]({loc['google_maps_link']})\n"
        
        visualization_markdown += "\n*Note: Set GOOGLE_MAPS_API_KEY for embedded maps*"
        
        visualization_html = None
        api_status = "not_configured"
    
    response = {
        "query_parameters": {
            "locations_count": len(locations),
            "map_type": map_type,
            "center": center,
            "zoom_level": zoom_level
        },
        "api_status": api_status,
        "visualization": {
            "google_maps_url": google_maps_url,
            "static_map_url": static_map_url if has_api_key else None,
            "embed_url": embed_url if has_api_key else None,
            "embed_html": visualization_html,
            "directions_url": directions_url,
        },
        "locations_plotted": location_summary,
        "markdown_output": visualization_markdown,
        "legend": {
            "red_markers": "High demand (>1000 shipments)",
            "orange_markers": "Medium demand (500-1000 shipments)",
            "yellow_markers": "Low demand (<500 shipments)"
        },
        "user_instructions": f"""
To view the map:
1. Click this link to open in Google Maps: {google_maps_url}
2. Or use the embed URL in an iframe: {embed_url if has_api_key else 'N/A'}
3. Individual location links are provided in 'locations_plotted'
        """ if has_api_key else f"Click this link to view: {google_maps_url}"
    }
    
    return json.dumps(response, indent=2, default=str)

