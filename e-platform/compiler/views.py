from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Pyquestions,Pytestcases,Pytrack,Student,Ctrack,Cquestions,Ctestcases
import re
import requests
from django.contrib import messages
from staff.models import Quiz,Question,Answer,QuizTaker,UsersAnswer

# Create your views here.

def index(request):
    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=name).exists():
                 messages.success(request,'User exists')  
            elif User.objects.filter(email=email).exists():
                 messages.success(request,'Email taken')
            else:
                user=User.objects.create_user(username=name,password=password1,email=email)
                user.save();
                s=Student(user=user)
                s.save()
                messages.success(request,'User registration successful')
                             
        else:    
             messages.success(request,'Passwords not matching')
        return redirect('/')    
    else:    
        return render(request,'/')

def login(request):
    if request.method=="POST":
        username=request.POST['name']
        password=request.POST['email']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if request.user.is_staff:
                return render(request,'staff.html')
            return render(request,'index.html')
        else:
            messages.info(request,'Invalid credintials')
            return redirect('/')    

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)  
        return redirect('/')

def home(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        return render(request,'index.html')
    else:
        return render(request,'home.html')

def ccoding(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        c=Cquestions.objects.all()
        return render(request,'ccoding.html',{'c':c})
    else:
        return render(request,'home.html')

def pcoding(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        p=Pyquestions.objects.all()
        return render(request,'pcoding.html',{'p':p})
    else:
        return render(request,'home.html')



def pyquestions(request,id):
    if request.user.is_authenticated and request.user.is_staff==False:
        q=Pyquestions.objects.filter(id=id)
        t=Pytestcases.objects.filter(question=id)[0]
        p=Pytrack.objects.filter(user=request.user,question_id=id)
        return render(request,'pyeditor.html',{'q':q,'t':t,'p':p})
    else:
        return render(request,'home.html')

def cquestions(request,id):
    if request.user.is_authenticated and request.user.is_staff==False:
        q=Cquestions.objects.filter(id=id)
        t=Ctestcases.objects.filter(question=id)[0]
        p=Ctrack.objects.filter(user=request.user,question_id=id)
        return render(request,'editor.html',{'q':q,'t':t,'p':p})
    else:
        return render(request,'home.html')

def pyevaluate(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        if request.method=="POST" and "btnrun" in request.POST:
            id=request.POST['qid']
            code=request.POST['code']
            inputs=request.POST['pyinput']
            url="https://tpcg.tutorialspoint.com/tpcg.php"
            data={
            'lang': 'python3',
            'device': '',
            'code': code,
            'stdinput':inputs,
            'ext': 'py',
            'compile': 0,
            'execute': 'python3 main.py',
            'mainfile': 'main.py',
            'uid': '154567',
            }
            r=requests.post(url,data=data)
            content=r.text
            
            stripped = re.sub('<[^<]+?>', '', content)
            #stripped=stripped[425:]
            s='$python3 main.py'
            if s in stripped:
                stripped=stripped[len(s):]
            q=Pyquestions.objects.filter(id=id)
            t=Pytestcases.objects.filter(question=id)[0]
            p=Pytrack.objects.filter(user=request.user,question_id=id)
            return render(request,'pyeditor.html',{'q':q,'t':t,'p':p,'code':code,'input':inputs,'output':stripped})
        elif request.method=="POST" and "btneval" in request.POST:

            id=request.POST['qid']
            code=request.POST['code']
            inputs=request.POST['pyinput']
            count=0
            t=Pytestcases.objects.filter(question=id)
            c=Pytestcases.objects.filter(question=id).count()
            inp=[]
            out=[]
            for i in t:
                inp.append(i.testinput)
                out.append(i.testoutput)
            for i in range(c):
                ins=inp[i]
                if '\r\n' in ins:
                    ins=re.sub('\r\n','\n',ins)
                else:
                    ins=ins+'\n'
                url="https://tpcg.tutorialspoint.com/tpcg.php"
                data={
                'lang': 'python3',
                'device': '',
                'code': code,
                'stdinput':ins,
                'ext': 'py',
                'compile': 0,
                'execute': 'python3 main.py',
                'mainfile': 'main.py',
                'uid': '154567',
                }
                r=requests.post(url,data=data)
                content=r.text
                stripped = re.sub('<[^<]+?>', '', content)
                s='$python3 main.py'
                
                if '\r\n' in out[i]:
                    out[i]=re.sub('\r\n','\n',out[i])
                else:
                    out[i]=out[i]+'\n'    

                if s in stripped:
                    stripped=stripped[len(s):]
                l=list(stripped) 
                k=list(out[i])  
                x=out[i] 
                if stripped==out[i]:
                    count+=10
            messages.info(request,"Your submission has got {}/{} points!".format(count,c*10))   
            q=Pyquestions.objects.filter(id=id)
            t=Pytestcases.objects.filter(question=id)[0]
            if c*10==count:
                q=Pyquestions.objects.get(id=id)
                if Pytrack.objects.filter(user=request.user,question=q).count()==0:
                    st=Student.objects.get(user=request.user)
                    st.pyscore=st.pyscore+count
                    st.save()
            q=Pyquestions.objects.get(id=id)
            pt=Pytrack(user=request.user,question=q,code=code,score=count)
            pt.save()
            q=Pyquestions.objects.filter(id=id)
            p=Pytrack.objects.filter(user=request.user,question_id=id)
            return render(request,'pyeditor.html',{'q':q,'t':t,'p':p,'code':code,'input':inputs})
    else:
        return render(request,'home.html')

def cevaluate(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        if request.method=="POST" and "btnrun" in request.POST:
            id=request.POST['qid']
            code=request.POST['code']
            inputs=request.POST['pyinput']
            url="https://tpcg.tutorialspoint.com/tpcg.php"
            data={
            'lang': 'c',
            'device': '',
            'code': code,
            'stdinput':inputs,
            'ext': 'c',
            'compile': 'gcc -o main *.c',
            'execute': 'main',
            'mainfile': 'main.c',
            'uid': '154567',
            }
            r=requests.post(url,data=data)
            content=r.text
            
            stripped = re.sub('<[^<]+?>', '', content)
            #stripped=stripped[425:]
            s="$gcc -o main *.c$main"
            if s in stripped:
                stripped=stripped[len(s):]
            q=Cquestions.objects.filter(id=id)
            t=Ctestcases.objects.filter(question=id)[0]
            p=Ctrack.objects.filter(user=request.user,question_id=id)
            return render(request,'editor.html',{'q':q,'t':t,'p':p,'code':code,'input':inputs,'output':stripped})
        elif request.method=="POST" and "btneval" in request.POST:
            print('===================================================================')
            id=request.POST['qid']
            code=request.POST['code']
            inputs=request.POST['pyinput']
            count=0
            t=Ctestcases.objects.filter(question=id)
            c=Ctestcases.objects.filter(question=id).count()
            inp=[]
            out=[]
            for i in t:
                inp.append(i.testinput)
                out.append(i.testoutput)
            print(inp,out)
            for i in range(c):
                ins=inp[i]
                if '\r\n' in ins:
                    ins=re.sub('\r\n','\n',ins)
                else:
                    ins=ins+'\n'
                url="https://tpcg.tutorialspoint.com/tpcg.php"
                data={
                'lang': 'c',
                'device': '',
                'code': code,
                'stdinput':ins,
                'ext': 'c',
                'compile': 'gcc -o main *.c',
                'execute': 'main',
                'mainfile': 'main.c',
                'uid': '154567',
                }
                r=requests.post(url,data=data)
                content=r.text
                stripped = re.sub('<[^<]+?>', '', content)
                s="$gcc -o main *.c$main"
                
                if '\r\n' in out[i]:
                    out[i]=re.sub('\r\n','\n',out[i])
                else:
                    out[i]=out[i]+'\n'    

                if s in stripped:
                    stripped=stripped[len(s):]
                l=list(stripped) 
                k=list(out[i])  
                x=out[i] 
                print(stripped,x)
                if stripped == out[i]:
                    count+=10
            messages.info(request,"Your submission has got {}/{} points!".format(count,c*10))   
            q=Cquestions.objects.filter(id=id)
            t=Ctestcases.objects.filter(question=id)[0]
            print(c,count)
            if c*10==count:
                q=Cquestions.objects.get(id=id)
                if Ctrack.objects.filter(user=request.user,question=q).count()==0:
                    st=Student.objects.get(user=request.user)
                    st.cscore=st.cscore+count
                    st.save()
            q=Cquestions.objects.get(id=id)
            pt=Ctrack(user=request.user,question=q,code=code,score=count)
            pt.save()
            q=Cquestions.objects.filter(id=id)
            p=Ctrack.objects.filter(user=request.user,question_id=id)
            return render(request,'editor.html',{'q':q,'t':t,'p':p,'code':code,'input':inputs})
    else:
        return render(request,'home.html')


def pleader(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        p=Student.objects.all()
        return render(request,'pleader.html',{'p':p})
    else:
        return render(request,'home.html')

def pcode(request,id):
    if request.user.is_authenticated and request.user.is_staff==False:
        c=Pytrack.objects.filter(id=id)
        return render(request,'pcode.html',{'c':c})
    else:
        return render(request,'home.html')

def csubmit(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        c=Ctrack.objects.filter(user=request.user)
        return render(request,'psubmit.html',{'p':c})
    else:
        return render(request,'home.html')

def ccode(request,id):
    if request.user.is_authenticated and request.user.is_staff==False:
        c=Ctrack.objects.filter(id=id)
        return render(request,'pcode.html',{'c':c})
    else:
        return render(request,'home.html')


def slist(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        q=Quiz.objects.all()
        return render(request,'slist.html',{'q':q})
    else:
        return render(request,'home.html')

def startquiz(request,id):
    if request.user.is_authenticated and request.user.is_staff==False:
        q=Quiz.objects.filter(id=id)
        for i in q:
            name=i.name
            timer=i.quiztime
        q=Question.objects.filter(quiz=id)
        o={}
        for i in q:
            t=i.id 
            if t not in o:
                o[t]=Answer.objects.filter(question=t) 
        return render(request,'startquiz.html',{'title':name,'timer':timer,'id':id,'q':q,'o':o})
    else:
        return render(request,'home.html')

def evaluate(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        c=0
        id=request.POST['id']
        answer=request.POST.getlist('answer[]')
        q=Quiz.objects.get(id=id)
        s=QuizTaker(user=request.user,quiz=q)
        s.save()
        for i in answer:
            ans=Answer.objects.get(id=i)
            u=UsersAnswer(quiz_taker=s,question=ans.question,answer=ans)
            u.save()
            if ans.is_correct==True:
                c=c+1
        s.score=c
        s.save()
        q=Quiz.objects.all()
        return render(request,'slist.html',{'q':q})
    else:
        return render(request,'home.html')

def sresult(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        s=QuizTaker.objects.filter(user=request.user)
        return render(request,'sresult.html',{'s':s})
    else:
        return render(request,'home.html')

def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        tc=Cquestions.objects.all().count()
        tp=Pyquestions.objects.all().count()
        c=Student.objects.filter(user=request.user)
        tq=Quiz.objects.all().count()
        aq=QuizTaker.objects.filter(user=request.user).count()
        cs,ps=0,0
        for i in c:
            cs=i.cscore
            ps=i.pyscore
        return render(request,'index.html',{'tc':tc,'tq':tq,'tp':tp,'aq':aq,'ps':ps,'cs':cs})
    else:
        return render(request,'home.html')


#=============================================================================================#
#====================================staff views==============================================#
def createquiz(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'createquiz.html')
    else:
        return render(request,"home.html")

def validquiz(request):
    if request.user.is_authenticated and request.user.is_staff:
        title=request.POST['title']
        description=request.POST['description']
        timer=request.POST['timer']
        s=Quiz(user=request.user,name=title,description=description,quiztime=timer)
        s.save()
        id=s.id
        return render(request,'editquiz.html',{'title':title,'description':description,'timer':timer,'id':id})
    else:
        return render(request,"home.html")

def listquiz(request):
    if request.user.is_authenticated and request.user.is_staff:
        q=Quiz.objects.filter(user=request.user)
        return render(request,'listquiz.html',{'q':q})
    else:
        return render(request,"home.html")

def open(request,id):
    if request.user.is_authenticated and request.user.is_staff:
        s=Quiz.objects.filter(id=id)
        for i in s:
            name=i.name
            description=i.description
            timer=i.quiztime 
        q=Question.objects.filter(quiz=id)
        o={}
        for i in q:
            t=i.id 
            if t not in o:
                o[t]=Answer.objects.filter(question=t)
        print(o)
        return render(request,'editquiz.html',{'title':name,'description':description,'timer':timer,'id':id,'q':q,'o':o})
    else:
        return render(request,"home.html")

def question(request,id):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'question.html',{'id':id})
    else:
        return render(request,"home.html")

def addquestion(request):
    if request.user.is_authenticated and request.user.is_staff:
        qid=request.POST['id']
        question=request.POST['question']
        option=request.POST.getlist('option[]')
        answer=request.POST.getlist('answer[]')
        q=Quiz.objects.get(id=qid)
        s=Question(question=question,quiz=q)
        s.save()
        for i in range(len(option)):
            op=option[i]
            ans=answer[i]
            if ans=='wrong':
                ans=False
            else:
                ans=True
            o=Answer(question=s,answer=op,is_correct=ans)
            o.save()
        q=Quiz.objects.filter(id=qid)
        for i in q:
            name=i.name
            description=i.description
            timer=i.quiztime
        q=Question.objects.filter(quiz=qid)
        o={}
        for i in q:
            t=i.id 
            if t not in o:
                o[t]=Answer.objects.filter(question=t) 
        return render(request,'editquiz.html',{'title':name,'description':description,'timer':timer,'id':qid,'q':q,'o':o})
    else:
        return render(request,"home.html")

def deletequiz(request,id):
    if request.user.is_authenticated and request.user.is_staff:
        s=Quiz.objects.get(id=id)
        s.delete()
        q=Quiz.objects.all()
        return render(request,'listquiz.html',{'q':q})
    else:
        return render(request,"home.html")   


def deletequestion(request,id,qid):
    if request.user.is_authenticated and request.user.is_staff:
        s=Question.objects.get(id=id)
        s.delete()
        q=Quiz.objects.filter(id=qid)
        for i in q:
            name=i.name
            description=i.description
            timer=i.quiztime
        q=Question.objects.filter(quiz=qid)
        o={}
        for i in q:
            t=i.id 
            if t not in o:
                o[t]=Answer.objects.filter(question=t) 
        return render(request,'editquiz.html',{'title':name,'description':description,'timer':timer,'id':qid,'q':q,'o':o})
    else:
        return render(request,"home.html")     

def updatequiz(request):
    if request.user.is_authenticated and request.user.is_staff:
        id=request.POST['id']
        title=request.POST['title']
        description=request.POST['description']
        timer=request.POST['timer']
        s=Quiz.objects.get(id=id)
        s.name=title
        s.description=description
        s.quiztime=timer
        s.save()
        q=Quiz.objects.filter(id=id)
        for i in q:
            name=i.name
            description=i.description
            timer=i.quiztime
        q=Question.objects.filter(quiz=id)
        o={}
        for i in q:
            t=i.id 
            if t not in o:
                o[t]=Answer.objects.filter(question=t) 
        return render(request,'editquiz.html',{'title':name,'description':description,'timer':timer,'id':id,'q':q,'o':o})
    else:
        return render(request,"home.html") 

def editquestion(request,id,qid):
    if request.user.is_authenticated and request.user.is_staff:
        s=Question.objects.get(id=id)
        o=Answer.objects.filter(question=s)
        s=Question.objects.filter(id=id)
        return render(request,'editquestions.html',{'s':s,'o':o})


def result(request,id):
    if request.user.is_authenticated and request.user.is_staff:
        q=Quiz.objects.get(id=id)
        s=QuizTaker.objects.filter(quiz=q)
        return render(request,'result.html',{'s':s})
    else:
        return render(request,"home.html")

def sdashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'staff.html')
    else:
        return render(request,"home.html")


