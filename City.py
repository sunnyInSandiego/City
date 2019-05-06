import requests
import json
from itertools import permutations

API_KEY = "a1ba193c4f709407c362ce7cef7bebb5"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
	def __init__(self, name, temperatures):
		self.name = name
		self.temps = temperatures

	def get_temperature(self, day):
		return self.temps[day]

	def __str__(self):
		return self.name


class Route:
	def __init__(self, cities):
		self.cities = cities

	def cost(self):
		return self.getAvgTemp()

	def __str__(self):
		name = ""
		for city in self.cities:
			name = name + city.name + ":"
		return name

	def getAvgTemp(self):
		avgTemp = 0
		for day, city in enumerate(self.cities):
			avgTemp += city.get_temperature(day) / len(self.cities)
		return avgTemp


def fetch_weather(id):
	# request parameter(s): Start with '?'
	# separate name and value with '='
	# multiple parameter name value pairs are separate with '&'
	query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
	request_url = WS_URL + query_string
	print("Request URL: ", request_url)
	response = requests.get(request_url)
	if response.status_code == 200:
		d = response.json()
		city_name = d["city"]['name']
		lst = d['list']
		tmp_list = []
		for i in range(len(lst) // 8):
			li = [x for x in range(len(lst)) if x // 8 == i]
			tmp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
		return city_name, tmp_list
	else:
		print("How should I know?")
		return None, None


if __name__ == "__main__":
	id_list = json.loads(open("cities.json").read())
	cities = []
	for id in id_list:
		city_name, tmp_list = fetch_weather(id)
		cities.append(City(city_name, tmp_list))

	routes = [Route(p) for p in list(permutations(cities))]

	routeTemps = [r.getAvgTemp() for r in routes]

	argmin = 0
	tempmin = routeTemps[0]
	for i, t in enumerate(routeTemps):
		if t < tempmin:
			argmin = i
			tempmin = t
	print("The lowest average temperature high is {} for the route {}".format(routeTemps[argmin], routes[argmin]))

