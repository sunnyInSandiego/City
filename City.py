import requests
import json
from itertools import permutations

API_KEY = "a1ba193c4f709407c362ce7cef7bebb5"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
	"""Five cities and the highest temperature"""
	def __init__(self, name, temperatures):
		self.name = name
		self.temps = temperatures

	def get_temperature(self, day):
		"""The highest temperature for each city"""
		return self.temps[day]

	def __str__(self):
		"""name of the city"""
		return self.name


class Route:
	"""Finds the best route for the five cities"""
	def __init__(self, cities):
		self.cities = cities

	def get_avg_temp(self):
		"""Finds the average temperature for all five cities"""
		temp = 0
		for day, city in enumerate(self.cities):
			temp += city.get_temperature(day) / len(self.cities)
		return temp

	def __str__(self):
		"""Iterates through each city and puts the cities into format output"""
		name = ""
		for city in self.cities:
			name = name + city.name + ":"
		return name


def fetch_weather(id):
	# request parameter(s): Start with '?'
	# separate name and value with '='
	# multiple parameter name value pairs are separate with '&'
	query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
	request_url = WS_URL + query_string
	print("Request URL: ", request_url)
	response = requests.get(request_url)
	try:
		if response.status_code == 200:
			d = response.json()
			city_name = d["city"]['name']
			lst = d['list']
			tmp_list = []
			[tmp_list.append(max([lst[j]["main"]["temp_max"] for j in [x for x in range(len(lst)) if x // 8 == i]])) for i in range(len(lst) // 8)]
			return city_name, tmp_list
		else:
			print("How should I know?")
			return None, None

	except Exception as e:
		print(e)


if __name__ == "__main__":
	id_list = json.loads(open("cities.json").read())
	cities = []
	for id in id_list:
		city_name, temp_list = fetch_weather(id)
		cities.append(City(city_name, temp_list))

	routes = [Route(p) for p in list(permutations(cities))]

	routeTemps = [r.get_avg_temp() for r in routes]

	argmin = 0
	temp_min = routeTemps[0]
	for i, t in enumerate(routeTemps):
		if t < temp_min:
			argmin = i
			temp_min = t
	print("The lowest average temperature high is {} for the route {}".format(routeTemps[argmin], routes[argmin]))

