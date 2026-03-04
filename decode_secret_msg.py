import requests
from bs4 import BeautifulSoup

def decode_secret_msg(url):
    # fetch page and error handling
    response = requests.get(url)
    response.raise_for_status()

    # parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table')
    rows = table.find_all('tr')

    # dictionary to hold data points
    data_points = {}

    # track boundaries of grid
    max_x = 0
    max_y = 0

    for row in rows:
        # extract table data (td) cells
        cells = row.find_all('td')
        
        # rows must have 3 columns: X, Char, Y
        if len(cells) == 3:
            try:
                x = int(cells[0].get_text().strip())
                char = cells[1].get_text().strip()
                y = int(cells[2].get_text().strip())
                
                # store data using coordinates as key
                data_points[(x, y)] = char

                # update boundaries
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

            except ValueError:
                continue

    # Let's verify we got something
    if not data_points:
        print("No data found. Check URL.")
        return

    print(f"Successfully extracted {len(data_points)} data points.")
    
    # --- NEXT WE WILL BUILD THE GRID HERE ---
    pass

if __name__ == "__main__":
    test_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    decode_secret_msg(test_url)