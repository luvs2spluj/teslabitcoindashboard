"""
YCharts data source adapter for Tesla delivery data and other financial metrics.
Parses HTML data from YCharts indicators.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
import time
import random
import structlog
import re
from .base import DataSource

logger = structlog.get_logger()


class YChartsDataSource(DataSource):
    """YCharts data source for Tesla delivery data and financial metrics."""
    
    def __init__(self):
        super().__init__("ycharts")
        self.base_url = "https://ycharts.com"
        self.session = requests.Session()
        # Add random user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.rate_limit_delay = 3.0  # Conservative rate limiting for web scraping
    
    def _make_request(self, url: str) -> Dict[str, Any]:
        """Make a rate-limited request to YCharts."""
        try:
            # Rate limiting: wait 2-5 seconds between requests
            time.sleep(random.uniform(2, 5))
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'html': response.text,
                    'error': None
                }
            elif response.status_code == 429:  # Rate limited
                # Wait longer and retry once
                time.sleep(random.uniform(10, 15))
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return {
                        'success': True,
                        'html': response.text,
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'html': None,
                        'error': f'Rate limited: {response.status_code}'
                    }
            else:
                return {
                    'success': False,
                    'html': None,
                    'error': f'HTTP {response.status_code}: {response.text[:200]}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'html': None,
                'error': f'Request error: {str(e)}'
            }
    
    def _parse_tesla_deliveries_html(self, html: str) -> Dict[str, Any]:
        """Parse Tesla delivery data from YCharts HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract current value
            current_value = None
            current_period = None
            
            # Look for the main value display
            value_elements = soup.find_all(['span', 'div'], string=re.compile(r'\d+\.?\d*'))
            for element in value_elements:
                text = element.get_text().strip()
                if re.match(r'^\d+\.?\d*$', text) and len(text) > 3:  # Likely a delivery number
                    current_value = float(text.replace(',', ''))
                    break
            
            # Look for period information
            period_elements = soup.find_all(['span', 'div'], string=re.compile(r'(Q[1-4]|Quarter|Jun|Mar|Dec|Sep)'))
            for element in period_elements:
                text = element.get_text().strip()
                if any(month in text for month in ['Q1', 'Q2', 'Q3', 'Q4', 'Jun', 'Mar', 'Dec', 'Sep']):
                    current_period = text
                    break
            
            # Extract historical data from tables
            historical_data = []
            
            # Look for data tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        date_text = cells[0].get_text().strip()
                        value_text = cells[1].get_text().strip()
                        
                        # Parse date
                        try:
                            if 'Jun' in date_text and '2025' in date_text:
                                parsed_date = datetime.strptime('June 30, 2025', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2025' in date_text:
                                parsed_date = datetime.strptime('March 31, 2025', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2024' in date_text:
                                parsed_date = datetime.strptime('December 31, 2024', '%B %d, %Y').date()
                            elif 'Sep' in date_text and '2024' in date_text:
                                parsed_date = datetime.strptime('September 30, 2024', '%B %d, %Y').date()
                            elif 'Jun' in date_text and '2024' in date_text:
                                parsed_date = datetime.strptime('June 30, 2024', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2024' in date_text:
                                parsed_date = datetime.strptime('March 31, 2024', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2023' in date_text:
                                parsed_date = datetime.strptime('December 31, 2023', '%B %d, %Y').date()
                            elif 'Sep' in date_text and '2023' in date_text:
                                parsed_date = datetime.strptime('September 30, 2023', '%B %d, %Y').date()
                            elif 'Jun' in date_text and '2023' in date_text:
                                parsed_date = datetime.strptime('June 30, 2023', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2023' in date_text:
                                parsed_date = datetime.strptime('March 31, 2023', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2022' in date_text:
                                parsed_date = datetime.strptime('December 31, 2022', '%B %d, %Y').date()
                            elif 'Sep' in date_text and '2022' in date_text:
                                parsed_date = datetime.strptime('September 30, 2022', '%B %d, %Y').date()
                            elif 'Jun' in date_text and '2022' in date_text:
                                parsed_date = datetime.strptime('June 30, 2022', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2022' in date_text:
                                parsed_date = datetime.strptime('March 31, 2022', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2021' in date_text:
                                parsed_date = datetime.strptime('December 31, 2021', '%B %d, %Y').date()
                            elif 'Sep' in date_text and '2021' in date_text:
                                parsed_date = datetime.strptime('September 30, 2021', '%B %d, %Y').date()
                            elif 'Jun' in date_text and '2021' in date_text:
                                parsed_date = datetime.strptime('June 30, 2021', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2021' in date_text:
                                parsed_date = datetime.strptime('March 31, 2021', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2020' in date_text:
                                parsed_date = datetime.strptime('December 31, 2020', '%B %d, %Y').date()
                            elif 'Sep' in date_text and '2020' in date_text:
                                parsed_date = datetime.strptime('September 30, 2020', '%B %d, %Y').date()
                            elif 'Jun' in date_text and '2020' in date_text:
                                parsed_date = datetime.strptime('June 30, 2020', '%B %d, %Y').date()
                            elif 'Mar' in date_text and '2020' in date_text:
                                parsed_date = datetime.strptime('March 31, 2020', '%B %d, %Y').date()
                            elif 'Dec' in date_text and '2019' in date_text:
                                parsed_date = datetime.strptime('December 31, 2019', '%B %d, %Y').date()
                            else:
                                continue
                            
                            # Parse value
                            value_match = re.search(r'(\d+\.?\d*)', value_text.replace(',', ''))
                            if value_match:
                                value = float(value_match.group(1))
                                
                                historical_data.append({
                                    'date': parsed_date,
                                    'deliveries': value,
                                    'quarter': f"Q{((parsed_date.month - 1) // 3) + 1} {parsed_date.year}"
                                })
                                
                        except Exception as e:
                            logger.warning(f"Error parsing date/value: {date_text}/{value_text} - {e}")
                            continue
            
            # Sort by date
            historical_data.sort(key=lambda x: x['date'])
            
            return {
                'current_value': current_value,
                'current_period': current_period,
                'historical_data': historical_data,
                'latest_deliveries': historical_data[-1] if historical_data else None,
                'total_records': len(historical_data)
            }
            
        except Exception as e:
            logger.error(f"Error parsing Tesla deliveries HTML: {e}")
            return {
                'current_value': None,
                'current_period': None,
                'historical_data': [],
                'latest_deliveries': None,
                'total_records': 0
            }
    
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch data from YCharts - implements abstract method from base class."""
        # Default to Tesla deliveries if no specific data type requested
        data_type = kwargs.get('data_type', 'tesla_deliveries')
        
        if data_type == 'tesla_deliveries':
            return await self.fetch_tesla_deliveries()
        else:
            return {
                'success': False,
                'data': None,
                'error': f'Unsupported data type: {data_type}'
            }
    
    async def fetch_tesla_deliveries(self) -> Dict[str, Any]:
        """Fetch Tesla delivery data from YCharts."""
        try:
            url = "https://ycharts.com/indicators/tesla_inc_tsla_total_deliveries_quarterly"
            
            logger.info("Fetching Tesla delivery data from YCharts")
            
            result = self._make_request(url)
            
            if not result['success']:
                return {
                    'success': False,
                    'data': None,
                    'error': result['error']
                }
            
            # Parse the HTML
            parsed_data = self._parse_tesla_deliveries_html(result['html'])
            
            return {
                'success': True,
                'data': {
                    'symbol': 'TSLA',
                    'metric': 'total_deliveries',
                    'source': 'ycharts',
                    'fetched_at': datetime.now().isoformat(),
                    'current_value': parsed_data['current_value'],
                    'current_period': parsed_data['current_period'],
                    'historical_data': parsed_data['historical_data'],
                    'latest_deliveries': parsed_data['latest_deliveries'],
                    'total_records': parsed_data['total_records']
                },
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch Tesla delivery data: {e}")
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate YCharts data."""
        if not isinstance(data, dict):
            return False
        
        if "data" not in data:
            return False
        
        if not data["data"]:
            return False
        
        # Validate that we have historical data
        if "historical_data" not in data["data"]:
            return False
        
        return True
