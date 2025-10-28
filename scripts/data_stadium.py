# %%
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


# %%
def get_stadium():
    """
    Get MLB stadiums from wikipedia.org
    :return: html text
    """
    url = "https://en.wikipedia.org/wiki/List_of_current_Major_League_Baseball_stadiums"
    response = requests.get(url)
    return response.content


# %%
def to_stadium_df(html):
    """
    Extract data from html and convert into pandas DataFrame
    :param html: Stadium html string
    :return: Stadium info DataFrame
    """
    mlb = BeautifulSoup(html, features="lxml")

    # Finding the table containing the stadiums
    table = mlb.find("table", class_="wikitable")

    # Extracting the header, excluding the first column
    headers = []
    for th in table.find_all("th")[1:10]:
        headers.append(th.text.strip())

    name_col_data = []
    for th in table.find_all("th")[10:]:
        cleaned_name = th.text.strip().replace("‡", "").replace("†", "")
        name_col_data.append(cleaned_name)

    # Extracting the rows
    data = []
    for idx, tr in enumerate(table.find_all("tr")[1:]):  # Skip the header row
        row = []

        # Add the corresponding header data as the first column
        if idx < len(name_col_data):
            row.append(name_col_data[idx])

        # Extracting the data cells
        for td in tr.find_all("td")[1:]:  # Start from the second cell
            cell_data = td.text.strip()

            if "Capacity" in headers:
                cell_data = re.sub(r"\s*\[.*?]", "", cell_data)
                # Remove square brackets and contents

            if cell_data:  # Only add non-empty cells
                row.append(cell_data)

        # Only append non-empty rows
        if row:
            data.append(row)

    stadium_df = pd.DataFrame(data, columns=headers)  # Use the headers list

    return stadium_df
