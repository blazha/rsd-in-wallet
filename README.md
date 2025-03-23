## Overview
It is REST API in Python that allows users to track the current Serbian dinar (RSD) value of their money held in different
foreign currencies.

### Features
- Wallet Management: Users can define how much money they have in various foreign currencies.
- Real-Time Currency Conversion: The system will convert these amounts into their RSD equivalent using current exchange.
- RSD Value Calculation: For each currency in the user’s wallet, the system will return its RSD value and the total RSD amount of all
currencies combined.

### Example
If a user has:
- 100 EUR
- 20 USD
- 8000 JPY

And the exchange rates are:
- 1 EUR = 4.25 RSD
- 1 USD = 3.85 RSD
- 1 JPY = 0.027 RSD

The system will return:
- 425 RSD for EUR
- 77 RSD for USD
- 216 RSD for JPY
- 718 RSD total

### Endpoints:
- TBD