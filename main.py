from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import decode_transfer
from solana.system_program import TransferParams
from solana.transaction import Transaction, TransactionInstruction
import base64
# solana_client = Client("https://api.mainnet-beta.solana.com")
solana_client = Client("https://devnet.solana.com")
address = ""
transactions = solana_client.get_confirmed_signature_for_address2(address)["result"]
for tx in transactions:
	tx_result = solana_client.get_confirmed_transaction(tx_sig=tx["signature"], encoding="base64")

	raw_tx_str = tx_result['result']['transaction'][0]

	raw_tx_base64_bytes = raw_tx_str.encode('ascii')
	raw_tx_bytes = base64.b64decode(raw_tx_base64_bytes)

	tx: Transaction = Transaction.deserialize(raw_tx_bytes)
	tx_instruction: TransactionInstruction = tx.instructions.pop()
	print(tx_instruction)
	# System Program Create accounts and transfer lamports between them == bunch of ones (signifies just a normal transaction between accounts)
	if tx_instruction.program_id.__str__() == "11111111111111111111111111111111":
		transfer_params: TransferParams = decode_transfer(tx_instruction)
		print(transfer_params.to_pubkey) # to
		print(transfer_params.from_pubkey) # from
		print(transfer_params.lamports * .000000001) # amount
	
