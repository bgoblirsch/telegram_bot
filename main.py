import StringIO
import json
import logging
import random
import urllib
import urllib2

# Google app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

# FOAMbot API token
TOKEN = '564975990:AAEQTGShf74c0y2Ppu4MZnODjzmAoSkKihs'

# URL to call for message logs
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================
# Base Library, don't change

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


# List of Replies
reply_help = "The available commands are: \n /whitepaper - Whitepaper Information \n /overview - An Overview of FOAM \n /hardware - Hardware Information \n /pol - Proof of Location Protocol \n /csc - Crypto-Spatial Coordinate \n /siv - The Spatial Index & Visualizer Beta \n /tcr - Token Curated Registries for Geographic Points of Interest \n /dev - Developer Resources \n /team - Team and Office Information \n /rules"
reply_whitepaper = "FOAM Product Whitepaper: \nhttps://blog.foam.space/foam-white-paper-release-the-consensus-driven-map-of-the-world-da6da1b15325"
reply_hardware = "FOAM's hardware track will be slower moving than the token sale and mainnet launch of the Spaital Index and Curated Points of Interest. The team is working on the specifications with the goal of pushing the limits of off-the-shelf compatible hardware in order to make it easy to contribute to the network. Stay tuned for updates on hardware. \n \nFOAM will be utilizing Low-Power Wide-Area Networks (LPWAN). While FOAM will using a different software stack than LoRaWAN, you can find good documentation on and examples of LPWAN hardware on The Things Network website. \n \nhttps://www.thethingsnetwork.org/docs/"
reply_team = "FOAM's main office is located at the New Lab in New York City. FOAM also has office space at Full Node in Berlin. The core team currently consists of about 10 people. \nhttps://foam.space/company"
reply_pol = "An overview of FOAM's proof of location protocol: \nhttps://blog.foam.space/introduction-to-proof-of-location-6b4c77928022"
reply_siv = "You can learn about the Spatial Index here: \nhttps://blog.foam.space/the-spatial-index-9793f42c46c8 \n \nAnd you can test out the Spatial Index beta here: \nhttps://beta.foam.space/ \n \nYou will need Metamask installed in Chrome with funds on Rinkeby. \n \nYou can acquire funds for Rinkeby at https://faucet.rinkeby.io \n \nMake sure you on the Rinkeby Testnet when testing out the Spatial Index!"
reply_csc = "An overview of the Crypto-Spatial Coordinate: \nhttps://blog.foam.space/crypto-spatial-coordinates-fe0527816506"
reply_tcr = "Token Curated Registries for Geographic Points of Interest: \nhttps://blog.foam.space/foam-token-curated-registries-for-geographic-points-of-interest-60d3c043f183"
reply_dev = "The FOAM Developer Portal: \nhttps://developer.foam.space \n\nFOAM Gitter for developer discussion: \nhttps://gitter.im/f-o-a-m/Lobby"
reply_sale = "The FOAM sale has concluded! Thank you to everyone that participated and we look forward to building the consensus driven map of the world with our community! \nYou can see the results of the sale here: https://tokenfoundry.com/projects/foam"
reply_overview = "The Elements of FOAM Explained: \nhttps://youtu.be/LKb0y8z9TJg \n \nIntroduction to FOAM: \nhttps://blog.foam.space/introducing-the-foam-protocol-2598d2f71417"
# reply_reg = "You can find info about the FOAM token sale and register for it on the FOAM Project Page on Token Foundry's website. \n\nhttps://tokenfoundry.com/projects/foam"
reply_rules = '1. No offensive or explicit content \n2. FOAM related discussion only \n3. No spam, ads, or referrals \n4. No posting links without context or links to non-FOAM specific Telegram groups \n5. No speculation or "moon" talk \n6. No profanity \n7. No GIFs \n8. Be respecftul to each other \n \nIf you want to create a local community group, please let us know so we can add it to the list of acceptable links for our bot.'

whitelistedGroups = ['t.me/foamspace', 't.me/foamaustralia', 't.me/foamprotocol', 't.me/foamcalifornia', 't.me/foamportugal', 't.me/foamjapan', 't.me/foamfilipino', 't.me/foamfrance', 't.me/foamuk', 't.me/foamchina', 't.me/foamnetherlands', 't.me/foamtoronto', 't.me/foamcyprus', 't.me/foamgermany', 't.me/foambelgium', 't.me/foamphilippines', 't.me/foamindia', 't.me/foamnorway', 't.me/foamswusa', 't.me/foamsingapore', 't.me/foampoland', 't.me/foam_ru', 't.me/foammalaysia', 't.me/foamspain', 't.me/foamnyc', 't.me/foamsouthernus', 't.me/tokenfoundry', 't.me/foammidwestusa', 't.me/foamnz', 't.me/foamswitzerland', 't.me/foampnw', 'https://t.me/foam_us_mountainwest', 'https://t.me/foamrsa', 'https://t.me/foamgreece']

class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))
        url = ''
        fileName = ''
        update_id = body['update_id']
        try:
            message = body['message']
        except:
            message = body['edited_message']
        message_id = message.get('message_id')
        try:
            forward_from_chat = message.get('forward_from_chat')
            forward_from_chat_username = forward_from_chat['username']
            logging.info(forward_from_chat_username)
        except:
            logging.info('not a forward')
        try:
            entities = message.get('entities')
            for i in entities:
            	if 'url' in i:
            		url = i.get('url')
            logging.info(url)
        except:
            logging.info('no embedded text properties')
        try:
            document = message.get('document')
            fileName = document.get('file_name')
            logging.info(fileName)
        except:
            logging.info('no attached file')
        date = message.get('date')
        text = message.get('text')
        caption = message.get('caption')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            
 
        def reply(msg=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                })).read()
            else:
                logging.error('no msg specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)
        
        
        def deleteMsg():
            if message_id:
                resp = urllib2.urlopen(BASE_URL + 'deleteMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'message_id': str(message_id),
                })).read()
            #else:
            #    logging.error('no msg specified')
            #    resp = None
            
        def banUser():
            logging.info('banned user:')
            try:
                logging.info(fr['username'])
            except:
                logging.info('user had no username')
            resp = urllib2.urlopen(BASE_URL + 'kickChatMember', urllib.urlencode({
                'chat_id': str(chat_id),
                'user_id': str(fr['id']),
            })).read()
        

            
        # ==========================================================================
        
        # Lower user's message text
        if text:
            text = text.lower()   
                
        # if /command -> respond with correct response
        # *TO-DO* Replace with function and a dictionary to clean up code
        if text and text.startswith('/'):
            # When the help menu is called, and a user clicks on one of the commands, it appends "@FOAM_Protocol_bot" to the command
            # This checks for and removes that text
            if text.endswith('@foam_protocol_bot'):
                 text = text[:-18]
            if text == '/start':
                reply('Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/help' or text == '/menu':
                reply(reply_help)
                return
            elif text == '/whitepaper':
                reply(reply_whitepaper)
                return
            elif text == '/hardware':
                reply(reply_hardware)
                return
            elif text == '/team':
                reply(reply_team)
                return
            elif text == '/pol':
                reply(reply_pol)
                return
            elif text == '/csc':
                reply(reply_csc)
                return
            elif text == '/siv':
                reply(reply_siv)
                return
            elif text == '/tcr':
                reply(reply_tcr)
                return
            elif text == '/dev':
                reply(reply_dev)
                return
            elif text == '/overview':
                reply(reply_overview)
                return
            elif text == '/sale':
                reply(reply_sale)
                return
            elif text == '/rules':
                reply(reply_rules)
                return
            else:
                return
            
        # ===================================================================
        # Handle Spam
        # ===================================================================
        
        # To-Do: create a dictionary, that adds usernames (or IDs, probably IDs) as keys to the dictionary when a message is deleted by the bot with a starting value of 1
        # Each time a message is deleted dict['user'] += 1
        # if dict['user'] > 3: ban user
        
        # Reset message whitelist status
        whitelisted = False
        
        # Check if forwarded from common spam channels, delete message, and ban user
        if text:
            if '[forwarded from join @thecryptoadviser]' in text or '[forwarded from join @thecryptospace]' in text:
                try:
                    deleteMsg()
                    banUser()
                except:
                    logging.error('unable to ban user or delete message')
                return
            elif forward_from_chat and forward_from_chat == 'trend_crypto_news':
                try:
                    deleteMsg()
                    banUser()
                except:
                    logging.error('unable to ban user or delete message')
                return
        
        
        # Check if Ethereum address is in text
        if text and '0x' in text:
        	# variable to check if this was wrongly flagged for 0x protocol or FOAM Contract Address
            flagged = True
        	
            # reserved for whitelisting FOAM contract address
            #if '[foamAddress]' in text:
            #    flagged = False
            
            # remove punctuation
            t1 = text.replace('!', ' ')
            t2 = t1.replace('.', ' ')
            t3 = t2.replace('?', ' ')
            t4 = t3.replace(',', ' ')
            
            # FOAM Contract Address
            if '0x4946fcea7c692606e8908002e55a582af44ac121' in text:
                flagged = False
            
            
            # parse text
            parsedText = t4.split(' ')
            
            
            # check and ignore if text was flagged for 0x protocol
            for i in parsedText:
                if '0x' in i and len(i) == 2:
                    flagged = False
                #elif '0x' in i and len(i) >= 42:
                #    flagged = True
                    
            if flagged:
                try:
                    deleteMsg()
                    logging.info('message deleted')
                except:
                    logging.error('unable to delete message')
        
        
        # Check if file is attached and delete if it matches blacklisted file types
        if fileName and '.scr' in fileName:
            try:
                deleteMsg()
                banUser()
            except:
                logging.error('unable to delete file attachment or ban user')
        
        # Check if every message contains a link to a telegram group and delete the message if it's not in the whitelist
        if text and 'bit.ly' in text:
            if 'http://bit.ly/foammapuserguide' in text:
                pass
            else:
                try:
                    deleteMsg()
                    logging.info('message with bit.ly link deleted')
                except:
                    logging.error('unable to delete bit.ly message')
        if text and 'tinyurl.com' in text:
            try:
                deleteMsg()
                banUser()
                logging.info('message with tinyurl link deleted')
            except:
                logging.error('unable to delete tinyurl message')
        if text and 'owl.ly' in text:
            try:
                deleteMsg()
                banUser()
                logging.info('message with tinyurl link deleted')
            except:
                logging.error('unable to delete tinyurl message')
        if text and 'deck.ly' in text:
            try:
                deleteMsg()
                banUser()
                logging.info('message with tinyurl link deleted')
            except:
                logging.error('unable to delete tinyurl message')
        if text and '1url.cz' in text:
            try:
                deleteMsg()
                banUser()
                logging.info('message with tinyurl link deleted')
            except:
                logging.error('unable to delete tinyurl message')
                
        if text and 'telegra.ph' in text:
            try:
                deleteMsg()
                banUser()
                logging.info('deleted and banned')
            except:
                logging.info('faliled to delete')
                
        
        
        if text and 'medium.com/@foamprotocol' in text:
            try:
                deleteMsg()
                logging.info('medium deleted')
            except:
                logging.error('unable to delete')
            try:
                banUser()
                logging.info('banned user')
            except:
                logging.error('unable to ban')
        
        if text and 't.me/' in text:
            for item in whitelistedGroups:
                if item in text:
        	        whitelisted = True
            if whitelisted == False:
                try:
                    deleteMsg()
                    logging.info('message with Telegram link deleted')
                except:
                    logging.error('unable to delete message')
                return
        if url and 't.me/' in url:
            for item in whitelistedGroups:
                if item in url:
        	        whitelisted = True
            if whitelisted == False:
                try:
                    deleteMsg()
                    logging.info('message with Telegram link deleted')
                except:
                    logging.error('unable to delete message')
                return
        elif caption and 't.me/' in caption:
            for item in whitelistedGroups:
                if item in caption:
                    whitelisted = True
            if whitelisted == False:
                try:
                    deleteMsg()
                    logging.info('message with Telegram link deleted')
                except:
                    logging.error('unable to delete message')
                return
        elif caption and 'NEW L' in caption and 'ST ALERT' in caption:
            try:
                deleteMsg()
                logging.info('Binance Forwarded messaged deleted')
                banUser()
            except:
                logging.error('unable to delete forwarded message or ban user')
            return
        else:
            return    
            

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
