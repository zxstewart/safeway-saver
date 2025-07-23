# Safeway Saver

A Flask web app that helps users save money by:

- Scraping current Safeway grocery deals (https://www.safeway.com/weeklyad)
- Matching those deals to the user's weekly shopping list
- Recommending sale items they've purchased before
- Recommending substitutions based on similar items on sale

This project runs entirely locally and requires no signup, payment, or database. 
(Final version will be hosted using Render and SQLite)

---

## Features

- Input weekly grocery list
- Find out which list items are on sale
- Get suggestions for sale items that have been bought before
- Automatically track past purchases for better future recommendations

---

## Tech Stack

- Python 3
- Flask
- BeautifulSoup (placeholder for web scraping)
- HTML/CSS (basic frontend)
- JSON for local user history
