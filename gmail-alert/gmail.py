from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class Message:
    def __init__(self, _titles, _hrefs, _authors, _abstracts, _keyword):
        self.keyword = _keyword
        self.message = []
        for n in len(_titles):
            self.msg.extend( msgMDWrapper(_titles[n], _hrefs[n], _authors[n], _abstracts[n]))

    def msgMDWrapper(title, href, author, abstract):
        """
        Wrap the message to markdown format
        """
        header = '['+title+']' + '('+href+')' +'\n'
        header += author +'\n'
        header += abstract 
    def msgHTMLWrapper(title, href, author, abstract):
        """
        To be implemented
        Wrap the message to html format
        """
        #soup = BeautifulSoup()
        
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    
    label_liter = "LITER"

    liter_id = getLableId(service, label_liter)
    if (liter_id == "100"):
        print("Can't get Gmail labels")
    elif (liter_id == "200"):
        print("Can't find the given label in the label list.\nPlease check your labels")
    else:
        threads = getThreads(service, liter_id)
        threads_ids = getThreadIds(threads)
        if len(threads_ids ) > 0:
            tgMsg = []
            for n in range(len(threads_ids)):
                keyword, content = getContent(service, threads_ids[n])
                titles, hrefs, authors, abstracts = parserContent(content) 
                tgMsg.extend(Message(titles, hrefs, authors, abstracts))

def getLableId(service, label_liter):
    """
    return code: (string)
        100: Can't get Gmails labels
        200: Can't find the given label in the label list
    """
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels',[])

    if not labels:
        return "100"
    else:
        found_label = False
        for label in labels:
            if (label['name'] == label_liter):
                found_label = True
                return (label['id'])
        if (found_label == False):
            return "200"

def getThreads(service, label_id):
    try:
        results = service.users().threads().list(userId='me',labelIds=liter_id).execute()
        threads = []
        if 'threads' in results:
            threads.extend(results['threads'])
    
        while 'nextPageToken' in results:
            page_token = results['nextPageToken']
            results = service.users().threads().list(userId='me',labelIds=liter_id, 
                    pageToken=page_token).execute()
            threads.extend(results['threads'])
        return threads
    except errors.HttpError, error:
        print("An error occured: %s", error)

def getThreadIds(threads):

    for thread in threads:
        thread_id = thread['id']
        if thread_id not in readedThreads:
            threads_ids.extend(thread['id'])
    return threads_ids

def getContent(service, thread_id):
    try: 
        results = service.users().threads().get(userId='me',id=thread_id).execute()

        # try to find keywords
        headers = results['messages'][0]['payload']['headers']
        for header in headers:
            if header['name'] == 'Subject':
                keyword = headers['value']

        # get E-mail's content
        msg = results['messages'][0]['payload']['body']['data']
        # base64 decode
        content = base64.urlsafe_b64decode(msg.encode('ASCII')) 
        return keyword, content

def parserContent(content):
    # parse the content using BeautifulSoup
    soup = BeautifulSoup(content,'html.parser')   

    _titles = soup.find_all('a','gse_alrt_title')
    _authors = soup.find_all('div',attrs={"style":"color:#006621"})
    _abstracts = soup.find_all('div', 'gse_alrt_sni')
    
    titles = []
    hrefs = []
    authors = []
    abstracts = []
    
    # get the items' plain text
    for n in range(len(_titles)):
        titles.extend(_titles[n].text)
        hrefs.extend(_titles[n]['href'])
        authors.extend(_authors[n].text)
        abstracts.extend(_abstracts[n].text)
    
    return titles, hrefs, authors, abstracts

def msgWrapper(titles, href, authors, abstracts):
    # wrap the contents to a msg
    msg = []
    #for n in range(len(titles)):
        #msg = 


if __name__ == '__main__':
    main()
    
