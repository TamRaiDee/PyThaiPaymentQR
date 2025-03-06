import pytest
from PyCRC.CRCCCITT import CRCCCITT


def constant_and_checksum_test(ksp_str: str):
    # Expected 000201 in ksp_str
    assert "000201" in ksp_str, "Prefix representation is incorrect."

    # Expected 010211 in ksp_str
    assert "010211" in ksp_str, "Payload Format Indicator representation is incorrect."

    # Expected 0016A000000677010112 in ksp_str
    assert (
        "0016A000000677010112" in ksp_str
    ), "Merchant Account Information representation is incorrect."

    # Expected 0115010753600031508 in ksp_str
    assert "0115010753600031508" in ksp_str, "Merchant Category Code representation is incorrect."

    # Expected 5303764 in ksp_str
    assert "5303764" in ksp_str, "Transaction Currency representation is incorrect."

    # Expected 5802TH in ksp_str
    assert "5802TH" in ksp_str, "Country Code representation is incorrect."

    crc_obj = CRCCCITT("FFFF")
    crc = crc_obj.calculate(ksp_str[:-4])
    crc_hex = format(crc, "X").upper()

    if len(crc_hex) != 4:
        crc_hex = crc_hex.zfill(4)

    # Expected CRC16 checksum in ksp_str
    assert crc_hex == ksp_str[-4:], "CRC16 checksum representation is incorrect."


def test_crc16():
    crc_obj = CRCCCITT("FFFF")
    crc = crc_obj.calculate(
        "00020101021129370016A000000677010111011300660000000005802TH53037646304"
    )

    # Expected CRC16 checksum 0x8956
    assert crc == 0x8956, "CRC16 checksum should be 0x8956."


def test_KShopQR():
    from ThaiPaymentQR import KShopQR

    ksp = KShopQR("014000000820910", "TESTPYTHON")
    ksp.setAmount(14.53)
    ksp_str = str(ksp)

    assert ksp_str, "KShopQR string representation should not be empty."

    constant_and_checksum_test(ksp_str)

    # Expected field 30
    assert "30" in ksp.fields, "BillPayment field should be in KShopQR fields."

    # Expected field 30 data
    assert str(ksp.fields["30"]) in ksp_str, "BillPayment field data should be in KShopQR string."

    # Expected field 31
    assert "31" in ksp.fields, "PaymentInnovation field should be in KShopQR fields."

    # Expected field 31 data
    assert (
        str(ksp.fields["31"]) in ksp_str
    ), "PaymentInnovation field data should be in KShopQR string."

    # Expected 0215014000000820910 in ksp_str
    assert "0215014000000820910" in ksp_str, "ShopID representation is incorrect."

    # Expected 0313KPSTESTPYTHON in ksp_str
    assert "0313KPSTESTPYTHON" in ksp_str, "ShopName representation is incorrect."

    # Expected 540514.53 in ksp_str
    assert "540514.53" in ksp_str, "Amount representation is incorrect."

    # Expected data (without 8 last characters) in ksp_str
    assert len(ksp_str[:-8]) == len(
        "00020101021130750016A000000677010112011501075360003150802150140000008209100313KPSTESTPYTHON31630016A000000677010113010300402150140000008209100413KPSTESTPYTHON5303764540514.535802TH"
    ), "Data length is incorrect."


def test_KShopQR_2():
    from ThaiPaymentQR import KShopQR

    ksp = KShopQR("014000000820910", "312121")
    ksp.setAmount(1212.00)
    ksp_str = str(ksp)

    assert ksp_str, "KShopQR string representation should not be empty."

    constant_and_checksum_test(ksp_str)

    # Expected 0215014000000820910 in ksp_str
    assert "0215014000000820910" in ksp_str, "ShopID representation is incorrect."

    # Expected 0309KPS312121 in ksp_str
    assert "0309KPS312121" in ksp_str, "ShopName representation is incorrect."

    # Expected 54071212.00 in ksp_str
    assert "54071212.00" in ksp_str, "Amount representation is incorrect."

    # Expected data (without 8 last characters) in ksp_str
    assert len(ksp_str[:-8]) == len(
        "00020101021130710016A000000677010112011501075360003150802150140000008209100309KPS31212131590016A000000677010113010300402150140000008209100409KPS312121530376454071212.005802TH"
    ), "Data length is incorrect."


def test_KShopQR_CRC():
    from ThaiPaymentQR import KShopQR

    ksp = KShopQR("014000000820910", "Supatipanno")
    ksp.setAmount(40010.00)
    ksp_str = str(ksp)
    assert ksp_str[-4] == "0", "CRC16 checksum for this test should be zero-leading."
    constant_and_checksum_test(ksp_str)


if __name__ == "__main__":
    pytest.main()
