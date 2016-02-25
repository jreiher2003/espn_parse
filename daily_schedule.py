from bs4 import BeautifulSoup as bsoup
import requests as rq



# def daily_mu(date):

# 	return [away, home]


url = "http://espn.go.com/nba/schedule"
r = rq.get(url)
soup = bsoup(r.content)
trs = soup.find_all("tr", class_=True)
for tr in trs:
	tds = tr.find_all("td")[0]
	date = tr.find_all("stathead")
	# print date
	for td in tds:
		print td
		# tdate = td.find_all('colspan')

