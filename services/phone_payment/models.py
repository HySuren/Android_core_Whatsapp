from pydantic import BaseModel


class PaymentsResponse(BaseModel):

    class Sum(BaseModel):
        amount: int
        currency: str = '643'

    class Fields(BaseModel):
        account: str

    class Transaction(BaseModel):

        class Code(BaseModel): code: str = None

        id: str = None
        state: Code

    fields: Fields
    terms: int
    sum: Sum
    transaction: Transaction

    def prepare_to_insert(self):
        return int(self.transaction.id), self.transaction.state.code, int(self.terms), self.fields.account, int(self.sum.amount),

