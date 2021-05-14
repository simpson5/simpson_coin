import pyupbit

access = "wDNJP9jHj8xWx3Oj7cL0TRJVqrtP8zdoKlaBi02a"          # 본인 값으로 변경
secret = "gDNjgJx4oB2cH099lrnNitJqSXxIKgmB8tEUa6bJ"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

# print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
