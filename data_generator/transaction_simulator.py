import random
import uuid
import csv
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
NUM_TRANSACTIONS = 100  # Number of transactions to generate per run
FRAUD_PROBABILITY = 0.05  # 5% of transactions flagged as fraud
OUTPUT_FILE = "data_generator/simulated_transactions.csv"  # Output CSV file name

CARD_PREFIXES = [
    '411111', '550000', '340000', '300000',
    '201400', '308800', '360000', '601100',
    '622126', '353011'
]
MERCHANT_TYPES = ['Grocery', 'Electronics', 'Restaurant', 'Travel', 'Online Retail']
MERCHANT_IDS = [str(uuid.uuid4())[:8] for _ in range(50)]  # Generate 50 random merchant IDs

def generate_card_number():
    """Generate a pseudo card number by combining a random prefix and a random 10-digit suffix."""
    prefix = random.choice(CARD_PREFIXES)
    suffix = "".join(str(random.randint(0, 9)) for _ in range(10))
    return prefix + suffix

def generate_amount():
    """Generate a random transaction amount between $1 and $2000."""
    return round(random.uniform(1.0, 2000.0), 2)

def generate_fraud_flag():
    """Return 1 if the transaction is fraudulent, 0 otherwise."""
    return 1 if random.random() < FRAUD_PROBABILITY else 0

def generate_timestamp():
    """Generate a random timestamp within the last 30 days."""
    now = datetime.now()
    start = now - timedelta(days=30)
    random_seconds = random.randint(0, int((now - start).total_seconds()))
    random_time = start + timedelta(seconds=random_seconds)
    return random_time.strftime('%Y-%m-%d %H:%M:%S')

def generate_transactions(num_records=NUM_TRANSACTIONS):
    transactions = []
    for _ in range(num_records):
        transaction = {
            'transaction_id': str(uuid.uuid4()),
            'card_number': generate_card_number(),
            'amount': generate_amount(),
            'merchant_id': random.choice(MERCHANT_IDS),
            'merchant_type': random.choice(MERCHANT_TYPES),
            'is_fraud': generate_fraud_flag(),
            'timestamp': generate_timestamp()
        }
        transactions.append(transaction)
    return transactions

def write_to_csv(transactions, output_file=OUTPUT_FILE):
    """Write the transactions list to a CSV file."""
    if not transactions:
        print("No transactions to write.")
        return

    headers = transactions[0].keys()
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(transactions)

    print(f"{len(transactions)} transactions written to {output_file}")

if __name__ == "__main__":
    txs = generate_transactions()
    write_to_csv(txs)
