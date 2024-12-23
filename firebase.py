import firebase_admin
from firebase_admin import credentials, firestore
import warnings
warnings.filterwarnings("ignore", category=UserWarning)



def getFirstJogakInfo():

    if not firebase_admin._apps:
        cred = credentials.Certificate('etc/secrets/orengeapp-43854-firebase-adminsdk-zq2mz-1a989fa573.json')
        app = firebase_admin.initialize_app(cred)

    user_info = {}
    db = firestore.client()

    for collection in db.collections():
        try:
            dict = collection.document('orenge').get().to_dict().get('orenge')[0]

            first_jogak = dict.get('조각', '')[1].get('이름', '')
            # print(first_jogak)

            first_jogak_list = [bite.get('이름', '') for bite in dict.get('조각', '')[1].get('입', '')]
            # print(first_jogak_list)

            user_info[first_jogak] = first_jogak_list
        except:
            continue
    
    return user_info

# print(getFirstJogakInfo())

startups = getFirstJogakInfo()
