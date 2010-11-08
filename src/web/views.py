from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from web.models import CarClassified, Make, Model

def splitthousands(s, sep='.'):  
    if len(s) <= 3: return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]

def index(request):
    #makes = MakeModel.objects.raw('SELECT DISTINCT id,make FROM web_makemodel ORDER BY make')
    makes = Make.objects.all().order_by('make')
    count = splitthousands(str(CarClassified.objects.all().count()))
    
    t = loader.get_template('index.html')
    c = Context({
                 'makes' : makes, 
                 'count' : count,  
    })
    return HttpResponse(t.render(c))

def make(request):
    _make = Make.objects.get(make=request.GET['make'])
    models = Model.objects.all().filter(make=_make).order_by('model')
    count = splitthousands(str(CarClassified.objects.all().count()))
    
    t = loader.get_template('make.html')
    c = Context({
                 'make' : request.GET['make'],
                 'models' : models,  
                 'count' : count, 
    })
    return HttpResponse(t.render(c))

def model(request):
    classifieds = []
    # If search fields filled out
    if request.method == 'POST':
        classifieds = CarClassified.objects.filter(make=request.GET['make']).filter(model=request.GET['model'])
        if request.POST['pricegte']:
            classifieds = classifieds.filter(price__gte=request.POST['pricegte'])
        if request.POST['pricelte']:
            classifieds = classifieds.filter(price__lte=request.POST['pricelte'])
        if request.POST['regno']:
            classifieds = classifieds.filter(regno=request.POST['regno'])
    else:
        classifieds = CarClassified.objects.all().filter(make=request.GET['make'], model=request.GET['model'])
        
    count = splitthousands(str(CarClassified.objects.all().count()))
    
    t = loader.get_template('model.html')
    c = Context({
                 'make' : request.GET['make'],
                 'model' : request.GET['model'],
                 'classifieds' : classifieds,   
                 'count' : count,
    })
    return HttpResponse(t.render(c))

def classified(request):
    classified = CarClassified.objects.get(finnid=request.GET['classifiedid'])
    count = splitthousands(str(CarClassified.objects.all().count()))
    
    t = loader.get_template('classified.html')
    c = Context({
                 'classified' : classified,   
                 'count' : count,
    })
    return HttpResponse(t.render(c))

def search(request):
    classifieds = []
    if request.method == 'POST':
        if request.POST['regno']:
            classifieds = CarClassified.objects.filter(regno=request.POST['regno'])
    count = splitthousands(str(CarClassified.objects.all().count()))
    
    t = loader.get_template('search.html')
    c = Context({
                 'classifieds' : classifieds, 
                 'count' : count,  
    })
    return HttpResponse(t.render(c))
