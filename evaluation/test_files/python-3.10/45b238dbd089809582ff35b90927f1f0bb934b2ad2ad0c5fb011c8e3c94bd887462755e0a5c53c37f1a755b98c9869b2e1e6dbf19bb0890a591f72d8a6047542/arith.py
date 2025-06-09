from __future__ import annotations
from xdsl.ir import *
from xdsl.irdl import *
from xdsl.util import *
from xdsl.dialects.builtin import IntegerType, Float32Type, IntegerAttr

@dataclass
class Arith:
    ctx: MLContext

    def __post_init__(self):
        self.ctx.register_op(Constant)
        self.ctx.register_op(Addi)
        self.ctx.register_op(Muli)
        self.ctx.register_op(Subi)
        self.ctx.register_op(FloorDiviSI)
        self.ctx.register_op(RemSI)
        self.ctx.register_op(Addf)
        self.ctx.register_op(Mulf)
        self.ctx.register_op(Cmpi)
        self.ctx.register_op(AndI)
        self.ctx.register_op(OrI)
        self.ctx.register_op(XOrI)

@irdl_op_definition
class Constant(Operation):
    name: str = 'arith.constant'
    output = ResultDef(AnyAttr())
    value = AttributeDef(AnyAttr())

    @staticmethod
    def from_attr(attr: Attribute, typ: Attribute) -> Constant:
        return Constant.create(result_types=[typ], attributes={'value': attr})

    @staticmethod
    def from_int_constant(val: Union[int, Attribute], typ: Union[int, Attribute]) -> Constant:
        if isinstance(typ, int):
            typ = IntegerType.from_width(typ)
        return Constant.create(result_types=[typ], attributes={'value': IntegerAttr.from_params(val, typ)})

@irdl_op_definition
class Addi(Operation):
    name: str = 'arith.addi'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> Addi:
        return Addi.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(32)])

@irdl_op_definition
class Muli(Operation):
    name: str = 'arith.muli'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> Muli:
        return Muli.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(32)])

@irdl_op_definition
class Subi(Operation):
    name: str = 'arith.subi'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> Subi:
        return Subi.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(32)])

@irdl_op_definition
class FloorDiviSI(Operation):
    name: str = 'arith.floordivsi'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> FloorDiviSI:
        return FloorDiviSI.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(32)])

@irdl_op_definition
class RemSI(Operation):
    name: str = 'arith.remsi'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> RemSI:
        return RemSI.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(32)])

@irdl_op_definition
class AndI(Operation):
    name: str = 'arith.andi'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> AndI:
        return AndI.build(operands=[operand1, operand2], result_types=[SSAValue.get(operand1).typ])

@irdl_op_definition
class OrI(Operation):
    name: str = 'arith.ori'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> OrI:
        return OrI.build(operands=[operand1, operand2], result_types=[SSAValue.get(operand1).typ])

@irdl_op_definition
class XOrI(Operation):
    name: str = 'arith.xori'
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> XOrI:
        return XOrI.build(operands=[operand1, operand2], result_types=[SSAValue.get(operand1).typ])

@irdl_op_definition
class Cmpi(Operation):
    name: str = 'arith.cmpi'
    predicate = AttributeDef(IntegerAttr)
    input1 = OperandDef(IntegerType)
    input2 = OperandDef(IntegerType)
    output = ResultDef(IntegerType.from_width(1))

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue], arg: int) -> Cmpi:
        return Cmpi.build(operands=[operand1, operand2], result_types=[IntegerType.from_width(1)], attributes={'predicate': IntegerAttr.from_int_and_width(arg, 64)})

@irdl_op_definition
class Addf(Operation):
    name: str = 'arith.addf'
    input1 = OperandDef(Float32Type)
    input2 = OperandDef(Float32Type)
    output = ResultDef(Float32Type)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> Addf:
        return Addf.build(operands=[operand1, operand2], result_types=[Float32Type()])

@irdl_op_definition
class Mulf(Operation):
    name: str = 'arith.mulf'
    input1 = OperandDef(Float32Type)
    input2 = OperandDef(Float32Type)
    output = ResultDef(Float32Type)

    def verify_(self) -> None:
        if self.input1.typ != self.input2.typ or self.input2.typ != self.output.typ:
            raise VerifyException('expect all input and output types to be equal')

    @staticmethod
    def get(operand1: Union[Operation, SSAValue], operand2: Union[Operation, SSAValue]) -> Mulf:
        return Mulf.build(operands=[operand1, operand2], result_types=[Float32Type()])