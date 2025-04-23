import sqlite3
import requests
from bs4 import BeautifulSoup

def scrape_and_update_db(db_path):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch properties with links
    cursor.execute("SELECT id, link FROM properties WHERE link IS NOT NULL")
    properties = cursor.fetchall()

    for prop in properties:
        prop_id, link = prop
        try:
            # Fetch HTML content
            full_link = "https://www.bayut.com" + link

            response = requests.get(full_link, timeout=10)
            response.raise_for_status()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract required content (modify selector based on needs)

            sc = "N/A"
            service_charge_spans = soup.find_all('span', class_='_2fdf7fc5', attrs={'aria-label': 'Service charges'})

            # Debugging: Check if we found any matching elements
            print(f"Found {len(service_charge_spans)} service charge elements")
            for span in service_charge_spans:
                print(span)  # Print each span to inspect

            # If you find the correct span, proceed with extraction
            if service_charge_spans:
                service_charge_span = service_charge_spans[0]  # Assuming the first match is the correct one
                print(service_charge_span)

                # Find the parent div containing the price
                parent_div = service_charge_span.find_parent('div', class_='f1fcc55a')
                if parent_div:
                    price_div = parent_div.find('div', class_='_2923a568')
                    if price_div:
                        sc = price_div.get_text(strip=True).replace("AED", "").strip()
                        print(f"Service charge: {sc}")
                    else:
                        print("Price div not found")
                else:
                    print("Parent div not found")
            else:
                print("No service charge span found")




            ownership = soup.find('div', class_='_3342dc3d').text.strip() if soup.find('div', class_='_3342dc3d') else 'N/A'
            yofcom = soup.find('div', class_='_3342dc3d').text.strip() if soup.find('div', class_='_3342dc3d') else 'N/A'

            # Update database
            cursor.execute("UPDATE properties SET sc = ?, ownership = ?, yofcom = ? WHERE id = ?", (sc, ownership, yofcom, prop_id))

            conn.commit()
            print(f"Updated ID {prop_id} with data: sc={sc}, ownership={ownership}, yofcom={yofcom}")


        except requests.RequestException as e:
            print(f"Failed to fetch {full_link}: {e}")

    # Close connection
    conn.close()

# Run script
scrape_and_update_db("properties.db")
