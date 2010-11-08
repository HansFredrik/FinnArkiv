'''
Created on Sep 23, 2010

@author: Hansi
'''
import settings
from django.core.management import setup_environ
setup_environ(settings)
from web.models import CarClassified, Make, Model

def uniquify(seq, idfun=None): 
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result
    
def parseMakeModel():
    makes = CarClassified.objects.all()
    makes = uniquify(makes)  
    for _make in makes:
        make = Make()
        make.make = _make.make
        make.count = len(CarClassified.objects.all().filter(make=_make.make))
        make.save()
        
        models = CarClassified.objects.all().filter(make=_make.make)
        models = uniquify(models)
        for _model in models:
            model = Model()
            model.model = _model.model
            model.make = make
            model.count = len(CarClassified.objects.all().filter(model=model.model))
            model.save()
            
def parseMakeSql():
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT make FROM web_carclassified")
    makes = cursor.fetchall()
    
    for make in makes:
        _make = Make()
        _make.make = str(make[0])
        cursor.execute("SELECT count(*) FROM web_carclassified WHERE make = '" + str(make[0]) + "'")
        _make.count = int(cursor.fetchone()[0])
        _make.save()

def parseModelSql():
    from django.db import connection, transaction
    cursor = connection.cursor()
    makes = list(Make.objects.all())
    
    for make in makes:
        cursor.execute("SELECT DISTINCT model FROM web_carclassified WHERE make = '" + str(make.make) + "'")
        models = cursor.fetchall()
        for model in models:
            modelname = str(model[0]).replace("'", "''") #Escape apostrophe, Kia Cee'd :)
            _model = Model()
            _model.make = make
            _model.model = modelname
            cursor.execute("SELECT count(*) FROM web_carclassified WHERE model = '" + modelname + "' AND make = '" + make.make + "'")
            _model.count = int(cursor.fetchone()[0]) 
            _model.save()
        
#Run parser
parseMakeSql()
parseModelSql()
