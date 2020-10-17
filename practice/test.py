# 存放系统的用户账号，密码，余额
userlist=[]


# 查询余额
def queryMoney(account):
    money=0;
    for obj in userlist:
        if account==obj["account"]:
            money=obj["money"]
            break
    return money

# 转账
def giveMoney(account):
    print("请输入您要转账的账户：")
    account2=input()
    print("请输入您要转账的金额：")
    money2=input()
    currentMoney=0;
    for obj in userlist:
        if account==obj["account"]:
            if int(money2)<=obj["money"]:
                obj["money"]=obj["money"]-int(money2)
                currentMoney=obj["money"]
                for test in userlist:
                    if account2==test["account"]:
                        test["money"]=test["money"]+int(money2)
                        break
                else:
                    print("【您的转账账户不存在，请检查账号后重新转账操作】")
                    xtnb(account)
            else:
                print("【您的余额已不足，无法转账！】")
                xtnb(account)
    return currentMoney

# 取钱
def getMoney(account):
    print("请输入您要取的金额：")
    money = input()
    currentMoney = 0;
    for obj in userlist:
        if account == obj["account"]:
            if obj["money"]>int(money):
                obj["money"] = obj["money"] - int(money)
                currentMoney = obj["money"]
                break
            else:
                print("【您的余额已不足，请充值！】")
                xtnb(account)
    return currentMoney

# 存钱
def saveMoney(account):
    print("请输入您的存钱金额：")
    money=input()
    currentMoney=0;
    for obj in userlist:
        if account==obj["account"]:
            obj["money"]=obj["money"]+int(money)
            currentMoney=obj["money"]
            break
    return currentMoney

# 系统内部
def xtnb(account):
    print("=====================")
    print("1，查询余额")
    print("2，转账")
    print("3，取钱")
    print("4，存钱")
    print("5，退出")
    print("=====================")
    print("请输入您要操作的指令：")
    num=input()
    if num=="1":
       money = queryMoney(account)
       print("【您的余额：",money,"元】")
       xtnb(account)
    elif num=="2":
       currentMoney = giveMoney(account)
       print("【转账成功，当前您的余额为", currentMoney, "元】")
       xtnb(account)
    elif num=="3":
        currentMoney=getMoney(account)
        print("【取钱成功，当前您的余额为", currentMoney, "元】")
        xtnb(account)
    elif num=="4":
       currentMoney = saveMoney(account)
       print("【存钱成功，当前您的余额为",currentMoney,"元】")
       xtnb(account)
    elif num=="5":
        print("【大爷，您有机会常来玩呀！】")
        begin()


# 登录系统
def login():
    print("请输入账号：")
    account=input()
    print("请输入密码：")
    pwd=input()
    for obj in userlist:
        if account==obj["account"] and pwd==obj["pwd"]:
            print("【登录成功，进入系统】")
            xtnb(account)
    else:
        print("【账号不存在/密码错误，请重新登录】")
        begin()




# 注册系统
def register():
    print("请输入您要注册的账号：")
    account=input()
    print("请设置您的密码：")
    pwd=input()
    obj={"account":account,"pwd":pwd,"money":0}
    userlist.append(obj)
    print("【恭喜您！账号注册成功】")
    begin()
    return

# 注销账户
def zxzh():
    print("请输入您要注销的账户：")
    account=input()
    for obj in userlist:
        if account==obj["account"]:
            userlist.remove(obj)
            print("【注销账户成功！】")
            begin();
    else:
        print("【该账户不存在，注销失败】")
        begin();


def begin():
    print("=======银行柜台服务=========")
    print("1，登录系统")
    print("2，注册系统")
    print("3，注销账户")
    print("==========================")
    print("请输入操作指令：")
    num = input()
    if num == "1":
        login();
    elif num == "2":
        register();
    elif num == "3":
        zxzh();
    return

begin();


