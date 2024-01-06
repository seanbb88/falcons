import requests
from bs4 import BeautifulSoup
from database import db 
from models.models import Player, Salary
from utils.loaders import print_progress_dots

class PlayerContract:
    def __init__(self, name, team, year_signed, total_years, total_value, average_per_year, guaranteed, position):
        self.name = name
        self.team = team
        self.year_signed = year_signed
        self.total_years = total_years
        self.total_value = total_value
        self.average_per_year = average_per_year
        self.guaranteed = guaranteed
        self.position = position


scrape_dictionary = {
    "QB": "quarterback", 
    "RB": "running-back", 
    "WR": "wide-receiver", 
    "TE": "tight-end", 
    "LT": "left-tackle", 
    "LG": "left-guard", 
    "C": "center", 
    "RG": 'right-guard', 
    "RT": 'right-tackle', 
    "DL": 'interior-defensive-line', 
    "LB": 'linebacker', 
    "S": 'safety', 
    "CB": "cornerback", 
    "K": "kicker", 
    "P": 'punter'
}

def scrape_website(url, position):
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            table = soup.find('table', {'class': 'position-table'})
            
            if table:
                rows = table.find_all('tr')
                
                contract_objects = []
                
                for row in rows:
                    cells = row.find_all('td')
                    
                    if len(cells) >= 6:
                        name = cells[0].get_text()
                        team = cells[1].get_text()
                        year_signed = cells[2].get_text()
                        total_years = cells[3].get_text()
                        total_value = cells[5].get_text()
                        average_per_year = cells[6].get_text()
                        guaranteed = cells[7].get_text()

                        contract = PlayerContract(name, team, year_signed, total_years, total_value, average_per_year, guaranteed, position)
                        contract_objects.append(contract)

                return contract_objects
            else:
                print("Table not found on the web page.")
            
        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        
def skip_seeding():
    total_records = db.query(Salary).count()
    return total_records > 0
        
def gather_player_salary_information_and_seed():
    print("SCRAPING AND SAVING PLAYER SALARY DATA")
    print_progress_dots(12)
    salary_objects = [] 
    
    if skip_seeding():
        print("Salary data already exists. Skipping the scrape.")
        return

    for position_key, url_end in scrape_dictionary.items():
        url = "https://overthecap.com/contract-history/" + url_end
        response = scrape_website(url, position_key)

        if response:
            for contract in response:
                player_name = contract.name
                player_in_db = db.query(Player).filter(Player.name == player_name).first()
                formatted_avp = contract.average_per_year.replace("$", "").replace(',', '')
                formatted_salary = contract.total_value.replace("$", "").replace(',', '')  # Use contract.total_value here
                formatted_guarantee = contract.guaranteed.replace("$", "").replace(',', '')  # Use contract.guaranteed here

                salary = Salary(
                    player_id=player_in_db.id if player_in_db is not None else None,
                    year_signed=contract.year_signed,
                    team=contract.team,
                    average_per_year=int(formatted_avp),
                    total_value=int(formatted_salary),
                    guaranteed=int(formatted_guarantee),
                    position=contract.position
                )
                salary_objects.append(salary) 

    db.add_all(salary_objects)
    db.commit()
   

if __name__ == "__main__":
    gather_player_salary_information_and_seed()
   
   
