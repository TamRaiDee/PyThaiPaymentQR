from .PromptPayField import PromptPayField
from .PromptPayQR import PromptPayQR


class KShopQR(PromptPayQR):
    def __init__(self, shopID, Ref):
        self.fields = {}
        super().__init__()
        bill_info_data = [
            PromptPayField("00", "AppID", "A000000677010112"),
            PromptPayField("01", "BillerID", "010753600031508"),
            PromptPayField("02", "ShopID", shopID),
            PromptPayField("03", "Ref", f"KPS{Ref}"),
        ]
        payment_innovation_data = [
            PromptPayField("00", "AppID", "A000000677010113"),
            PromptPayField("01", "AcquirerID", "004"),
            PromptPayField("02", "ShopID", shopID),
            PromptPayField("04", "Ref", f"KPS{Ref}"),
        ]
        self.additionalField = []
        bill_info = PromptPayField("30", "BillPayment", bill_info_data)
        payment_innovation = PromptPayField("31", "PaymentInnovation", payment_innovation_data)
        self.fields["30"] = bill_info
        self.fields["31"] = payment_innovation
