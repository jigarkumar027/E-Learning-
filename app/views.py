from django.shortcuts import render,redirect
from .models import *
from random import randint
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from .utils import *
import socket
socket.getaddrinfo('localhost',8080)

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Indexpage(request):
    if 'Email' in request.session and 'Password' in request.session:
        return render(request,'app/index.html')   
    else:
        return render(request,'app/index.html')   

def Indexpage2(request):

    if 'Email' in request.session and 'Password' in request.session:
        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        catdata = Cart12.objects.all().filter(Student_id_id = student) 
        print("Cart Data ------------------>",catdata)
        T = 0
        count = 0
        for i in catdata:
            T += i.Course_id.Price
            count += 1
        if T == 0 :
            return render(request,'app/index-2.html',{'cart123':catdata,'Count':count}) 
        else:
            return render(request,'app/index-2.html',{'cart123':catdata,'Total':T,'Count':count}) 
        #return render(request,"app/index-2.html")
    else:
        return render(request,'app/index-2.html')

def Indextutorpage2(request):
    if 'Email' in request.session and 'Password' in request.session:
        return render(request,"app/TutorIndex.html")
    else:
        return redirect('loginTutor')

def tutorpage(request):
    if 'Email' in request.session and 'Password' in request.session:
        uid = request.session['id']          
        udata = User.objects.get(id=uid)     
        if udata.Role=="Tutor":              
            tutor = Tutor.objects.get(user_id=udata)   
            cdata = Course.objects.filter(Tutor_id_id=tutor)
            scount = 0
            COURSE = 0
            T = 0
            # sdata = 0
            #print(scount)
            crt = 0
            for course in cdata:
                COURSE += 1
                #print(course)
                try:
                    print('lemon')
                    crt = Cart12.objects.all().filter(Course_id_id = course)
                    print(crt)
                    for cart13 in crt:
                        # sdata = Student.objects.all().filter(id = cart13.Student_id_id)
                        # print(cart13)
                        # for i in sdata:
                        scount+=1
                        T += cart13.Course_id.Price
                except:
                    pass
            return render(request,"app/Tutor/index-2.html",{'key2':tutor,'Scount':scount,'Course':COURSE,'Price':T,'sdata':crt}) 
        else: 
            print('not permitted')  
    else:
        return redirect('loginTutor')  

def RegisterPage(request):
    return render(request,"app/register.html") 

def LoginPage(request):
    return render(request,"app/login.html")  

def TutorRegister(request):
    return render(request,"app/TutorRegister.html")

def TutorLogin(request):
    return render(request,"app/TutorLogin.html")





def Otpvarify(request):
    gotp = request.POST['gotp']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email=email)
    if user:
        a = user.OTP
        b = otp
        if str(a) == str(b):
            print('varified')
            return redirect('loginpage')
        else:
            message = "OTP doesnot MATCH"
            return render(request,"app/otpverify.html",{'msg':message})
    else:
        message = "User Desnot Exist"
        return render(request,"app/register.html",{'msg':message})

def OtpvarifyTutor(request):
    gotp = request.POST['gotp']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email=email)
    if user:
        a = user.OTP
        b = otp
        if str(a) == str(b):
            print('varified')
            return redirect('TutorLogin')
        else:
            message = "OTP doesnot MATCH"
            return render(request,"app/otpvarifyTutor.html",{'msg':message})
    else:
        message = "User Desnot Exist"
        return render(request,"app/TutorRegister.html",{'msg':message})

def RegisterUser(request):
    if request.POST['role']=="Student":
        role = request.POST['role']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        contact = request.POST['contact']

        user = User.objects.filter(Email=email)
        if user:
            message = "User already Exist"
            return render(request,"app/register.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(10000,99999)
                newuser = User.objects.create(Username=username,Email=email,Password=password,Role=role,OTP=otp)
                email_subject = "Tutor email : Account Vericication"
                sendmail(email_subject,'mail_template',email,{'name':username,'otp':otp,'link':'http://localhost:8000/register/'})    
                newstudent = Student.objects.create(user_id=newuser,Contact=contact)
                return render(request,"app/otpverify.html",{'email':email,'otp':otp})
            else:
                message = "Password and Cpassword not Match"
                return render(request,"app/register.html",{'msg':message})
    else:
        role = request.POST['role']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        contact = request.POST['contact']

        user = User.objects.filter(Email=email)
        if user:
            message = "User already Exist"
            return render(request,"app/TutorRegister.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(10000,99999)
                newuser = User.objects.create(Username=username,Email=email,Password=password,Role=role,OTP=otp)
                email_subject = "Tutor email : Account Vericication"
                sendmail(email_subject,'mail_template',email,{'name':username,'otp':otp,'link':'http://localhost:8000/register/'})    
                
                newstudent = Tutor.objects.create(user_id=newuser,Contact=contact)
                return render(request,"app/otpvarifyTutor.html",{'email':email})
            else:
                message = "Password and Cpassword not Match"
                return render(request,"app/TutorRegister.html",{'msg':message})

           
def LoginUser(request):
    if request.POST['role'] == "Student":
        email = request.POST['email']
        password = request.POST['password']
        try:

            user = User.objects.get(Email=email)
        except:
            message = "Please Register yourself"
            return render(request,"app/login.html",{'msg':message})
        if user:
            if user.Password == password and user.Role == "Student":
                #stu = Student.objects.get(user_id=user) 
                request.session['Role'] = user.Role
                request.session['id']  = user.id
                request.session['Password'] = user.Password
                request.session['Username'] = user.Username
                request.session['Email'] = user.Email
                return redirect('indexpage2')
            else:
                message = "Password doesnot match"
                return render(request,"app/login.html",{'msg':message})
        else:
            message = "Please Register yourself"
            return render(request,"app/login.html",{'msg':message})
    else:
        print("TUTOR")

def LoginTutor(request):
    if request.POST['role'] == "Tutor":
        email = request.POST['email']
        password = request.POST['password']
        try :

            user = User.objects.get(Email=email)
            if user:
                if user.Password == password and user.Role == "Tutor":
                    stu = Tutor.objects.get(user_id=user)
                    request.session['Role'] = user.Role
                    request.session['id']  = user.id
                    request.session['Password'] = user.Password
                    request.session['Username'] = user.Username
                    request.session['Email'] = user.Email
                    
                    
                    return redirect('tutorpage') 
                else:
                    message = "Password doesnot match"
                    return render(request,"app/TutorLogin.html",{'msg':message})
            else:
                message = "Please Register yourself"
                return render(request,"app/TutorRegister.html",{'msg':message})
        except :
            message = "Please Register yourself"
            return render(request,"app/TutorRegister.html",{'msg':message})
    else:
        print("Student")

def TutorProfile(request,pk):
    if 'Email' in request.session and "Password" in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role == "Tutor":
            tutor = Tutor.objects.get(user_id=udata)
            return render(request,"app/Tutor/app-profile.html",{'key1':tutor})
    else:
        return redirect('loginTutor')

def studentprofile(request,pk):
    if 'Email' in request.session and "Password" in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role == "Student": 
            student = Student.objects.get(user_id=udata) 
            return render(request,"app/student_profile.html",{'key1':student})  
    else:
        return redirect('loginpage')

def studentdata(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role == "Student":
        sdata = Student.objects.get(user_id=udata)
        sdata.Firstname = request.POST['Firstname']
        sdata.Lastname = request.POST['Lastname']
        sdata.Email = request.POST['Email']
        sdata.Contact = request.POST['Contact']
        sdata.Address = request.POST['Address']
        sdata.Gender = request.POST['Gender']
        sdata.Qaulification = request.POST['Qaulification']
        sdata.DOB = request.POST['DOB']
        sdata.Country = request.POST['Country']
        sdata.State = request.POST['State']
        sdata.City = request.POST['City']
        #sdata.profile_Pic = request.FILES['profile_Pic'] 

        sdata.save()
        url = f"/sprofile/{pk}"
        return redirect(url) 

def profiledata(request,pk):
    udata = User.objects.get(id=pk)
    if udata.Role == "Tutor":
            tutor = Tutor.objects.get(user_id=udata)
            tutor.Firstname = request.POST['Firstname']
            tutor.Lastname = request.POST['Lastname']
            udata.Email = request.POST['Email']
            tutor.Contact = request.POST['Contact']
            tutor.Address = request.POST['Address']
            tutor.Gender = request.POST['Gender']
            tutor.Skills = request.POST['Skills']
            tutor.Qaulification = request.POST['Qaulification']
            tutor.Experience = request.POST['Experience']
            tutor.DOB = request.POST['DOB']
            tutor.Country = request.POST['Country']
            tutor.State = request.POST['State']
            tutor.City = request.POST['City']
            try:
                tutor.profile_Pic = request.FILES['profile_Pic'] 
                tutor.save()
                return redirect('tutorpage')
            except:
                tutor.save()
                #url = f"/tutorprofile/{pk}"
                #return redirect(url)
                return redirect('tutorpage') 

def addcatTutor(request):
    
    TutorID = request.session['id'] 
    if User.objects.get(id=TutorID).is_verifed == True:
        category = Category.objects.all()
        return render(request,"app/Tutor/add-courses.html",{'category':category})
    else:
        message = "WAIT FOR AUTHENTICATION"
        return render(request,'app/Tutor/index-2.html',{'msg':message})

def addcourseTutor(request):
    TutorID = request.session['id'] 
    if User.objects.get(id=TutorID).is_verifed == True:

        try:
            CourseID= int(request.POST['category'])  
            TutorID = request.session['id'] 
            tid = Tutor.objects.get(user_id=TutorID) 
            CourseName= request.POST['Name'] 
            CourseCode= request.POST['Code']  
            CourseDescription= request.POST['Detail']  
            CourseDuration= request.POST['Duration'] 
            CourseTech= request.POST['Technology']      
            CourseRequirment= request.POST['Pre_Requirment']  
            CoursePrice= request.POST['Price']  
            course_pic = request.FILES['courseimg']
            ddata = Category.objects.get(id=CourseID)  
            print(ddata.id)  
            
            coursedata = Course.objects.create(Tutor_id=tid,Category_id_id = ddata.id,course_pic=course_pic,Name = CourseName,Technology = CourseTech,Pre_Requirment= CourseRequirment,Code = CourseCode ,Description = CourseDescription,Duration = CourseDuration,Price=CoursePrice)
            return redirect('tutorpage')
        except Exception as e:
            print(" Add course Exception----------------->",e)
    else:
        message = "WAIT FOR AUTHENTICATION"
        return render(request,'app/Tutor/index-2.html',{'msg':message})


def showcourse(request):
    course = Course.objects.all()
    if 'Email' in request.session and "Password" in request.session:

        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        catdata = Cart12.objects.all().filter(Student_id_id = student) 
        print("Cart Data ------------------>",catdata)
        T = 0
        count = 0
        for i in catdata:
            T += i.Course_id.Price
            count += 1
        return render(request,'app/class-grid.html',{'keycourse':course,'cart123':catdata,'Total':T,'Count':count}) 
    else:
        return render(request,"app/class-grid.html",{'keycourse':course})

def coursedetail(request,pk):
    cdetail = Course.objects.get(id=pk)
    tdetail = Tutor.objects.get(id=cdetail.Tutor_id_id) 
    if 'Email' in request.session and "Password" in request.session:
            userid = request.session['id'] 
            student = Student.objects.get(user_id_id = userid)  
            catdata = Cart12.objects.all().filter(Student_id_id = student)  
            print("Cart Data ------------------>",catdata) 
            T = 0 
            count = 0 
            for i in catdata: 
                T += i.Course_id.Price 
                count += 1 

            return render(request,"app/class-details.html",{'keycourse':cdetail,'tdetails':tdetail,'cart123':catdata,'Total':T,'Count':count}) 
    else:
        return render(request,"app/class-details.html",{'keycourse':cdetail,'tdetails':tdetail})

def allcourse(request,pk): 
    cdata = User.objects.get(id=pk) 
    tdata = Tutor.objects.get(user_id_id=cdata.id)  
    if cdata.is_verifed == True:
        course = Course.objects.filter(Tutor_id_id=tdata.id) 
        return render(request,"app/Tutor/all-courses.html",{'ucourse':course}) 
    else:
        message = "WAIT FOR AUTHENTICATION"
        return render(request,'app/Tutor/index-2.html',{'msg':message})

def editcourse(request,pk): 
    codata = Course.objects.get(id=pk)
    return render(request,'app/Tutor/edit-courses.html',{'courseupdate':codata}) 

def updatecourse(request,pk):
    updatedata = Course.objects.get(id=pk)
    updatedata.Name= request.POST['Name'] 
    updatedata.Code= request.POST['Code']  
    updatedata.Detail= request.POST['Detail']  
    updatedata.Duration= request.POST['Duration'] 
    updatedata.Technology= request.POST['Technology']      
    updatedata.Pre_Requirment= request.POST['Pre_Requirment']  
    updatedata.Price= request.POST['Price']  
    updatedata.courseimg = request.FILES['courseimg']
    updatedata.save()
    tid = Course.objects.filter(Tutor_id_id = updatedata.Tutor_id_id)
    return  render(request,"app/Tutor/all-courses.html",{'ucourse':tid})

def deletecourse(request,pp):  
    course = Course.objects.get(id=pp)  
    tid = Course.objects.filter(Tutor_id_id = course.Tutor_id_id)
    
    course.delete()  
    #   course = Course.objects.filter(Tutor_id_id = tid) 
    return  render(request,"app/Tutor/all-courses.html",{'ucourse':tid}) 

def showcourses(request):
    course = Course.objects.all()
    if 'Email' in request.session and "Password" in request.session:

        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        catdata = Cart12.objects.all().filter(Student_id_id = student) 
        print("Cart Data ------------------>",catdata)
        T = 0
        count = 0
        for i in catdata:
            T += i.Course_id.Price
            count += 1
        return render(request,'app/shop-grid.html',{'shopcourse':course,'cart123':catdata,'Total':T,'Count':count}) 
    else:
        return render(request,'app/shop-grid.html',{'shopcourse':course})

def shopsingle(request,pk):
    cdetail = Course.objects.get(id=pk)
    #tdetail = Tutor.objects.get(id=cdetail.Tutor_id_id) 
    cat = Category.objects.get(id = cdetail.Category_id_id)
    if 'Email' in request.session and "Password" in request.session:

        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        catdata = Cart12.objects.all().filter(Student_id_id = student) 
        print("Cart Data ------------------>",catdata) 
        T = 0
        count = 0
        for i in catdata:
            T += i.Course_id.Price
            count+=1  

        return render(request,"app/shop-single.html",{'keycourse':cdetail,'category':cat,'Total':T,'Count':count})  
    else:
        return render(request,"app/shop-single.html",{'keycourse':cdetail})


def addcart(request,pk):
    if 'Email' in request.session and "Password" in request.session:
         
        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        cdata = Cart12.objects.filter(Student_id_id = student.id).values_list('Course_id_id',flat=True)
        print(cdata) 
        T = 0
        count = 0
        if pk not in  cdata: 
            
            cdetail = Course.objects.get(id=pk)  
            
            data = Cart12.objects.create(Course_id = cdetail ,Student_id = student,total = cdetail.Price,subtotal= cdetail.Price) 
            print('in cdata') 
            
            catdata = Cart12.objects.all().filter(Student_id_id = student)
            count = 0
            for i in catdata:
                T += i.Course_id.Price
                count += 1
            return render(request,'app/cart.html',{'cart123':catdata,'Total':T,'Count':count}) 
        else:
            catdata = Cart12.objects.all().filter(Student_id_id = student) 
            print("Cart Data ------------------>",catdata) 
            for i in catdata:
                T += i.Course_id.Price
                count+=1
            return render(request,'app/cart.html',{'cart123':catdata,'Total':T,'Count':count}) 
    else:
        message = "Please login yourself" 
        return render(request,"app/login.html",{'msg':message}) 

def deletecartpro(request,pk):
    cart = Cart12.objects.get(id=pk)
    uid = Cart12.objects.filter(Student_id_id = cart.Student_id_id)
    cart.delete()
    userid = request.session['id'] 
    student = Student.objects.get(user_id_id = userid) 
    #cdata = Cart12.objects.filter(Student_id_id = student.id).values_list('Course_id_id',flat=True)
    catdata = Cart12.objects.all().filter(Student_id_id = student) 
    print("Cart Data ------------------>",catdata) 
    T=0
    count = 0
    for i in catdata:
        T += i.Course_id.Price
        count += 1
    return  render(request,'app/cart.html',{'cart123':catdata,'Total':T,'Count':count}) 

def deletecartlittel(request,pk):
    cart = Cart12.objects.get(id=pk)
    uid = Cart12.objects.filter(Student_id_id = cart.Student_id_id)
    cart.delete()
    userid = request.session['id'] 
    student = Student.objects.get(user_id_id = userid) 
    #cdata = Cart12.objects.filter(Student_id_id = student.id).values_list('Course_id_id',flat=True)
    catdata = Cart12.objects.all().filter(Student_id_id = student) 
    print("Cart Data ------------------>",catdata) 
    T=0
    for i in catdata:
        T += i.Course_id.Price
    return  render(request,'app/index-2.html',{'cart123':catdata,'Total':T}) 



 
def studentlogout(request):

    del request.session['Email'] 
    del request.session['Password'] 
    request.session.modified = True
    #message = "Please login yourself" 
    return render(request,"app/index.html") 

def Totorlogout(request):
    del request.session['Email'] 
    del request.session['Password']
    request.session.modified = True
    return render(request,'app/index-2.html')

def checkout(request):
    if 'Email' in request.session and "Password" in request.session:
        T = 0
        userid = request.session['id'] 
        student = Student.objects.get(user_id_id = userid) 
        
        catdata = Cart12.objects.all().filter(Student_id_id = student) 
        print("Cart Data ------------------>",catdata) 
        for i in catdata:
            T += i.Course_id.Price
        return render(request,'app/checkout.html',{'cart123':catdata,'Total':T,'sdata':student})

def Students(request,pk):
    udata = User.objects.get(id=pk)                  
    tutor = Tutor.objects.get(user_id=udata)   
    cdata = Course.objects.filter(Tutor_id_id=tutor)
    coursename=[]
    Scourse = []
    # student = dict()
    crt = 0
    for course in cdata:
        coursename.append(course.Name)
        # student[course.Name]=[]
        try:
            crt = Cart12.objects.all().filter(Course_id_id = course)
            #print()
            Scourse.append(crt)
            # student[course.Name].append(crt)
        except:
            pass
    #print(student.values())
    # print(Scourse)
    #print(coursename)
    # print(crt)
    # print("data--------------------->")
    # print(Scourse)
    return render(request,"app/Tutor/all-students.html",{'sdata':crt,'Scourse1':Scourse}) 
       





############################################## admin panel ####################################
def adminpage(request):
    return render(request,"app/admin/login.html")

def AdminIndex(request):
    if 'username' in request.session and 'password' in request.session:
          catdata = Category.objects.all()
          catlen = len(catdata)
          return render(request,"app/admin/index.html",{'count':catlen}) 

def adminlogin(request):
    username = request.POST['username']
    password = request.POST['password']

    if username == "admin" and password == 'admin':
        request.session['username'] = username
        request.session['password'] = password
        return redirect('adminindex')
    else:
        message = "Username and Password doesnot match"
        return render(request,"app/admin/login.html",{'msg':message})
    

def AddCategory(request):
    if 'username' in request.session and 'password' in request.session:
        cname = request.POST['cname']

        catname = Category.objects.filter(Name=cname)
        if catname:
            message = "Category already added"
            return render(request,"app/admin/index.html",{'msg':message})
        else:
            newcat = Category.objects.create(Name=cname)
            message = "Category Add successfully"
            
            return render(request,"app/admin/index.html",{'msg':message})
    else:
        return redirect('adminlogin')

def showcat(request):
      if 'username' in request.session and 'password' in request.session:
          catdata = Category.objects.all()
          return render(request,'app/admin/categories.html',{'keycat':catdata})
      else:
          return redirect('adminlogin')
    
def editcat(request,pk):
    if 'username' in request.session and 'password' in request.session:
        catdata = Category.objects.get(id=pk)
        return render(request,"app/admin/editcat.html",{'keyedit':catdata})
    else:
        return redirect('adminlogin')

def updatecat(request,pk):
    if 'username' in request.session and 'password' in request.session:
        updatedata = Category.objects.get(id=pk)
        updatedata.Name = request.POST['Categories']
        updatedata.save()
        return redirect('showcat')
    else:
        return redirect('adminlogin')


def deletecat(request,pk):
    if 'username' in request.session and 'password' in request.session:
        catdata = Category.objects.get(id=pk)
        catdata.delete()
        return redirect('showcat')
    else:
        return redirect('adminlogin')

def adminlogout(request):

    del request.session['username'] 
    del request.session['password'] 
    request.session.modified = True
    return redirect('adminindex')




############################################# Paytm Block #################################################

def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        amount = int(request.POST['sub_total'])
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print(err)
        return render(request, 'app/checkout.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)
