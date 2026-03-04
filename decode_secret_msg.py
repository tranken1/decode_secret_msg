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

    # verify if we extracted data points
    if not data_points:
        print("No data found. Check URL.")
        return

    # print statement to check if the data was extracted
    print(f"Successfully extracted {len(data_points)} data points.")
    
    # build grid with height = max_y + 1 and width = max_x + 1
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # use dictionary to fill grid
    for (x, y), char in data_points.items():
        grid[y][x] = char

    for y in range(max_y, -1, -1):
        print("".join(grid[y]))

if __name__ == "__main__":
    user_url = input("Enter Google Doc URL: ").strip()
    if user_url:
        decode_secret_msg(user_url)
    else:
        print("No URL found.")