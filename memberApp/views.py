from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import pymysql
from memberApp.form import MemberData
from myapp.dbConn import *
# Create your views here.

# 0,1 是管理員身分，唯有管理員才有權力修改或刪除使用者資料
# 2 ~ 9 為一般使用者
privilege_updated=[1,1,0,0,0,0,0,0,0,0]

# 初始化程式
# 建立資料庫連線
def main():
    global myDB
    db = pymysql.connect(host="127.0.0.1", user="username", passwd="password", database="your_database_name")
    myDB = dbConn(db)

main()

# 系統首頁
def orderSystem(request):
    if request.session.get("loginName") != None:
        return render(request,"orderSystem.html", {"loginName": request.session['loginName']})
    else:
        return render(request, "orderSystem.html",{"login": 0})

def memberAppHome(request):
    if request.session.get("loginName") != None:
        # 有登入，網頁轉到會員首頁
        return render(request, "memberApp\member.html",{"loginName": request.session['loginName']})
    else:
        # login = 0時，代表沒有登入，網頁轉到登入的介面
        return render(request, "memberApp\member.html",{"login": 0})
    # return HttpResponse("my memberApp Home")
    
# 預設為空
def memberCreate(request, name="", account="", passwd="", level=""):
    if request.session.get("loginName") != None:
        if privilege_updated[int(request.session['loginLevel'])] == 1:
            data={}
            data["name"] = name
            data["account"] = account
            data["passwd"] = passwd
            data["level"] = level
            return render(request,"memberApp\memberCreate.html", {"data": data, 'uName':request.session['loginName']})
        else:
            message ="目前身分： 一般使用者，您無權限新增使用者。"
            return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
    else:
        message = "尚未登入，無法新增會員"
        return render(request,"orderMessage.html", {"message": message, "login": 0})

# 新增會員_二次確認
def memberCreateDbCheck(request):
    # 轉成字典型態
    data = {}
    data['name'] = request.POST["name"]
    data['account'] = request.POST["account"]
    data['passwd'] = request.POST["passwd"]
    data['level'] = request.POST["level"]
    return render(request, "memberApp\memberDbCheck.html", {"data": data})

# 新增會員
def memberCreateConfirm(request):
    main()
    name = request.POST["name"]
    account = request.POST["account"]
    passwd = request.POST["passwd"]
    level = request.POST["level"]
    sql = "INSERT INTO new_member (name,account,password,level) VALUES ('{}','{}','{}','{}')".format(name,account,passwd,level)
    myDB.sql_execute(sql)
    myDB.connEnd()
    message = "成功寫入資料庫"
    return render(request,"memberApp\memberDbCheck.html",{'message':message, 'uName':request.session['loginName']})

# 會員資料更新
def memberUpdate(request, id=-1):
    main()
    if request.session['loginName'] != "" or request.session['loginName'] == None:
        if privilege_updated[int(request.session['loginLevel'])] == 1:
    # 修正資料庫會員資料，使用id欄位
            if request.method=='POST':
                name=request.POST['name']
                account=request.POST['account']
                passwd=request.POST['passwd']
                level=request.POST['level']
                sql = "UPDATE new_member SET name = '{}', account = '{}', password = '{}', level = '{}' WHERE id = {}".format(name, account, passwd, level, id)
                myDB.sql_execute(sql)
                myDB.connEnd()
                return redirect("/memberListAll/")
                # return HttpResponse("測試")
            else:
                if id != -1:
                    sql = "SELECT * FROM new_member WHERE id = {}".format(id)
                    data = myDB.sql_selectFetchOne(sql)
                    myDB.connEnd()
                    return render(request, "memberApp\memberUpdate.html", {"data": data, 'uName':request.session['loginName']})
                else:
                    message = "無id資料"
                    return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})     
        else: 
            message = "您無權限修改資料"
            return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
    else:
        message = "無id"
        return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
        
# id預設-1、0或空字串的話, 代表允許不帶值, 以免發生錯誤
def memberDelete(request, id=-1):
    main()
    del_sql = "DELETE FROM new_member WHERE id = {}".format(id)
    myDB.sql_execute(del_sql)
    myDB.connEnd()
    return redirect("/memberListAll/")

# id預設-1、0或空字串的話, 代表允許不帶值, 以免發生錯誤
def memberListOne(request, id=-1):
    main()
    if id == -1:
        return HttpResponse("無id資料 <a href='\memberKeyQuery\'>回查詢頁面</a> &nbsp&nbsp&nbsp<a href='\member\'>回首頁</a>")
    else:
        sql = "SELECT * FROM new_member WHERE id = {}".format(id)
        data = myDB.sql_selectFetchAll(sql)
        myDB.connEnd()
        return render(request, "memberApp\memberListOne.html", {"data": data[0], 'uName':request.session['loginName']})

# 會員查詢 (全部會員)
def memberListAll(request):
    main()
    if request.session.get("loginName") != None:
        if privilege_updated[int(request.session['loginLevel'])] == 1:
            if request.method == "POST":
                name = request.POST["name"]
                level = request.POST["level"]
                optLogic = request.POST["optLogic"]
                optMode = request.POST["optMode"]
                if name == "" and level == "":
                    message = "資料輸入有誤"
                    return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
                else:
                    # 如果名字和等級其中一個有值時
                    if len(name) > 0 and len(level) == 0:   # 只有name值時
                        key = name.split(" ")
                        tmp = ""
                        if optMode == "1":   # name精準比對
                            for i in key:
                                tmp = tmp + "name = " + '\'' + i + '\'' + ' OR '
                            tmp = tmp[:-3]
                            sql = "SELECT * FROM new_member WHERE " + tmp
                            # sql = "SELECT * FROM new_member WHERE name = '{}'".format(name)
                        else:    # name模糊比對, 模糊比對可以使用sql的AND
                            for i in key:
                                tmp = tmp + "name LIKE " + '\'%' + i + '%\'' + ' AND '
                            tmp = tmp[:-4]
                            sql = "SELECT * FROM new_member WHERE " + tmp
                            # sql = "SELECT * FROM new_member WHERE name LIKE '%{}%'".format(name)
                    elif len(name) == 0 and len(level) > 0: # 只有level值時
                        key = level.split(" ")
                        if optMode == "1":  # level精準比對
                            for i in key:
                                tmp = tmp + "level = " + '\'' + i + '\'' + ' OR '
                            tmp = tmp[:-3]
                            sql = "SELECT * FROM new_member WHERE " + tmp
                            # sql = "SELECT * FROM new_member WHERE level = '{}'".format(level)
                        else:   # level模糊比對
                            for i in key:
                                tmp = tmp + "level LIKE " + '\'%' + i + '%\'' + ' AND '
                            tmp = tmp[:-3]
                            sql = "SELECT * FROM new_member WHERE " + tmp
                            # sql = "SELECT * FROM new_member WHERE level LIKE '%{}%'".format(level)
                    else:
                        if optLogic == "and" and optMode == "1":    # and的精確比對
                            sql = "SELECT * FROM new_member WHERE level = '{}' AND name = '{}'".format(level,name)
                        elif optLogic == "and" and optMode == "2":  # and的模糊比對
                            sql = "SELECT * FROM new_member WHERE level LIKE '%{}%' AND name LIKE '%{}%'".format(level,name)
                        elif optLogic == "or" and optMode == "1":   # or的精確比對
                            sql = "SELECT * FROM new_member WHERE level = '{}' or name = '{}'".format(level,name)
                        else:   # or的模糊比對
                            sql = "SELECT * FROM new_member WHERE level LIKE '%{}%' OR name LIKE '%{}%'".format(level,name)
            else:
                sql = "SELECT * FROM new_member"
            data = myDB.sql_selectFetchAll(sql)
            myDB.connEnd()
            return render(request,"memberApp\memberListAll.html", {"data": data, 'uName':request.session['loginName']})
        else:
            message ="目前身分： 一般使用者，您無權限查看使用者列表。"
            return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
    else:
        message = "尚未登入，無法顯示會員列表"
        return render(request,"orderMessage.html", {"message": message, "login": 0})
        
# 會員查詢
def memberKeyQuery(request):
    if request.session.get("loginName") != None:
        if privilege_updated[int(request.session['loginLevel'])] == 1:
            return render(request,"memberApp\memberKeyQuery.html", {'uName':request.session['loginName']})
        else:
            message ="目前身分： 一般使用者，您無權限查詢使用者。"
            return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
    else:
        message = "尚未登入，無法查詢會員"
        return render(request,"orderMessage.html", {"message": message, "login": 0})
    

# 資料驗證
def memberValid(request,id=-1):
    data = MemberData()
    return render (request, r"memberApp/memberValid.html", {"data": data, "id": id, 'aa': request.session["loginName"]})

# 會員登入
def memberLogin(request):
    main()
    if request.method=="POST":
        account = request.POST["account"]
        passwd = request.POST["passwd"]
        sql = "SELECT name, level FROM new_member WHERE account = '{}' AND password = '{}'".format(account, passwd)
        data = myDB.sql_selectFetchOne(sql)
        myDB.connEnd()
        request.session["loginName"] = ""
        # 傳回使用者名稱及等級
        if data != None:
            request.session["loginName"] = data[0]
            request.session["loginLevel"] = data[1]
            return redirect ("/orderSystem/")
        else:
            del request.session["loginName"]
            # 登入失敗，回傳錯誤訊息
            message = "帳號密碼錯誤, 請再試一次"
            return render(request, "memberApp\memberLogin.html", {"message": message, "login":0})
        
    else:
        # 產生登入的空白頁面 帳號/密碼
        return render(request, "memberApp\memberLogin.html", {"login": 0})
        
# 會員登出
def memberLogout(request):
    if request.session.get("loginName") != None:
        del request.session['loginName']
        del request.session['loginLevel']
        return render(request,"memberApp\member.html", {"login": 0}) # 登出成功後，轉主功能頁
    else:
        message = "您尚未登入，無須登出"
        return render(request, "orderMessage.html",{"message": message})
