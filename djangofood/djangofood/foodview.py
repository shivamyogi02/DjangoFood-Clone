from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from . import pool
import os


def FoodInterface(request):
    return render(request, "foodinterface.html")


def FetchAllFoodTypes(request):
    DB, SMT = pool.OpenConnection()
    SMT.execute("select * from foodtype")
    records = SMT.fetchall()
    print(records)
    return JsonResponse(records, safe=False)


def FetchAllFoodItems(request):
    try:
        DB, SMT = pool.OpenConnection()
        SMT.execute(
            "select * from fooditem where foodtypeid={0}". format(request.GET['foodtypeid']))
        records = SMT.fetchall()
        print(records)
        return JsonResponse(records, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)


def FoodSubmit(request):
    try:
        if request.method == 'POST':
            DB, SMT = pool.OpenConnection()
            foodtypeid = request.POST['foodtypeid']
            fooditemid = request.POST['fooditemid']
            foodstatus = request.POST['foodstatus']
            description = request.POST['description']
            price = request.POST['price']
            offer = request.POST['offer']
            picture = request.FILES['picture']

            q = "insert into foodlist(foodtypeid, fooditemid, foodstatus, description, price, offer, picture)values({0},{1},'{2}','{3}',{4},{5},'{6}')".format(foodtypeid, fooditemid, foodstatus, description, price, offer, picture)
            print("query",q)
            SMT.execute(q)
            F = open("d:/djangofood/assets/"+picture.name, "wb")
            for chunck in picture.chunks():
                F.write(chunck)
            F.close()

            DB.commit()

        return render(request, "FoodInterface.html", {'status': True, 'message': "Record Submitted"})
    except Exception as e:
        return render(request, "FoodInterface.html", {'status': False, 'message': "Server Error"})


def FetchAllRecords(request):
    try:
        DB, SMT = pool.OpenConnection()
        SMT.execute("select FL.*,(select FT.foodtype from foodtype FT where FT.foodtypeid=FL.foodtypeid) as foodtype, (select FI.fooditem from fooditem FI where FI.fooditemid=FL.fooditemid) as food from foodlist FL")
        records = SMT.fetchall()
        print(records)
        return render(request, "DisplayAllRecords.html", {'data': records})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllRecords.html", {'data': []})


def DisplayById(request):
    try:
        foodid = request.GET['foodid']
        DB, SMT = pool.OpenConnection()
        SMT.execute(
            "select FL.*,(select FT.foodtype from foodtype FT where FT.foodtypeid=FL.foodtypeid) as foodtype, (select FI.fooditem from fooditem FI where FI.fooditemid=FL.fooditemid) as food from foodlist FL where foodlistid={0}".format(foodid))
        records = SMT.fetchone()
        if (records):
            status = False
            if (records['foodstatus'] == "Veg"):
                status = True
            else:
                status = False

            return render(request, "DisplayById.html", {'data': records, 'status': status})
        else:
            return render(request, "DisplayById.html", {'data': []})
    except Exception as e:
        print(e)
        return render(request, "DisplayById.html", {'data': []})


def Edit_Food_Data(request):
    try:
        if request.method == 'POST':
            DB, SMT = pool.OpenConnection()
            if (request.POST['btn'] == 'Edit'):
                foodlistid = request.POST['foodlistid']
                foodtypeid = request.POST['foodtypeid']
                fooditemid = request.POST['fooditemid']
                foodstatus = request.POST['foodstatus']
                description = request.POST['description']
                price = request.POST['price']
                offer = request.POST['offer']

                q = "update foodlist set foodtypeid={0}, fooditemid={1}, foodstatus='{2}', description='{3}', price={4}, offer={5} where foodlistid={6}".format(foodtypeid, fooditemid, foodstatus, description, price, offer, foodlistid)
                SMT.execute(q)

                DB.commit()

            else:
                foodlistid = request.POST['foodlistid']
                q = "delete from foodlist where foodlistid={0}".format(
                    foodlistid)
                SMT.execute(q)

                DB.commit()

        return redirect('/fetchallrecords')
    except Exception as e:
        print(e)
        return redirect('/fetchallrecords')

def DisplayPicture(request):
     print("Req", dict(request.GET))
     return render(request, "DisplayPicture.html", {'data': dict(request.GET)})

def Edit_Picture(request):
    try:
        if request.method == 'POST':
            DB, SMT = pool.OpenConnection()
            foodid = request.POST['foodid']
            picture = request.FILES['picture']
            oldfile = request.POST['oldfile']
            q = "update foodlist set picture='{0}' where foodlistid={1}".format(picture.name,foodid)
            print("query",q)
            SMT.execute(q)
            F = open("d:/djangofood/assets/"+picture.name, "wb")
            for chunck in picture.chunks():
                F.write(chunck)
            F.close()
            os.remove('/static/{0}'.format(oldfile))

            DB.commit()
            return redirect('/fetchallrecords')

    except Exception as e:
            return redirect('/fetchallrecords')
