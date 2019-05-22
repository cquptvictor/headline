from __init__ import mail,app,db
from flask_mail import Message
from flask import request,jsonify,session
from models import Authentication
import time
import pdb
import random
@app.route("/userRegisterSendEmail",methods=["POST"])
def Mail():
    emai=request.form.get('email')
    auth_code=random.randint(11111,99999)
    msg=Message(subject='hello',recipients=['%s'%(emai)],body="这是您的验证码:%s"%(auth_code))
    try:    
        mail.send(msg)
        session["auth_code"]=auth_code
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5) 
        db.session.commit()
        return(jsonify({'static':1}))
    except Exception as e:
        print(e)
        return(jsonify({'static':0}))
import jieba

from sklearn.cluster import KMeans as KM
from sklearn.feature_extraction.text import HashingVectorizer,TfidfVectorizer


def ttsf(ID,CONTENTS):
    length = len(ID)
    wei = []
    for content in CONTENTS:
        cut = jieba.cut(content,cut_all=False)
        words = (' '.join(cut))
        wei.append(words)
    vector = TfidfVectorizer()
    tfidf = vector.fit_transform(wei)
    d = tfidf.toarray()
    k = 3
    clf = KM(k)
    hehe = clf.fit_predict(d)
    results = []
    for i in range(length):
        if hehe[i] == hehe[0] and i!=0:
            results.append(ID[i])
        else:
            None
    print(results)
    return results
def history(times,id):
    #有五次
    #0次
    #0-5次
    if(times==[]):
        times.append(id)
    elif(len(times)==10):
        del times[0]
        times.append(id)
    elif(0<len(times)<10):
        times.append(id)
    return times