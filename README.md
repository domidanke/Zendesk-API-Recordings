# ZendeskAPIRecordings
Retrieving Call Recordings  from Zendesk API for business-related purposes and data analytics

![alt text](https://github.com/domidanke/ZendeskAPIRecordings/master/logo.png?raw=true)

Zendesk Inc. is a customer service software company headquartered in San Francisco, California, USA, founded in 2007 in Copenhagen, Denmark. Zendesk has 2,000 employees and serves 119,000 paying customers in 150 countries and territories as of 2017. 
Customer and team experience can be enhanced by building powerful products on top of a Zendesk product with APIs, apps, and mobile SDKs.

This Repo holds Python files using API requests to retrieve Customer Call Recordings and store them systematically based on name, client, and date. This well-working version is currently used at my Software Service Company integrated into a task scheduler that runs the script every 24 hours to retrieve the most recent recordings and store them in the correct directories in one of our servers. I created the scripts at the beginning of May 2020.

Of course, the variables and methodology is biased towards what my company needs. 

Within Zendesk, I, as an agent user, created a View that contains all tickets holding voice recordings.
My script requests data from that view holding all tickets with their IDs. After retrieving the ticket ID, I am requesting specific data about that ticket to retrieve a URL from the 'recording_url'-key of the json decoded data. The last request is to access and download the actual MP3 file containing the recording and store it in the corresponding directory. This loop continues until the last ticket in the view, or until the data property of a ticket is longer ago than 24 hours.

I provided two files to initially retrieve all recordings, and to continue retrieving daily data.
