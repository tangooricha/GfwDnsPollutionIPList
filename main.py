import sqlite3
import datetime
import DNS

ipList = []
domainName = "twitter.com"
nameServer = ["12.12.12.12"]

if __name__ == '__main__':
	conn = sqlite3.connect('log.sqlite')
	conn.isolation_level = None
	c = conn.cursor()
	c.execute("create table if not exists log(id integer primary key autoincrement, ip text, datetime text)")

	for row in c.execute("select * from log"):
		ipList.append(row)

	DNS.DiscoverNameServers()
	request = DNS.DnsRequest(name=domainName, server=nameServer)

	while (True):
		try:
			response = request.req()
		except:
			pass
		ip = ""
		ip = response.answers[0]["data"]
		c.execute("select * from log where ip = ?", (ip,))
		row = c.fetchone()
		if row == None:
			c.execute("insert into log(ip, datetime) values(?, ?)", (ip, datetime.datetime.now()))
		elif row[1] != ip:
			c.execute("insert into log(ip, datetime) values(?, ?)", (ip, datetime.datetime.now()))
		else:
			pass