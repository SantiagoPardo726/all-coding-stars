from fastapi import FastAPI, Form,Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from extract import *
import extract


#
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def form(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/",response_class=HTMLResponse)
def form(request:Request, links: str = Form(...)):
    print(links)
    lst = links.split("\n")
    message = ""
    cont = 1
    for i in lst:
        print(i)
        mes = getMessaje(i)
        message += str(cont) + ")"+mes
        cont += 1
        
        
    return templates.TemplateResponse("index.html",{"request":request,"message":message})

def getMessaje(url):
    message = ""
    if extract.verifyHindi(url):
        pass
    else:
        return "Wrong page"
    if extract.verifyImage(url):
        pass
    else:
        message += "Images not high resolution; \n"
    if extract.verifyInside(url):
        pass
    else:
        message += "Inner pages not translated; \n"
    if extract.verifyDropDownMenu(url):
        pass
    else:
        message += "Javascript dropdown not working properly;\n"
    if message == "":
        return "Pass"
    else:
        return "Fail: "+message




