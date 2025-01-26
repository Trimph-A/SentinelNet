from web3 import Web3
import json
from datetime import datetime

class BlockchainNotifier:
    def __init__(self):
        # Connect to the Ethereum testnet (e.g., Rinkeby or Goerli)
        self.infura_url = "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
        if not self.w3.isConnected():
            raise ConnectionError("Failed to connect to the blockchain")
        
        # Load your wallet private key (to sign transactions)
        self.private_key = "YOUR_PRIVATE_KEY"
        self.account = self.w3.eth.account.privateKeyToAccount(self.private_key)
        self.contract_address = "YOUR_CONTRACT_ADDRESS"  # The address where you want to send notifications

        # ABI for the contract (simplified version, you should use your own ABI)
        self.abi = json.loads('[{"constant": false, "inputs": [{"name": "eventType", "type": "string"}, {"name": "description", "type": "string"}, {"name": "timestamp", "type": "uint256"}, {"name": "evidence", "type": "string"}, {"name": "security", "type": "string"}], "name": "sendNotification", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}]')

    def send_notification(self, notification):
        """Send the notification to the blockchain."""
        try:
            # Contract instance
            contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

            # Prepare transaction
            tx = contract.functions.sendNotification(
                notification['event_type'],
                notification['description'],
                int(notification['timestamp'].timestamp()),  # Convert datetime to timestamp
                notification['evidence'],
                notification['security']
            ).buildTransaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.toWei('20', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(self.account.address),
            })

            # Sign the transaction
            signed_tx = self.w3.eth.account.signTransaction(tx, self.private_key)

            # Send the transaction
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f"Transaction hash: {tx_hash.hex()}")

            # Wait for the transaction receipt
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"Transaction receipt: {receipt}")

        except Exception as e:
            print(f"Failed to send notification to blockchain: {e}")

# Create a global instance of the notifier to use in your routes
blockchain_notifier = BlockchainNotifier()
