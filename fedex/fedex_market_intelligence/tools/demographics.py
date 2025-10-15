"""Demographics tool using US Census API."""

import requests
import json
from typing import List, Optional

# Census API endpoint (no key required for basic queries)
CENSUS_API_BASE = "https://api.census.gov/data/2021/acs/acs5"


def get_demographics(
    zip_codes: List[str],
    metrics: Optional[List[str]] = None
) -> str:
    """
    Fetch demographic data from US Census API for specified zip codes.
    
    Args:
        zip_codes: List of 5-digit zip codes
        metrics: List of metrics to fetch - defaults to ['population', 'income', 'age']
    
    Returns:
        JSON string with demographic data
    """
    
    if not zip_codes:
        return json.dumps({
            "error": "Please provide at least one zip code"
        }, indent=2)
    
    if metrics is None:
        metrics = ['population', 'income', 'age']
    
    # Census variable codes
    # https://api.census.gov/data/2021/acs/acs5/variables.html
    variable_map = {
        'population': 'B01003_001E',  # Total population
        'income': 'B19013_001E',      # Median household income
        'age': 'B01002_001E',         # Median age
        'households': 'B11001_001E',  # Total households
        'employment': 'B23025_005E',  # Employed population
    }
    
    # Build variable list
    variables = [variable_map.get(m, variable_map['population']) for m in metrics]
    variables = list(set(variables))  # Remove duplicates
    
    # Add NAME variable for location name
    variables_str = ','.join(['NAME'] + variables)
    
    # Fetch data for each zip code
    demographics = []
    
    for zip_code in zip_codes[:10]:  # Limit to 10 zip codes to avoid rate limits
        # Census uses ZCTA (ZIP Code Tabulation Areas)
        try:
            url = f"{CENSUS_API_BASE}?get={variables_str}&for=zip%20code%20tabulation%20area:{zip_code}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1:  # First row is headers
                    headers = data[0]
                    values = data[1]
                    
                    # Parse response
                    demo_data = {
                        'zip_code': zip_code,
                        'location_name': values[0] if len(values) > 0 else 'Unknown'
                    }
                    
                    # Map variables to readable names
                    for i, var_code in enumerate(variables):
                        value_idx = i + 1  # Skip NAME which is at index 0
                        if value_idx < len(values):
                            value = values[value_idx]
                            
                            # Convert to int if possible
                            try:
                                value = int(value) if value and value != '-666666666' else None
                            except (ValueError, TypeError):
                                value = None
                            
                            # Map back to readable name
                            for metric_name, var_name in variable_map.items():
                                if var_name == var_code:
                                    if metric_name == 'income' and value:
                                        demo_data['median_household_income'] = value
                                    elif metric_name == 'population' and value:
                                        demo_data['total_population'] = value
                                    elif metric_name == 'age' and value:
                                        demo_data['median_age'] = value
                                    elif metric_name == 'households' and value:
                                        demo_data['total_households'] = value
                                    elif metric_name == 'employment' and value:
                                        demo_data['employed_population'] = value
                    
                    demographics.append(demo_data)
                else:
                    demographics.append({
                        'zip_code': zip_code,
                        'error': 'No data available for this ZIP code'
                    })
            else:
                demographics.append({
                    'zip_code': zip_code,
                    'error': f'API returned status code {response.status_code}'
                })
                
        except requests.exceptions.RequestException as e:
            demographics.append({
                'zip_code': zip_code,
                'error': f'Request failed: {str(e)}'
            })
        except Exception as e:
            demographics.append({
                'zip_code': zip_code,
                'error': f'Unexpected error: {str(e)}'
            })
    
    # Generate summary insights
    insights = []
    valid_data = [d for d in demographics if 'error' not in d]
    
    if valid_data:
        # Average income
        incomes = [d['median_household_income'] for d in valid_data if 'median_household_income' in d and d['median_household_income']]
        if incomes:
            avg_income = sum(incomes) / len(incomes)
            insights.append(f"Average median household income: ${avg_income:,.0f}")
        
        # Total population
        populations = [d['total_population'] for d in valid_data if 'total_population' in d and d['total_population']]
        if populations:
            total_pop = sum(populations)
            insights.append(f"Total population across {len(populations)} ZIP codes: {total_pop:,}")
        
        # Age demographics
        ages = [d['median_age'] for d in valid_data if 'median_age' in d and d['median_age']]
        if ages:
            avg_age = sum(ages) / len(ages)
            insights.append(f"Average median age: {avg_age:.1f} years")
    
    response = {
        "query_parameters": {
            "zip_codes_requested": zip_codes,
            "metrics_requested": metrics
        },
        "summary": {
            "successful_queries": len(valid_data),
            "failed_queries": len(demographics) - len(valid_data),
            "insights": insights
        },
        "demographics": demographics,
        "note": "Data sourced from US Census Bureau ACS 5-Year Estimates (2021)",
        "api_limitations": "Limited to 10 ZIP codes per request to avoid rate limits"
    }
    
    return json.dumps(response, indent=2, default=str)

