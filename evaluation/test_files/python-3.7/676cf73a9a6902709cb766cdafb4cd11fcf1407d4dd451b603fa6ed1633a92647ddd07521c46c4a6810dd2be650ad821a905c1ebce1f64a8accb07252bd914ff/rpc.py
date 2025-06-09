from marshmallow import Schema, fields, post_load, pre_load, EXCLUDE
from marshmallow_oneofschema import OneOfSchema
from starknet_py.net.client_models import StarknetBlock, L1toL2Message, L2toL1Message, BlockStateUpdate, StorageDiff, DeployedContract, Event, EntryPoint, EntryPointsByType, DeclaredContract, InvokeTransaction, DeclareTransaction, DeployTransaction, TransactionReceipt, SentTransactionResponse, DeclareTransactionResponse, DeployTransactionResponse, EstimatedFee, StateDiff
from starknet_py.net.schemas.common import Felt, BlockStatusField, StatusField, NonPrefixedHex

class FunctionCallSchema(Schema):
    contract_address = fields.Integer(data_key='contract_address', required=True)
    entry_point_selector = fields.Integer(data_key='entry_point_selector', required=True)
    calldata = fields.List(fields.Integer(), data_key='calldata', required=True)

class EventSchema(Schema):
    from_address = Felt(data_key='from_address', required=True)
    keys = fields.List(Felt(), data_key='keys', required=True)
    data = fields.List(Felt(), data_key='data', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> Event:
        return Event(**data)

class L1toL2MessageSchema(Schema):
    l1_address = Felt(data_key='from_address', required=True)
    l2_address = Felt(load_default=None)
    payload = fields.List(Felt(), data_key='payload', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> L1toL2Message:
        return L1toL2Message(**data)

class L2toL1MessageSchema(Schema):
    l2_address = Felt(load_default=None)
    l1_address = Felt(data_key='to_address', required=True)
    payload = fields.List(Felt(), data_key='payload', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> L2toL1Message:
        return L2toL1Message(**data)

class TransactionReceiptSchema(Schema):
    hash = Felt(data_key='transaction_hash', required=True)
    status = StatusField(data_key='status', required=True)
    block_number = fields.Integer(data_key='block_number', load_default=None)
    block_hash = Felt(data_key='block_hash', load_default=None)
    actual_fee = Felt(data_key='actual_fee', required=True)
    rejection_reason = fields.String(data_key='status_data', load_default=None)
    events = fields.List(fields.Nested(EventSchema()), data_key='events', load_default=[])
    l1_to_l2_consumed_message = fields.Nested(L1toL2MessageSchema(), data_key='l1_origin_message', load_default=None)
    l2_to_l1_messages = fields.List(fields.Nested(L2toL1MessageSchema()), data_key='messages_sent', load_default=[])

    @post_load
    def make_dataclass(self, data, **kwargs) -> TransactionReceipt:
        return TransactionReceipt(**data)

class EstimatedFeeSchema(Schema):
    overall_fee = Felt(data_key='overall_fee', required=True)
    gas_price = Felt(data_key='gas_price', required=True)
    gas_usage = Felt(data_key='gas_consumed', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return EstimatedFee(**data)

class TransactionSchema(Schema):
    hash = Felt(data_key='transaction_hash', required=True)
    signature = fields.List(Felt(), data_key='signature', load_default=[])
    max_fee = Felt(data_key='max_fee', load_default=0)
    version = Felt(data_key='version', required=True)

class InvokeTransactionSchema(TransactionSchema):
    contract_address = Felt(data_key='contract_address', required=True)
    entry_point_selector = Felt(data_key='entry_point_selector', required=True)
    calldata = fields.List(Felt(), data_key='calldata', required=True)
    nonce = Felt(data_key='nonce', load_default=None)

    @pre_load
    def preprocess(self, data, **kwargs):
        return data

    @post_load
    def make_transaction(self, data, **kwargs) -> InvokeTransaction:
        return InvokeTransaction(**data)

class DeclareTransactionSchema(TransactionSchema):
    class_hash = Felt(data_key='class_hash', required=True)
    sender_address = Felt(data_key='sender_address', required=True)
    nonce = Felt(data_key='nonce', load_default=None)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclareTransaction:
        return DeclareTransaction(**data)

class DeployTransactionSchema(TransactionSchema):
    contract_address = Felt(data_key='contract_address', required=True)
    constructor_calldata = fields.List(Felt(), data_key='constructor_calldata', required=True)
    class_hash = Felt(data_key='class_hash', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployTransaction:
        return DeployTransaction(**data)

class TypesOfTransactionsSchema(OneOfSchema):
    type_field = 'type'
    type_schemas = {'INVOKE': InvokeTransactionSchema, 'DECLARE': DeclareTransactionSchema, 'DEPLOY': DeployTransactionSchema, 'DEPLOY_ACCOUNT': None}

class StarknetBlockSchema(Schema):
    block_hash = Felt(data_key='block_hash', required=True)
    parent_block_hash = Felt(data_key='parent_hash', required=True)
    block_number = fields.Integer(data_key='block_number', required=True)
    status = BlockStatusField(data_key='status', required=True)
    root = NonPrefixedHex(data_key='new_root', required=True)
    transactions = fields.List(fields.Nested(TypesOfTransactionsSchema(unknown=EXCLUDE)), data_key='transactions', required=True)
    timestamp = fields.Integer(data_key='timestamp', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> StarknetBlock:
        return StarknetBlock(**data)

class StorageDiffSchema(Schema):
    address = Felt(data_key='address', required=True)
    key = Felt(data_key='key', required=True)
    value = Felt(data_key='value', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> StorageDiff:
        return StorageDiff(**data)

class ContractDiffSchema(Schema):
    address = Felt(data_key='address', required=True)
    contract_hash = Felt(data_key='contract_hash', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployedContract:
        return DeployedContract(**data)

class DeployedContractSchema(Schema):
    address = Felt(data_key='address', required=True)
    class_hash = NonPrefixedHex(data_key='class_hash', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return DeployedContract(**data)

class DeclaredContractClassHashSchema(Schema):
    class_hash = Felt(data_key='class_hash', required=True)

    @post_load
    def return_class_hash(self, data, **kwargs):
        return data['class_hash']

class StateDiffSchema(Schema):
    deployed_contracts = fields.List(fields.Nested(DeployedContractSchema()), data_key='deployed_contracts', required=True)
    declared_contracts = fields.List(fields.Nested(DeclaredContractClassHashSchema()), data_key='declared_contracts', required=True)
    storage_diffs = fields.List(fields.Nested(StorageDiffSchema()), data_key='storage_diffs', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> StateDiff:
        return StateDiff(**data)

class BlockStateUpdateSchema(Schema):
    block_hash = Felt(data_key='block_hash', required=True)
    new_root = Felt(data_key='new_root', required=True)
    old_root = Felt(data_key='old_root', required=True)
    state_diff = fields.Nested(StateDiffSchema(), data_key='state_diff', required=True)

    @pre_load
    def preprocess(self, data, **kwargs):
        del data['state_diff']['nonces']
        return data

    @post_load
    def make_dataclass(self, data, **kwargs) -> BlockStateUpdate:
        declared_contracts = data['state_diff'].declared_contracts
        deployed_contracts = data['state_diff'].deployed_contracts
        storage_diffs = data['state_diff'].storage_diffs
        del data['state_diff']
        return BlockStateUpdate(**data, declared_contracts=declared_contracts, deployed_contracts=deployed_contracts, storage_diffs=storage_diffs)

class EntryPointSchema(Schema):
    offset = Felt(data_key='offset', required=True)
    selector = Felt(data_key='selector', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> EntryPoint:
        return EntryPoint(**data)

class EntryPointsByTypeSchema(Schema):
    constructor = fields.List(fields.Nested(EntryPointSchema()), data_key='CONSTRUCTOR', required=True)
    external = fields.List(fields.Nested(EntryPointSchema()), data_key='EXTERNAL', required=True)
    l1_handler = fields.List(fields.Nested(EntryPointSchema()), data_key='L1_HANDLER', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> EntryPointsByType:
        return EntryPointsByType(**data)

class DeclaredContractSchema(Schema):
    program = fields.String(data_key='program', required=True)
    entry_points_by_type = fields.Nested(EntryPointsByTypeSchema(), data_key='entry_points_by_type', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclaredContract:
        return DeclaredContract(**data)

class SentTransactionSchema(Schema):
    transaction_hash = Felt(data_key='transaction_hash', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return SentTransactionResponse(**data)

class DeclareTransactionResponseSchema(SentTransactionSchema):
    class_hash = Felt(data_key='class_hash', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return DeclareTransactionResponse(**data)

class DeployTransactionResponseSchema(SentTransactionSchema):
    contract_address = Felt(data_key='contract_address', required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return DeployTransactionResponse(**data)

class PendingTransactionsSchema(Schema):
    pending_transactions = fields.List(fields.Nested(TypesOfTransactionsSchema(unknown=EXCLUDE)), required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return data['pending_transactions']