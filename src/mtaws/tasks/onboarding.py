def onboard_account(data, msg):
    print("TEST ONBOARDING")
    print(data)
    print("DELETE MESSAGE")
    res = msg.delete()
    print("RES: ")
    print(res)
