from stake_api import Stake

stake = Stake('4e0f11ff7a0a4985de03c57ce063b1f5d0ce43e2b2026b09077e2c268a1696b81f591d9c2fe4d8b699deca28cdb4b9b8')

response = stake.user_balances()

print(response)
    
    