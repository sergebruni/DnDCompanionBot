import os

from firebase import firebase

FIREBASE_API_SECRET = os.environ.get('FIREBASE_API_SECRET')

class Database:
    def __init__(self):
        self.firebase_db = firebase.FirebaseApplication('https://dndbot-c2cad.firebaseio.com', authentication=None)

    # TODO: Only active campaigns
    def get_campaign(self, chat_id):
        results = self.firebase_db.get('/', 'campaigns', params={'orderBy': '\"chat_id\"', 'equalTo': chat_id, 'auth': FIREBASE_API_SECRET})
        index = list(results.keys())[0]
        return results[index]

    def set_turn_index(self, campaign_id, turn_index):
        return self.firebase_db.put('/campaigns', campaign_id, data={'turn_index': turn_index}, params={'auth': FIREBASE_API_SECRET})

    def set_turns(self, campaign_id, turns):
        return self.firebase_db.put('/campaigns', campaign_id, data={'turns': turns}, params={'auth': FIREBASE_API_SECRET})
