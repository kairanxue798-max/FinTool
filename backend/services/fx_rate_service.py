import os
import requests
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()


class FXRateService:
    """
    Foreign Exchange Rate Service
    Uses exchangerate-api.io (free tier) or similar service
    """
    
    def __init__(self):
        # Using exchangerate-api.io free tier
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY", "")
        self.base_url = "https://api.exchangerate-api.com/v4"
    
    def get_current_rates(self, base_currency: str = "USD") -> Dict:
        """
        Get current exchange rates
        """
        try:
            if self.api_key:
                # If API key is provided, use it
                url = f"{self.base_url}/latest/{base_currency}"
                response = requests.get(url, timeout=10)
            else:
                # Free tier without API key
                url = f"{self.base_url}/latest/{base_currency}"
                response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "base": data.get("base", base_currency),
                    "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
                    "rates": data.get("rates", {}),
                    "source": "exchangerate-api.io"
                }
            else:
                return self._fallback_rates(base_currency)
        except Exception as e:
            print(f"Error fetching FX rates: {e}")
            return self._fallback_rates(base_currency)
    
    def get_historical_rates(self, date: str, base_currency: str = "USD") -> Dict:
        """
        Get historical exchange rates for a specific date
        Format: YYYY-MM-DD
        """
        try:
            url = f"{self.base_url}/history/{base_currency}/{date}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "base": data.get("base", base_currency),
                    "date": date,
                    "rates": data.get("rates", {}).get(date, {}),
                    "source": "exchangerate-api.io"
                }
            else:
                return self._fallback_rates(base_currency, date)
        except Exception as e:
            print(f"Error fetching historical FX rates: {e}")
            return self._fallback_rates(base_currency, date)
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str, date: Optional[str] = None) -> Dict:
        """
        Convert currency amount
        """
        if date:
            rates_data = self.get_historical_rates(date, from_currency)
        else:
            rates_data = self.get_current_rates(from_currency)
        
        if rates_data.get("success") and rates_data.get("rates"):
            rates = rates_data["rates"]
            if to_currency in rates:
                converted_amount = amount * rates[to_currency]
                return {
                    "success": True,
                    "original_amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "converted_amount": round(converted_amount, 2),
                    "rate": rates[to_currency],
                    "date": rates_data.get("date", datetime.now().strftime("%Y-%m-%d"))
                }
        
        return {
            "success": False,
            "error": "Currency conversion failed"
        }
    
    def get_ato_rates(self, year: str, month: str) -> Dict:
        """
        Fetch FX rates from Australian Tax Office (ATO) website
        URL: https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-2026-financial-year
        """
        try:
            # ATO URL format - need to construct based on financial year
            # For 2026 financial year (July 2025 - June 2026)
            financial_year = int(year) if int(month) >= 7 else int(year) - 1
            
            # Try different URL patterns
            urls = [
                f"https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-{financial_year}-financial-year",
                f"https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-{financial_year + 1}-financial-year",
                "https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-2026-financial-year",
                "https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-2025-financial-year"
            ]
            
            rates = {}
            for url in urls:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5'
                    }
                    response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for tables with FX rates
                        tables = soup.find_all('table')
                        
                        # Also look for divs with rate information
                        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                                     'July', 'August', 'September', 'October', 'November', 'December']
                        month_name = month_names[int(month) - 1]
                        month_short = month_name[:3]
                        
                        for table in tables:
                            rows = table.find_all('tr')
                            
                            for row in rows:
                                cells = row.find_all(['td', 'th'])
                                if len(cells) >= 2:
                                    # Check if this row contains the month we're looking for
                                    row_text = ' '.join([cell.get_text().strip() for cell in cells]).lower()
                                    
                                    # Look for month indicators
                                    if (month_name.lower() in row_text or 
                                        month_short.lower() in row_text or 
                                        month in row_text or
                                        f"{year}-{month}" in row_text):
                                        
                                        # Extract currency and rate from this row or following rows
                                        currency = cells[0].get_text().strip().upper()
                                        rate_text = cells[1].get_text().strip() if len(cells) > 1 else ""
                                        
                                        # Extract numeric rate
                                        rate_match = re.search(r'[\d.]+', rate_text.replace(',', ''))
                                        if rate_match and len(currency) <= 5 and currency.isalpha():
                                            try:
                                                rate = float(rate_match.group())
                                                if 0.001 < rate < 100000:  # Reasonable range
                                                    rates[currency] = rate
                                            except:
                                                pass
                                    
                                    # Also try to extract any currency codes and rates
                                    if len(cells) >= 2:
                                        currency_candidate = cells[0].get_text().strip().upper()
                                        rate_candidate = cells[1].get_text().strip()
                                        
                                        if (len(currency_candidate) == 3 and currency_candidate.isalpha() and
                                            re.match(r'^[\d.]+$', rate_candidate.replace(',', ''))):
                                            try:
                                                rate = float(rate_candidate.replace(',', ''))
                                                if 0.001 < rate < 100000:
                                                    rates[currency_candidate] = rate
                                            except:
                                                pass
                        
                        if rates:
                            break
                except Exception as e:
                    print(f"Error fetching from {url}: {e}")
                    continue
            
            if rates:
                return {
                    "success": True,
                    "base": "AUD",
                    "date": f"{year}-{month}",
                    "rates": rates,
                    "source": "ATO (Australian Tax Office)"
                }
            else:
                # Return fallback rates with note
                return self._fallback_ato_rates(year, month)
                
        except Exception as e:
            print(f"Error fetching ATO rates: {e}")
            return self._fallback_ato_rates(year, month)
    
    def _fallback_ato_rates(self, year: str, month: str) -> Dict:
        """
        Fallback ATO rates (sample data based on typical ATO rates)
        Note: These are sample rates. For production, implement proper ATO API integration
        """
        # Sample ATO rates (AUD per unit of foreign currency)
        # These approximate typical ATO monthly rates
        base_rates = {
            "USD": 0.65,
            "EUR": 0.60,
            "GBP": 0.52,
            "JPY": 97.50,
            "CNY": 4.70,
            "HKD": 5.08,
            "SGD": 0.88,
            "NZD": 1.08,
            "CAD": 0.89,
            "CHF": 0.58,
            "INR": 54.20,
            "KRW": 850.00,
            "THB": 23.50,
            "MYR": 3.05,
            "IDR": 10250.00,
            "PHP": 36.50,
            "VND": 16200.00,
            "AUD": 1.00,
            "BRL": 3.25,
            "MXN": 11.20,
            "ZAR": 12.15,
            "SEK": 6.85,
            "NOK": 6.95,
            "DKK": 4.50,
            "PLN": 2.60,
            "CZK": 14.80,
            "HUF": 230.00,
            "RUB": 58.50,
            "TRY": 21.00,
            "AED": 2.39,
            "SAR": 2.44,
            "ILS": 2.40,
            "BGN": 1.17,
            "RON": 3.00
        }
        
        return {
            "success": True,
            "base": "AUD",
            "date": f"{year}-{month}",
            "rates": base_rates,
            "source": "fallback",
            "note": f"Using fallback rates for {month}/{year}. ATO website scraping may need adjustment. Visit https://www.ato.gov.au/tax-rates-and-codes/foreign-exchange-rates-monthly-2026-financial-year for official rates."
        }

    def _fallback_rates(self, base_currency: str = "USD", date: Optional[str] = None) -> Dict:
        """
        Fallback rates if API fails (sample rates)
        """
        # Sample rates (should be replaced with actual API)
        common_rates = {
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 149.50,
            "CNY": 7.25,
            "AUD": 1.52,
            "CAD": 1.35,
            "CHF": 0.88,
            "USD": 1.0
        }
        
        return {
            "success": True,
            "base": base_currency,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "rates": common_rates,
            "source": "fallback",
            "note": "Using fallback rates. Set EXCHANGE_RATE_API_KEY in .env for live rates."
        }

