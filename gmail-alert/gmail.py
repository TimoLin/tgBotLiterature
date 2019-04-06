from __future__ import print_function
import pickle
import os.path
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors, discovery
import base64
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

readedThreads = []

class Message:
    def __init__(self, _titles, _hrefs, _authors, _abstracts, _keyword):
        self.keyword = _keyword
        self.msg = []
        for n in range(len(_titles)):
            self.msg.append( self.msgMDWrapper(_titles[n], _hrefs[n], _authors[n], _abstracts[n]))

    def msgMDWrapper(self, title, href, author, abstract):
        """
        Wrap the message to markdown format
        """
        header = '['+title+']' + '('+href+')' +'\n'
        header += '*'+author +'*'+'\n'
        header += abstract 
        return(header)
    def msgHTMLWrapper(self, title, href, author, abstract):
        """
        No need to implement
        Wrap the message to html format
        """
        
#def main():
def getGmailMsg(n_msgs):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    global readedThreads

    # silence annoying log info
    logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_file = '../gmail-alert/token.pickle'
    cred_file  = '../gmail-alert/credentials.json'
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    
    # load readed thread id
    id_file = '../gmail-alert/threadId.pickle'
    if os.path.exists(id_file):
        with open(id_file, 'rb') as f:
            readedThreads = pickle.load(f)
            print(readedThreads)
    else:
        readedThreads = []

    label_liter = "LITER"

    liter_id = getLableId(service, label_liter)

    tgMsg = []

    if (liter_id == "100"):
        print("Can't get Gmail labels")
    elif (liter_id == "200"):
        print("Can't find the given label in the label list.\nPlease check your labels")
    else:
        threads = getThreads(service, liter_id)
        threads_ids = getThreadIds(threads)
        if len(threads_ids ) > 0:
            if n_msgs == 0:
                # only handle the latest literature tracking email
                n_range = 1
            elif n_msgs == -1:
                # handle all the emails
                n_range = len(threads_ids)
                if (n_range) > 10:
                    n_range = 10
            elif n_msgs > 0:
                # handle the first n_msgs emails
                n_range = min(n_msgs, len(threads_ids))
            else:
                logger.info(" I can't believe you give me a non-number: %s !", n_msgs)
                
            for n in range(n_range):
                readedThreads.append(threads_ids[n])
                keyword, content = getContent(service, threads_ids[n])
                titles, hrefs, authors, abstracts = parserContent(content) 
                tgMsg.append(Message(titles, hrefs, authors, abstracts, keyword))
    
    # save readed thread_id
    with open(id_file, 'wb') as f:
        pickle.dump(readedThreads, f)


    return tgMsg

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
        results = service.users().threads().list(userId='me',labelIds=label_id).execute()
        threads = []
        if 'threads' in results:
            threads.extend(results['threads'])
    
        while 'nextPageToken' in results:
            page_token = results['nextPageToken']
            results = service.users().threads().list(userId='me',labelIds=label_id, 
                    pageToken=page_token).execute()
            threads.extend(results['threads'])
        return threads
    except errors.HttpError as error:
        print("An error occured: {error}")

def getThreadIds(threads):
    threads_ids = []
    for thread in threads:
        thread_id = thread['id']
        if thread_id not in readedThreads:
            threads_ids.append(thread_id)
    return threads_ids

def getContent(service, thread_id):
    try: 
        results = service.users().threads().get(userId='me',id=thread_id).execute()

        # try to find keywords
        headers = results['messages'][0]['payload']['headers']
        for header in headers:
            if header['name'] == 'Subject':
                keyword = header['value']

        # get E-mail's content
        msg = results['messages'][0]['payload']['body']['data']
        # base64 decode
        content = base64.urlsafe_b64decode(msg.encode('ASCII')) 
        return keyword, content
    except errors.HttpError as error:
        print(f"An error occured: {error}")


def parserContent(content):
    # parse the content using BeautifulSoup
    soup = BeautifulSoup(content,'html.parser')

    _titles = soup.find_all('a','gse_alrt_title')
    _authors = soup.find_all('div',attrs={"style":"color:#006621"})
    _abstracts = soup.find_all('div', 'gse_alrt_sni')

    # check data, let _titles as base (which exists all the time)
    # find the missing location and fill the missing content with blank
    if len(_authors) < len(_titles):
        for n, _title in enumerate(_titles):
            _title_parent = _title.parent
            _title_next = _title_parent.next_sibling
            if (not _title_next.has_attr('style')) or ('color:#006621' not in _title_next['style']):
                no_author = "<div class='gse_alrt_sni'>No authors</div>"
                _authors.insert(n, BeautifulSoup(no_author,'html.parser'))
    if len(_abstracts) < len(_titles):
        for n, _title in enumerate(_titles):
            _title_parent = _title.parent
            _title_next_next = _title_parent.next_sibling.next_sibling
            if (not _title_next_next.has_attr('class')) or ('gse_alrt_sni' not in _title_next_next['class']):
                no_abs = "<div class='gse_alrt_sni'>No abstract</div>"
                _abstracts.insert(n, BeautifulSoup(no_abs,'html.parser'))
    
    titles = []
    hrefs = []
    authors = []
    abstracts = []
    
    # get the items' plain text
    for n in range(len(_titles)):
        titles.append(_titles[n].text)
        hrefs.append(_titles[n]['href'])
        authors.append(_authors[n].text)
        abstracts.append(_abstracts[n].text)
    return titles, hrefs, authors, abstracts


def msgWrapper(titles, href, authors, abstracts):
    # wrap the contents to a msg
    msg = []
    #for n in range(len(titles)):
        #msg = 


if __name__ == '__main__':
    main()
    
