from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import decode_transfer
from solana.system_program import TransferParams
from solana.transaction import Transaction, TransactionInstruction
import base64
solana_client = Client("https://devnet.solana.com")
tx_sig = ""
tx_result = solana_client.get_confirmed_transaction(tx_sig=tx_sig, encoding="base64")

raw_tx_str = tx_result['result']['transaction'][0]

raw_tx_base64_bytes = raw_tx_str.encode('ascii')
raw_tx_bytes = base64.b64decode(raw_tx_base64_bytes)

tx: Transaction = Transaction.deserialize(raw_tx_bytes)
tx_instruction: TransactionInstruction = tx.instructions.pop()
transfer_params: TransferParams = decode_transfer(tx_instruction)

print(transfer_params.to_pubkey) # to
print(transfer_params.from_pubkey) # from
print(tranfer_params.lamports) # amount
