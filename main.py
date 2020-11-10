from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import decode_transfer as sol_decode_transfer
from spl.token.instructions import decode_transfer as spl_decode_transfer
from solana.system_program import TransferParams as SOLTransferParams
from spl.token.instructions import TransferParams as SPLTransferParams
from solana.transaction import Transaction, TransactionInstruction
from solana._layouts.system_instructions import SYSTEM_INSTRUCTIONS_LAYOUT, InstructionType as SOLInstructionType
from spl.token._layouts import INSTRUCTIONS_LAYOUT, InstructionType as SPLInstructionType
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

	des_tx: Transaction = Transaction.deserialize(raw_tx_bytes)
	tx_instruction: TransactionInstruction = des_tx.instructions.pop()
	# program id will be a bunch of ones if it's a transaction involving SOL
	if tx_instruction.program_id.__str__() == "11111111111111111111111111111111":
		if SYSTEM_INSTRUCTIONS_LAYOUT.parse(tx_instruction.data).instruction_type == SOLInstructionType.Transfer:
			transfer_params: SOLTransferParams = sol_decode_transfer(tx_instruction)
			print(tx["slot"]) # blockheight
			print(f'from:{transfer_params.from_pubkey}') # from
			print(f'to:{transfer_params.to_pubkey}') # to
			print(f'amount:{transfer_params.lamports * .000000001}') # amount
	# program id will be Token... if it's a transaction involving tokens
	if tx_instruction.program_id.__str__() == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
		if INSTRUCTIONS_LAYOUT.parse(tx_instruction.data).instruction_type == SPLInstructionType.Transfer:
			transfer_params: SPLTransferParams = spl_decode_transfer(tx_instruction)
			print(tx["slot"]) # blockheight
			print(f'from:{transfer_params.source}') # from
			print(f'to:{transfer_params.dest}') # to
			print(f'token:{None}') # TODO token
			print(f'amount:{transfer_params.amount *.000001}') # amount
