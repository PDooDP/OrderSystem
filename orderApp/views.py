from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from myapp.dbConn import *
import pymysql
# Create your views here.
orderlist = []

# 初始化程式
# 建立資料庫連線

def main():
    global myDB
    db = pymysql.connect(host="127.0.0.1", user="username", passwd="password", database="your_database_name")
    myDB = dbConn(db)

main()

# level 0 ~ 9
# 1代表有權限 0代表沒有
# createMenu
# 1. 0~1 管理者，2. 2~9 一般使用者
privilegeCreateMenu=[1,1,0,0,0,0,0,0,0,0]
privilegeSelectMenu=[1,1,1,1,1,1,1,1,0,0]
def orderAppHome(request):
    if request.session.get("loginName") != None:
        return render(request, "orderApp\orderAppHome.html",{"loginName": request.session['loginName']})
    else:
        return render(request, "orderApp\orderAppHome.html", {"login": 0})

#設定 可選擇的 餐廳名稱，只能設定一間餐廳
# 選擇今日餐廳
def orderMenu(request):
    main()
    if request.session.get('loginName') != None: #權限判定 1:有權限
        if privilegeCreateMenu[int(request.session["loginLevel"])] == 1:
            #修正資料庫會員資料，使用 id欄位
            if request.method == "POST":
                rName = request.POST["rName"]   #網頁回傳餐廳名稱
                del_sql = "DELETE FROM menu"    #先刪除menu舊資料
                # 先刪除menu舊資料
                myDB.sql_execute(del_sql)
                del_sql = "DELETE FROM cart"    #再刪除cart裡所有的資料
                myDB.sql_execute(del_sql)

                # 先檢查回傳餐廳名稱是否存在Restaurant資料表中
                main()
                sql = "SELECT * FROM restaurant WHERE name = '{}'".format(rName)
                data = myDB.sql_selectFetchAll(sql)
                if len(data) != 0:  #餐廳名稱是否存在Restaurant資料表中
                    # 將回傳餐廳名稱寫入menu表單
                    sql = "INSERT INTO menu (rName) VALUES ('{}')".format(rName)
                    myDB.sql_execute(sql)
                    myDB.connEnd()
                    return redirect("/orderCartList/")
                else:
                    message = "無餐廳資料"
                    return render(request, "orderMessage.html",{"message": message})
            else:
                # 尋找所有在Restaurant的餐廳名稱，傳給網頁做選單
                sql = "SELECT DISTINCT name FROM restaurant"
                data = myDB.sql_selectFetchAll(sql)
                myDB.connEnd()
                return render(request, r"orderApp\orderMenu.html", {'data': data, 'uName':request.session['loginName']})
        else:
            message = "目前身分： 一般使用者，您無權限選擇餐廳。"
            return render(request, r'orderMessage.html', {"message": message, 'uName':request.session['loginName']})
    else:
        message = "尚未登入"
        return render(request, "orderMessage.html",{"message": message, "login": 0})

# 取得餐點購物車資料
def orderCartList(request):
    main()
    # 取得資料庫內購物車的資料
    if request.session.get('loginName') != None:
        sql = "SELECT * FROM cart"
        data = myDB.sql_selectFetchAll(sql)
        sql = "SELECT SUM(fPrice) FROM cart;"
        sum = myDB.sql_selectFetchOne(sql,0)
        if sum == None:
            total = 0
        else:
            total = sum
        myDB.connEnd()
        return render(request,"orderApp\orderCartList.html",{"data": data, "uName":request.session["loginName"], "total": total})
    else:
        message = "尚未登入"
        return render(request, "orderMessage.html",{"message": message, "login": 0})
      
# 訂購餐點
def orderSelectCart(request, id):
    main()
    message = ""
    if request.session.get('loginName') != None:
        sql = "SELECT * FROM restaurant WHERE id = {}".format(id)   # 取得目前登入的ID
        data = myDB.sql_selectFetchone(sql)
        fName = data[2]
        fPrice = data[4]
        fQuanity = 1    # 暫定一次只能訂購一個餐點
        uName = request.session["loginName"]
        sql = "INSERT INTO cart (fName, fPrice, fQuantity, uName) VALUES ('{}',{},{},'{}')".format(fName,fPrice, fQuanity, uName)
        myDB.sql_execute(sql)
        myDB.connEnd()
        message = fName + " 訂購成功"
    return render(request, r"orderApp\orderSelect.html", {'rName': rName, "rdata": rdata, 'uName':request.session['loginName'],"message":message})

# 餐廳菜單
def orderSelect(request):
    global rdata, rName
    main()
    if request.session.get('loginName') != None: #權限判定 1:有權限
        if privilegeSelectMenu[int(request.session["loginLevel"])] == 1:
            #修正資料庫會員資料，使用 id欄位
            if request.method == "POST":
                pass
            else:
                sql = "SELECT * FROM menu"
                rName = myDB.sql_selectFetchOne(sql,0)
                # 尋找所有在Restaurant的餐廳名稱，傳給網頁做選單
                sql = "SELECT * FROM restaurant WHERE name = '{}'".format(rName)
                rdata = myDB.sql_selectFetchAll(sql)
                myDB.connEnd()
                return render(request, r"orderApp\orderSelect.html", {'rName': rName, "rdata": rdata, 'uName':request.session['loginName']})
        else:
            message = "無權限"
            return render(request, "orderMessage.html",{"message": message})
    else:
        message = "尚未登入"
        return render(request, "orderMessage.html",{"message": message, "login": 0})

# 新增餐廳及餐點資料
def orderRestaurant(request):
    main()
    if request.session.get('loginName') != None: #權限判定 1:有權限
        if privilegeCreateMenu[int(request.session["loginLevel"])] == 1:
            if request.method == "POST":
                name = request.POST["name"]
                food = request.POST["food"]
                price = request.POST["price"]
                foodNote = request.POST["foodNote"]

                sql = "SELECT * FROM restaurant WHERE name = '{}' and food = '{}'".format(name, food)
                data = myDB.sql_selectFetchAll(sql)
                if len(data) == 0:
                    sql = "INSERT INTO restaurant (name, food, price, foodNote) VALUES ('{}','{}','{}','{}')".format(name, food, price, foodNote)
                    myDB.sql_execute(sql)
                    myDB.connEnd()
                    Msg = "資料新增成功"
                    return redirect("/orderRestaurant/")
                else:
                    myDB.connEnd()
                    message = "重複資料，是否帶入Update <a href='orderUpdate\{}'".format(data[0])
                    return render(request, "orderMessage.html",{"message": message})
            else:
                return render(request, "orderApp\orderRestaurant.html", {'uName': request.session['loginName']})
        else:
            message = "目前身分： 一般使用者，您無權限新增餐廳資料。"
            return render(request, r'orderMessage.html', {"message": message, 'uName':request.session['loginName']})
    else:
        message = "尚未登入"
        return render(request, "orderMessage.html",{"message": message, "login": 0}) 

# 餐點刪除
def orderDelete(request, id=-1):
    main()
    if request.session['loginName'] != "" or request.session['loginName'] == None:
        if privilegeCreateMenu[int(request.session['loginLevel'])] == 1:
        # 修正資料庫訂餐資料，使用cart id欄位
            if id != -1:
                del_sql = "DELETE FROM cart WHERE id = {}".format(id)
                myDB.sql_execute(del_sql)
                myDB.connEnd()
                return redirect("/orderCartList/")
            else:
                message = "無id資料!"
                return render(request, "orderMessage.html",{"message": message})
        else: 
            message ="目前身分： 一般使用者，您無權限刪除餐點資料，如需協助，請洽管理員。"
            return render(request, "orderMessage.html",{"message": message, 'uName':request.session['loginName']})
    else:
        message = "無id"
        return render(request, "orderMessage.html",{"message": message})

