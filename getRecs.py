import requests
from urllib.parse import urlencode
import time
import os
import os.path
from os import path
from datetime import datetime
from pytz import timezone
import pytz
import tzlocal

months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
	'07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

def navigate(url):
	#print('Navigated to: ',url)
	while (True):
		try:
			response = requests.get(url, auth=(user, pwd))
			return response
		except:
			time.sleep(60)
			
def searchRecURL(dict):
	for element in dict['comments']:
		try:
			return element['data']['recording_url']
		except:
			continue
	raise Exception("Could not find recording URL")
	
def reformatDate(date):
	date = date.replace('T', ' ') # Date
	date = date.replace('Z', '')
	dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
	local_tz = tzlocal.get_localzone()
	dt = dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
	hours = int(dt.strftime('%H'))
	if (hours >= 12):
		time = 'PM'
		if (hours != 12):
			hours = hours - 12
	else:
		time = 'AM'
	return dt.strftime('%Y-%m-%d {}-%M{}').format(hours, time)
	
def reformatPhone(phone):
	return phone.replace(' ', '', 2)	


user = [YourEmailAddress] + '/token'
pwd = [YourAPIKey]

url = 'https://lislv.zendesk.com/api/v2/views/360126690174/execute.json?page=12&sort_by=status&sort_order=desc'
finished = False
onGoing = []
count = 0

# loop through all tickets that are not archived yet
while(not finished):
	# Set the request parameters
	# + urlencode(params)
	response = navigate(url)
	data = response.json()
	
	# loop through each ticket in json result (100 per request)	
	for ticket in data['rows']:
		count = count + 1
		ti = ticket['ticket_id']
		try:
			cc = ticket['custom_fields'][0]['name'] # company code
		except:
			print('No Custom Field')
			cc = 'UNKNOWN'
		try:
			ba = ticket['custom_fields'][1]['value'] if ticket['custom_fields'][1]['value'] != 'N/A' else 'noBA' # BA number
		except:
			ba = 'noBA'
			
		while(True):
			try:
				pn = reformatPhone(ticket['via']['source']['from']['formatted_phone']) # phone number
				break
			except:
				print('Could not find phone number immediately')
				
		cr = reformatDate(ticket['created'])
		month = cr[5:7]
		year = cr[:4]
		print(cr, ' | ', months[month], year)
		
		if (os.path.isfile('Company_Codes/' + cc + '/' + months[month] + ' ' + year + '/' + ba + '__' + pn + '__' + cr + '.mp3')):
			print('file already exists')
			continue
		
		print('processing ticket: ', ti,' | ', cc,' | ', ba, ' | ', pn, ' | ', cr)
		# new request for ticket
		ticketResponse = navigate('https://lislv.zendesk.com/api/v2/tickets/' + str(ti) + '/comments.json')
		ticketData = ticketResponse.json()
		try:
			recordingUrl = searchRecURL(ticketData)
		except:
			print('No recording attached yet')
			onGoing.append(ti)
			print('Done with processing: ', ti, ' || ', ticket['ticket']['status'], ' || ', 'Count: ', count)
			continue
		# new request for recording
		recordingResponse = navigate(recordingUrl)
		# create directory of company code if it does not exist yet
		try:
			open('Company_Codes/' + cc + '/' + months[month] + ' ' + year + '/' + ba + '__' + pn + '__' + cr + '.mp3', 'wb').write(recordingResponse.content)
		except:
			if (not path.exists('Company_Codes/' + cc)):
				os.mkdir('Company_Codes/' + cc)
			os.mkdir('Company_Codes/' + cc + '/' + months[month] + ' ' + year)	
			open('Company_Codes/' + cc + '/' + months[month] + ' ' + year + '/' + ba + '__' + pn + '__' + cr + '.mp3', 'wb').write(recordingResponse.content)
		print('Done with processing: ', ti, ' || ', ticket['ticket']['status'], ' || ', 'Count: ', count)

	url = data['next_page']
	print('----------Next Page----------')
	print(onGoing)
	if (url is not None):
		time.sleep(20)
	else:
		finished = True
print('Done with loop')
exit()