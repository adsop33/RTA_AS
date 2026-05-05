from kafka import KafkaConsumer
from collections import defaultdict
import json, time
 
WINDOW_SEC = 60  
MAX_TX = 3       
 
# słownik: user_id
user_timestamps = defaultdict(list)
 
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    group_id='velocity-detector',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
 
print("Anomalie prędkości")
 
for msg in consumer:
    tx = msg.value
    uid = tx['user_id']
    now = time.time()
 
    # wyrzuć timestamps starsze niż okno
    user_timestamps[uid] = [t for t in user_timestamps[uid] if now - t < WINDOW_SEC]
    user_timestamps[uid].append(now)
 
    count = len(user_timestamps[uid])
 
    if count > MAX_TX:
        print(f"!  ALERT   !| {uid} | {count} tx 60s | {tx['tx_id']} | {tx['amount']:.2f} zl | {tx['store']}")
    else:
        print(f" CLEAN | {uid} | {tx['tx_id']} | {tx['amount']:.2f} zl")