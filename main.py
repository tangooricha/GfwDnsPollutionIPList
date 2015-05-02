import sqlite3
import datetime
import DNS

domainName = "twitter.com"
nameServer = ["12.12.12.12"]

if __name__ == '__main__':
	conn = sqlite3.connect('log.sqlite')
	conn.isolation_level = None
	c = conn.cursor()
	c.execute("create table if not exists log(id integer primary key autoincrement, ip text, firstdatetime text, lastdatetime text, count integer)")

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
			c.execute("insert into log(ip, firstdatetime, lastdatetime, count) values(?, ?, ?, ?)", (ip, datetime.datetime.now(), datetime.datetime.now(), 1))
		elif row[1] != ip:
			c.execute("insert into log(ip, firstdatetime, lastdatetime, count) values(?, ?, ?, ?)", (ip, datetime.datetime.now(), datetime.datetime.now(), 1))
		else:
			counter = int(row[4]) + 1
			c.execute("update log set lastdatetime = ?, count = ? where ip = ?", (datetime.datetime.now(), counter, ip))
			print ip + ": " + str(counter)