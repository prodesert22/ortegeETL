from dataclasses import dataclass, asdict, fields
from typing import Any, List, Optional, TypedDict

class ChangesType(TypedDict):
    type: str
    address: Optional[str]
    state_key_hash: str
    module: Optional[str]
    resource: Optional[str]
    key: Optional[str]
    handle: Optional[str]
    value: Optional[str]
    data: Optional[str]

class SignatureType(TypedDict):
    type: str
    public_key: str
    signature: Optional[str]
    signatures: Optional[List[str]]
    threshold: Optional[int]
    bitmap: Optional[str]

class GenericTypeParams(TypedDict):
    constraints: List[str]

class AbiType(TypedDict):
    name: str
    visibility: str
    is_entry: bool
    is_view: bool
    generic_type_params: dict
    params: List[str]
    return_type: List[str]

class CodeType(TypedDict):
    bytecode: str
    abi: AbiType

class ScriptType(TypedDict):
    code: CodeType
    type_arguments: List[str]
    arguments: List[str]

class WriteSetType(TypedDict):
    type: str
    execute_as: str
    script: ScriptType

class TransactionPayload(TypedDict):
    type: str
    function: str
    type_arguments: List[str]
    arguments: List[str]
    write_set: WriteSetType

class TransactionEventsGuid(TypedDict):
    creation_number: int
    account_address: str

class TransactionEvents(TypedDict):
    guid: TransactionEventsGuid
    sequence_number: int
    type: str
    data: str

@dataclass
class AptosTransaction:
    hash: str
    block_number: int
    state_change_hash: str
    event_root_hash: str
    version: int
    gas_used: int
    success: bool
    vm_status: str
    accumulator_root_hash: str
    changes: List[ChangesType]
    tx_type: str
    
    #optionals parameters
    sender: Optional[str]
    state_checkpoint_hash: Optional[str]
    id: Optional[str]
    epoch: Optional[str]
    round: Optional[str]
    previous_block_votes_bitvec: Optional[List[int]]
    proposer: Optional[str]
    failed_proposer_indices: Optional[List[int]]
    timestamp: Optional[int]
    max_gas_amount: Optional[int]
    gas_unit_price: Optional[int]
    expiration_timestamp_secs: Optional[int]
    payload: Optional[TransactionPayload]
    events: Optional[List[TransactionEvents]]
    signature: Optional[SignatureType]

    @staticmethod
    def from_dict(json_dict: dict):
        valid_fields = {field.name for field in fields(AptosTransaction)}
        filtered_data = {key: value for key, value in json_dict.items() if key in valid_fields} # Remove the extra keys in the dict

        filtered_data["block_number"] = int(json_dict['block_number'])
        filtered_data["version"] = int(json_dict['version'])
        filtered_data["gas_used"] = int(json_dict['gas_used'])
        filtered_data["tx_type"] = json_dict['type']

        filtered_data["max_gas_amount"] = int(json_dict.get('max_gas_amount')) if json_dict.get('max_gas_amount') else None
        filtered_data["gas_unit_price"] = int(json_dict.get('gas_unit_price')) if json_dict.get('gas_unit_price') else None
        filtered_data["expiration_timestamp_secs"] = int(json_dict.get('expiration_timestamp_secs')) if json_dict.get('expiration_timestamp_secs') else None
        filtered_data["timestamp"] = int(json_dict.get('timestamp')) if json_dict.get('timestamp') else None

        filtered_data["sender"] = json_dict.get('sender')
        filtered_data["state_checkpoint_hash"] = json_dict.get('state_checkpoint_hash')
        filtered_data["id"] = json_dict.get('id')
        filtered_data["epoch"] = json_dict.get('epoch')
        filtered_data["round"] = json_dict.get('round')
        filtered_data["previous_block_votes_bitvec"] = json_dict.get('previous_block_votes_bitvec')
        filtered_data["proposer"] = json_dict.get('proposer')
        filtered_data["failed_proposer_indices"] = json_dict.get('failed_proposer_indices')
        filtered_data["signature"] = json_dict.get('signature')
        filtered_data["changes"] = json_dict.get('changes', [])

        events: TransactionEvents = json_dict.get('events')
        if events:
            def _convert_event(event: dict[str, Any]):
                event['data'] = str(event['data'])
                return event

            events = list(map(_convert_event, events))
        filtered_data["events"] = events
        
        payload: TransactionPayload = json_dict.get('payload')
        if payload:
            payload_write_set = payload.get('write_set')
            if payload_write_set is not None and payload_write_set.get('script', {}).get('code', {}).get('abi', {}).get('return'):
               payload_write_set['script']['code']['abi']['return_type'] = payload_write_set.get('script', {}).get('code', {}).get('abi', {}).get('return')

        filtered_data["payload"] = payload

        return AptosTransaction(**filtered_data)

    def to_dict(self):
        transaction_dict = asdict(self)
        transaction_dict['type'] = "transaction"

        return transaction_dict
