import requests
from bs4 import BeautifulSoup
from firebase import firebase

# firebase connect
firebase = firebase.FirebaseApplication("https://hacettepeyemekmenusu-default-rtdb.europe-west1.firebasedatabase.app/")

# url response
url = 'https://sksdb.hacettepe.edu.tr/bidbnew/grid.php?parameters=qbapuL6kmaScnHaup8DEm1B8maqturW8haidnI%2Bsq8F%2FgY1fiZWdnKShq8bTlaOZXq%2BmwWjLzJyPlpmcpbm1kNORopmYXI22tLzHXKmVnZykwafFhImVnZWipbq0f8qRnJ%2BioF6go7%2FOoplWqKSltLa805yVj5agnsGmkNORopmYXam2qbi%2Bo5mqlXRrinJdf1BQUFBXWXVMc39QUA%3D%3D'
response = requests.get(url)

# html parse
soup = BeautifulSoup(response.content, 'html.parser')

# yemek menulerinin siteden ayristirilmasi
menu_table = soup.find('table', class_='table table-bordered table-sm')
menu_items = menu_table.find_all('tr')

# menulerinin ozellestirilip veritabanina push edilmesi
for item in menu_items:
    menu_data = {}

    #date
    date = item.find('div', class_='popular').text.split()[1]
    menu_data['date'] = date

    #calorie
    calorie = item.find_all('p')[1].text.split('Kalori : ')[1]
    menu_data['calorie'] = calorie

    #meal
    meal = str(item.find_all('p')[1]).split('<br/>')[1:2].__str__().split('<br>')+str(item.find_all('p')[1]).split('<br/>')[2:-2]
    meal = [m.lstrip(' ').lstrip("['").rstrip("']") for m in meal]
    menu_data['meal'] = meal

    #push
    firebase.put("/", name=date.replace(".", "-"), data=menu_data)


#ornek cagri
#print(firebase.get('/', name="1-04-2023"))
