import json
import random
import uuid
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer

# -------------------------------
# CONFIGURATION
# -------------------------------
NUM_TRANSACTIONS = 1000            # Total transactions to send
FRAUD_PROBABILITY = 0.05           # 5% chance of fraud
KAFKA_TOPIC = 'fraud_transactions'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

# -------------------------------
# SET UP KAFKA PRODUCER
# -------------------------------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# -------------------------------
# SAMPLE DATA SETUP
# -------------------------------
CARD_PREFIXES = [
    '411111', '550000', '340000', '300000',
    '201400', '308800', '360000', '601100',
    '622126', '353011'
]
MERCHANT_TYPES = ['Grocery', 'Electronics', 'Restaurant', 'Travel', 'Online Retail']
MERCHANT_IDS = [str(uuid.uuid4())[:8] for _ in range(50)]

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def generate_card_number():
    """Generate a card number by combining a random prefix and a 10-digit suffix."""
    prefix = random.choice(CARD_PREFIXES)
    suffix = "".join(str(random.randint(0, 9)) for _ in range(10))
    return prefix + suffix

def generate_amount():
    """Generate a random amount between $1 and $2000."""
    return round(random.uniform(1.0, 2000.0), 2)

def generate_fraud_flag():
    """Return 1 for fraud based on FRAUD_PROBABILITY, else 0."""
    return 1 if random.random() < FRAUD_PROBABILITY else 0

def generate_timestamp():
    """Generate a timestamp within the last 30 days."""
    now = datetime.now()
    start = now - timedelta(days=30)
    random_seconds = random.randint(0, int((now - start).total_seconds()))
    random_time = start + timedelta(seconds=random_seconds)
    return random_time.strftime('%Y-%m-%d %H:%M:%S')

def generate_transaction():
    """Generate a single transaction record."""
    return {
        'transaction_id': str(uuid.uuid4()),
        'card_number': generate_card_number(),
        'amount': generate_amount(),
        'merchant_id': random.choice(MERCHANT_IDS),
        'merchant_type': random.choice(MERCHANT_TYPES),
        'is_fraud': generate_fraud_flag(),
        'timestamp': generate_timestamp()
    }

# -------------------------------
# MAIN LOOP: SEND TRANSACTIONS
# -------------------------------
if __name__ == "__main__":
    print("Starting Kafka Producer for Transactions...")
    for i in range(NUM_TRANSACTIONS):
        tx = generate_transaction()
        producer.send(KAFKA_TOPIC, tx)
        print(f"Sent transaction: {tx['transaction_id']}")
        time.sleep(0.1)  # Simulate a delay between transactions
    producer.flush()
    print("Finished sending transactions.")
