from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests
import time
from random import randint
import random
from time import sleep

# Create your views here.

class LoginView(View):

    def get(self,request):
        template_name = "login.html"
        context = {}
        return render(request, template_name, context)

    def post(self,request):
        if request.method == "POST":
            # check user and password is authenticated or not
            user = authenticate(username=request.POST["username"],password=request.POST["pass"])
            if user is not None:
                # go to login
                login(request,user)
                return redirect('index/')
            else:
                return render(request,template_name="login.html",context={
                    "error":"Invalid Login Credentials"
                })
        else:
            return render(request,template_name="login.html")

class SignupView(View):

    def get(self,request):
        template_name = "registration.html"
        context = {}
        return render(request, template_name, context)

    def post(self,request):
        template_name = "registration.html"
        print("Request Data :",request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print("User Name :",username)
        print("User email :",email)
        print("User password :",password)
        print("User confirm_password :",confirm_password)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        if request.method == "POST":
            # to create a user
            if password == confirm_password:
                try:
                    user = User.objects.get(username=username)
                    context = {
                        "error":"User name Is Already Taken"
                    }
                    return render(request,template_name,context)
                except User.DoesNotExist:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    return redirect('/')
            else:
                context = {
                    "error":"Passwords does not match !"
                }
                return render(request,template_name,context)
        else:
            return render(request,template_name)

@login_required(login_url='/')
def IndexView(request):
    template_name = "index.html"
    print("request.user :",request.user)
    quertset = User.objects.get(username=request.user)
    print("User Id :",quertset.email)
    context = {
        "usename":request.user
    }
    return render(request, template_name, context)


# class IndexView(View):
#
#     @login_required(login_url='/')
#     def get(self,request):
#         template_name = "index.html"
#         print("request.user :",request.user)
#         quertset = User.objects.get(username=request.user)
#         print("User Id :",quertset.email)
#         context = {
#             "usename":request.user
#         }
#         return render(request, template_name, context)
#
#     def post(self,request):
#         self.get(request)

class LogoutView(View):

    def get(self,request):
        logout(request)
        return redirect('/')

    def post(self,request):
        self.get(request)

@login_required(login_url='/')
def UserProfileView(request):
    template_name = "profile.html"
    print("request.user : ",request.user)
    queryset = User.objects.get(username=request.user)
    context = {
        "username": queryset.username,
        "email": queryset.email,
        "password": queryset.password
    }
    return render(request, template_name, context)

def getRequest(websiteUrl):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
        # hit the website url
        session = requests.Session()
        response = session.get(websiteUrl, headers=headers, verify=False)

        if response.status_code == 200:
            sleep(randint(1, 1))
            beautifyData = BeautifulSoup(response.content, 'html.parser')
            return beautifyData
        else:
            return None
    except Exception as e:
        print("Error IN : Custom Error in getRequest",e)


class GetAllUrlsView(View):

    def get(self,request):
        self.get(request)

    def post(self,request):
        template_name = "index.html"
        search_term = request.POST["search_term"]
        print("$$$$$$$$$$$$$$$$$$$$$$$$")
        print(search_term)
        print("$$$$$$$$$$$$$$$$$$$$$$$$")
        if search_term:
            base_url = 'https://www.google.com/search?q={0}'.format(search_term)

        soup = getRequest(base_url)

        print("Soup Html :",soup)

        wrong_search_keyword = 'Your search - ' + search_term + ' - did not match any documents.'

        if soup == None:
            return HttpResponse("Something Went Wrong!!! Please try again")
        else:
            soup_page_for_wrong_input = soup.findAll('div', {'class': 'card-section'})

            if soup_page_for_wrong_input :
                for wrong in soup_page_for_wrong_input:
                    if wrong.select('p'):
                        if wrong.select('p')[0].get_text() == wrong_search_keyword:
                            print("did not match any documents.!!!!!!")
                            context = {
                                "status":True,
                                "result_status":False,
                                "result": "Your search - {} - did not match any documents.".format(search_term)
                            }
                            return render(request,template_name,context)

            list_of_urls_and_description = []
            rating_count = 5
            all_matching_urls = soup.findAll('h3',{'class':'LC20lb DKV0Md'})
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            for url in all_matching_urls:
                # print(url.find_previous('a').get("href"))
                # print(url.find_next('div',{'class':'s'}).find_next('span',{'class':'st'}).get_text())
                # list_of_url_description.append(url.find_next('div',{'class':'s'}).find_next('span',{'class':'st'}).get_text())
                # list_of_urls.append(url.find_previous('a').get("href"))
                answer_dict = {
                    "link":url.find_previous('a').get("href"),
                    # "description":url.find_next('div',{'class':'s'}).find_next('span',{'class':'st'}).get_text(),
                    "rating":range(rating_count)
                }
                list_of_urls_and_description.append(answer_dict)
                rating_count -= 1

            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(list_of_urls_and_description)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            context = {
                "status": True,
                "result_status": True,
                "usename": request.user,
                "result":list_of_urls_and_description,
                "search_term":search_term
            }
            return render(request, template_name, context)