from __init__ import app,login_manager
from flask import request,jsonify,make_response,session
from models import User,db,Article,Zan,Comment,Ucollection,Collection,Authentication,User_headline,Collection,Follow,Fans,Reply
from flask import render_template
from flask_login import login_user,logout_user,login_required,current_user
import pdb
import os
import ast
from config import ALLOWED_EXTENSIONS,UPLOAD_PATH
import time
from mail import ttsf,history
@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user
@app.route("/")
def index():
    return(render_template("index.html"))
# @app.route('/userRegisterTest',methods=["GET","POST"])
# def register():
#     if(request.method=="POST"):
#         username=request.form.get("username")
#         email=request.form.get("email")
#         password=request.form.get("passwd")
#         auth_code=request.form.get("auth_code")
#         data=Authentication.query.filter_by(email=email).order_by(Authentication.id.desc()).first()
#         #pdb.set_trace()
#         if(abs(data.time-time.time())<3000):
#             if(str(data.auth_code) == auth_code):
#                 i=User(username = username,password=password,email=email)
#                 db.session.add(i)
#                 db.session.commit()
#                 return(jsonify({'static':1}))
#             else:
#                 return(jsonify({"static":-1}))#验证码不对
#         else:
#             return(jsonify({'static':0}))#验证码失效
#     else:
#         response.make_response()
#         response=render_template("login.html")
#         reponse.headers['content-encoding']='gzip'
#         return response
        #return(render_template('login.html'))
@app.route('/userRegisterTest',methods=["GET","POST"])
def register():
    if(request.method=="POST"):
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("passwd")
        auth_code=request.form.get("auth_code")
        if(session['auth_code'] != None):    
            if(session['auth_code'] == int(auth_code)):
                i=User(username = username,password=password,email=email)
                db.session.add(i)
                db.session.commit()
                return(jsonify({'static':1}))
            else:
                return(jsonify({"static":-1}))#验证码不对
        else:
            return(jsonify({'static':0}))#验证码失效
    else:
        response.make_response()
        response=render_template("login.html")
        reponse.headers['content-encoding']='gzip'
        return response
        #return(ren
@app.route('/userSignIn',methods=["POST","GET"])
def login():
    if(request.method=="POST"):
        email=request.form.get("email")
        password=request.form.get("passwd")
        if(User.query.filter_by(email=email)):
           # pdb.set_trace()
            user=User.query.filter_by(email=email,password=password).first()
            if(user):
                login_user(user)
                return(jsonify({
                'static':1,
                'imgUrl':user.pic,
                'follow':user.follow_num,
                'fans':user.fans_num,
                'uid':user.id,
                'name':user.username
                }))
            else:
                return(jsonify({"static":0}))
        else:
            return(jsonify({'static':-1}))
        
    else:
        return(render_template("login.html"))
@app.route("/isLogin")
def isLogin():
    
    if(current_user.is_anonymous):
        return(jsonify({"static":0}))
    else:
        return(jsonify({"static":1,"uid":current_user.get_id()}))
@app.route("/userLogout")
@login_required
def logout():
    if(logout_user()):
        return(jsonify({'static':1}))
    else:
        return(jsonify({'static':0}))

@app.route("/userFollow",methods=["POST","GET"])
@login_required
def userFollow():
    uid=int(request.form.get('uid'))
    follow_id=int(request.form.get('follow_id'))   
    following=User.query.filter_by(id=uid).first()#粉丝
    followed=User.query.get(follow_id)#明星
    following.follow_num=following.follow_num+1#粉丝数和关注数个加一，插入fans和follow
    followed.fans_num=followed.fans_num+1
    follow=Follow(uid=uid,followed_id=follow_id)
    fans=Fans(uid=follow_id,fans_id=uid)       
    try:
        db.session.add_all([fans,follow]) 
        db.session.commit()
        return(jsonify({'static':1}))
    except Exception as e:
        print(e)
        return(jsonify({'statir':0}))
@app.route("/userRemoveFollow",methods=["POST"])
@login_required
def RemoveFollow():   
    uid=request.form.get("uid")
    follow_id=request.form.get("follow_id")
    #关注和粉丝数各-1，关注表删掉和粉丝表中删掉对应的记录            
    following=User.query.get(uid)#我
    followed=User.query.get(follow_id)#明星
    following.follow_num=following.follow_num-1
    followed.fans_num=followed.fans_num-1
    try:    
        Follow.query.filter_by(followed_id=follow_id,uid=uid).delete()
        Fans.query.filter_by(uid=follow_id,fans_id=uid).delete()
        db.session.commit()
        return(jsonify({"static":1}))
    except Exception as e:
        print(e)
        return(jsonify({'static':0}))
@app.route('/getFollows',methods=["POST"])
@login_required
def getFollows():
    uid=request.form.get("uid")
    page=request.form.get("page")
    follow=Follow.query.filter_by(uid=uid).offset(int(page)*30-30).limit(10).all()
    if(follow==None):
        return(jsonify({"static":0}))
    else:
        data=[]
        for each in follow:
            user=User.query.get(each.followed_id)    
            data.append(
            {
            'name':user.username,
            'imgUrl':user.pic,
            'uid':user.id
		}
                    )
        return(jsonify({'data':data}))
@app.route("/isFollow",methods=["POST"])
def isFollow():
    uid=request.form.get("uid")
    follow_id=request.form.get("follow_id")
    follow=Follow.query.filter_by(followed_id=follow_id,uid=uid).first()
    if(follow is None):
        return(jsonify({"follow":"false"}))
    else:
        return(jsonify({"follow":"true"}))
@app.route("/isZan",methods=["POST"])
def isZan():
    uid=request.form.get("uid")
    article_id=request.form.get("id")
    type=request.form.get("type")
    zan=Zan.query.filter_by(uid=uid,article_id=article_id,type=type).first()
    if(zan==None):
        return(jsonify({"zan":"false"}))
    else:
        return(jsonify({"zan":"true"}))

@app.route('/getfans',methods=["POST"])
@login_required
def getfans():
    uid=request.form.get("uid")
    page=request.form.get("page")
    fans=Fans.query.filter_by(uid=int(uid)).offset(int(page)*30-30).limit(30).all()
    print(fans)
    if(fans!=None):
        data=[]
        for each in fans:
            user=User.query.get(each.fans_id)    
            data.append(
            {
                'name':user.username,
                'imgUrl':user.pic,
                 'uid':user.id                     }
            )
        return(jsonify({'data':data}))
    return(jsonify({"static":0}))
#发布微头条
@app.route('/userPublishArticle',methods=["POST"])
@login_required
def userPublishArticle():
    uid=request.form.get("uid")
    content=request.form.get("content")
    files=request.files.getlist('pic')
    pic="#"
    for file in files:    
        if file and allowed_file(file.filename):
            user=User.query.get(uid)
            filename=str(uid)+"_Wei_"+str(time.time())+"."+file.filename.rsplit('.',1)[1]
            pic=pic+filename+"#"
            file.save(os.path.join(UPLOAD_PATH,filename))
            #os.path.join将多个路径组合后返回
    try:    
        publish=User_headline(uid=uid,content=content,pic=pic)
        db.session.add(publish)
        db.session.commit()
        return(jsonify({"static":1}))
    except Exception as e:
        print(e)
        return(jsonify({"static":0}))
#获得用户发布的微头条列表
@app.route("/getPublishList",methods=["POST"])
def getPulishList():
    uid=request.form.get("uid")
    page=request.form.get("page")
    data=[]
    user_headline=User_headline.query.filter_by(uid=uid).offset(int(page)*20-20).limit(20).all()
    if(user_headline==None):
         return(jsonify({"static":0}))
    else:
        for each in user_headline:
            picture=[]
            #pdb.set_trace()
            if(len(each.pic) != 0):
                pics=each.pic.strip('#').split('#')
                pic="./static/img/%s"%(pics[0])
            else:
                    pic=[]
            data.append(
            {
                    'id':each.id,
                    'content':each.content,
                    'readNum':each.read_num,
                    'zanNum':each.like_num,
                    'time':each.time,
                    'imgUrl':pic
                         }
                                )
        return(jsonify(data))
#获得用户的评论列表
@app.route("/getCommentList",methods=["POST"])
@login_required
def getCommentList():
    uid=request.form.get("uid")
    page=request.form.get("page")
    data=[]
    comment=Comment.query.filter_by(uid=uid).order_by(Comment.uid.desc()).offset(int(page)*20-20).limit(20).all()
    if(comment==None):    
        return(jsonify({"static":0}))
    else:
        for each in comment:
       #     pdb.set_trace()
            article=Article.query.filter_by(id=each.article_id).first()     
            data.append(
            {
            'id':article.id,
            "cid":each.id,
            "title":article.title,
            "readNum":each.read_num,
            "zanNum":each.like_num,
            "contentUrl":article.pic,
            "time":each.time,
            "content":each.content
                         }
                         )
            each.read_num+=1
        db.session.commit()
        return(jsonify(data))

#删除用户发布的评论和微头条
@app.route("/deletePulished",methods=["POST"])
@login_required
def deletePulished():
    type=request.form.get("type")
    id=int(request.form.get("id"))
    uid=int(request.form.get("uid"))
    if(type=='0'):
        try:
            User_headline.query.filter_by(uid=uid,id=id).delete()
            pdb.set_trace()
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
    else:

        try:
            Comment.query.filter_by(id=id).delete()
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
#
@app.route("/slideArticle")
def slideArticle():
    article1=Article.query.filter_by(category="国际").order_by((Article.time).desc()).first()
    article2=Article.query.filter_by(category="其他").order_by((Article.time).desc()).first()
    article3=Article.query.filter_by(category="娱乐").order_by((Article.time).desc()).first()
    article4=Article.query.filter_by(category="体育").order_by((Article.time).desc()).first()
    article5=Article.query.filter_by(category="军事").order_by((Article.time).desc()).first()
    article6=Article.query.filter_by(category="科技").order_by((Article.time).desc()).first()
    data=[]
  #  pdb.set_trace()
    for each in [article1,article2,article3,article4,article5,article6]:
        data.append(
            {
              'title':each.title,
              'imgUrl':each.pic,
              'id':each.id,
              'type':each.category
          }
          )
    return(jsonify(data))


#获得文章列表
@app.route("/getArticle",methods=["POST"])
def getArticle():
   # pdb.set_trace()
    page=request.form.get("page")
    category=request.form.get("type")
    if(category=="热点"):
        article=Article.query.order_by(Article.comment_num).offset(int(page)*20-20).limit(20).all()
        data=[]
        for each in article:
            data.append(
            {
              'id':each.id, 
              'title':each.title,
              'author':each.author,
              'commentNum':each.comment_num,
              'time':each.time,
              'imgUrl':each.pic,
           #   'readNum':each.read_num
          }
            )
        return(jsonify(data))
    data=[] 
    article=Article.query.filter_by(category=category).order_by((Article.time).desc()).offset(int(page)*20-20).limit(20).all()
    if(article==None):
        return(jsonify({"static":0}))
    else:
        for each in article:
            data.append(
            {
              'id':each.id, 
              'title':each.title,
              'author':each.author,
              'commentNum':each.comment_num,
              'time':each.time,
              'imgUrl':each.pic
          }
            )
    return(jsonify(data))
@app.route("/getReommendArticle",methods=["POST"])
def getReommendArticle():
  #  pdb.set_trace()
    past=request.cookies.get("past")
    page=int(request.form.get("page"))
    
    if(past==None or len(ast.literal_eval(past))<3):
        article=Article.query.order_by(Article.time.desc()).offset(int(page)*20-20).limit(20).all()
        data=[]
        for each in article:
            data.append(
            {
                "title":each.title,
                "imgUrl":each.pic,
                "id":each.id,
                "author":each.author,
                "commentNum":each.comment_num,
                "time":each.time,
                "type":each.category

            }
        )
        return(jsonify(data))
    else:
        ID=[]
        past=ast.literal_eval(past)
        Content=[]
        for each in past:
            article=Article.query.get(each)
            ID.append(each)
            Content.append(article.content)
        #pdb.set_trace()
        results=ttsf(ID,Content)
        if(results==[]):
            article=Article.query.order_by(Article.time.desc()).offset(int(page)*20-20).limit(20).all()
            data=[]
            for each in article:
                data.append(
            {
                "title":each.title,
                "imgUrl":each.pic,
                "id":each.id,
                "author":each.author,
                "commentNum":each.comment_num,
                "time":each.time,
                "type":each.category

            }
        )
            return(jsonify(data))
        else:
            print(results)
            article=Article.query.filter(Article.id.in_(results)).all()
            category=[]
            print(article)
            for each1 in article:
                category.append(each1.category)
            category=list(set(category))
            print(category)
            articles=Article.query.filter(Article.category.in_(category)).offset((page-1)*20).limit(20).all()
            data=[]
            for each in articles:
                data.append(
            {
                "title":each.title,
                "imgUrl":each.pic,
                "id":each.id,
                "author":each.author,
                "commentNum":each.comment_num,
                "time":each.time,
                "type":each.category
            }
        )
            return(jsonify(data))
#24小时热新闻
@app.route("/hotArticle")
def hotArticle():
    article=Article.query.order_by(Article.comment_num).limit(4).all()
    data=[]
    for each in article:
        data.append(
            {
                "title":each.title,
                "imgUrl":each.pic,
                "id":each.id,
                "author":each.author,
                "commentNum":each.comment_num,
                "time":each.time
            }
        )
    return(jsonify(data))
#每一篇文章下的评论
@app.route("/getComments",methods=["POST"])
def getComments():
    id=int(request.form.get("id"))
   #db.set_trace()
    page=int(request.form.get("page"))
    comment=Comment.query.filter_by(article_id=id).order_by(Comment.like_num.desc()).offset((int(page)-1)*5).limit(5).all()
    data=[]
    if(comment==None):
        return(jsonify({"static":0})) 
    else:
        for each in comment:
            num=Reply.query.filter_by(cid=each.id).count() 
            user=User.query.get(each.uid)
            data.append(
            {
                "uid":user.id,
                "username":user.username,
                "imgUrl":user.pic,
                "content":each.content,
                "time":each.time,
                "zan":each.like_num,
                "cid":each.id,
                "replyNum":num          
  }
        )
            each.read_num+=1
        db.session.commit()
        return(jsonify(data))

#收藏
@app.route("/startArticle",methods=["POST"])
@login_required
#文章id和用户id为判断依据
def startArticle():
    uid=request.form.get("uid")#用户id
    id=request.form.get("id")#文章id
    type=request.form.get("type")
    if(type=='0'):
        collection=Collection(article_id=id,uid=uid)
    else:
        collection=Ucollection(article_id=id,uid=uid)
    try:
        db.session.add(collection)
        db.session.commit()
        return(jsonify({'static':1}))
    except Exception as e:
        print(e)
        return(jsonify({'static':0}))
#取消收藏
@app.route("/removeStartArticle",methods=["POST"])
@login_required
def removeStartArticle():
    uid=request.form.get("uid")
    id=request.form.get("id")
    type=request.form.get("type")
    if(type=='0'):
        Collection.query.filter_by(article_id=id,uid=uid).delete()
    else:
        Ucollection.query.filter_by(article_id=id,uid=uid).delete()
    try:
        db.session.commit()
        return(jsonify({'static':1}))
    except Exception as e:
        print(e)
        return(jsonify({'static':0}))
@app.route("/getStartList",methods=["POST"])
@login_required
def getStartList():
    uid=request.form.get("uid")
    page=request.form.get("page")
   # pdb.set_trace()
    collection=Collection.query.filter_by(uid=uid).order_by(Collection.time.desc()).offset((int(page)-1)*10).limit(10).all()
    ucollection=Ucollection.query.filter_by(uid=uid).order_by(Collection.time.desc()).offset((int(page)-1)*10).limit(10).all()
    if(Collection==None):
        return(jsonify({"static":0}))
    else:
        data=[]
        for each in collection:
            article=Article.query.get(each.article_id)
            data.append(
            {   "type":0,
                "id":each.article_id,
                "title":article.title,
                "time":each.time,
               # "readNum":article.read_num,
                "commentNum":article.comment_num
            })
        for each2 in ucollection:
            user_headline=User_headline.query.get(each2.article_id)
            data.append(
            {   "type":1,
                "id":each2.article_id,
                "content":user_headline.content,
                "time":each2.time,
                "commentNum":user_headline.comment_num
            }
        )
        return(jsonify(data))
@app.route("/reportArticle",methods=["POST"])
@login_required
def reportArticle():
    return(jsonify({'static':1}))
#发表评论
@app.route("/publishComment",methods=["POST"])
@login_required
def publishComment():
    id=int(request.form.get("id"))
    uid=int(request.form.get("uid"))
    comment=request.form.get("content")
    comment=Comment(uid=uid,article_id=id,content=comment)
    article=Article.query.get(id)
    article.comment_num+=1
    try:
        db.session.add(comment)
        db.session.commit()
        return(jsonify({"static":1}))
    except Exception as e:
        print(e)
        return(jsonify({"static":0}))
#回复评论
@app.route("/replyComment",methods=["POST"])
@login_required
def replyComment():
    from_id=int(request.form.get("from_id"))#form
    to_id=int(request.form.get("to_id"))#to
    to_name=request.form.get("to_name")
    cid=int(request.form.get("cid"))
    content=request.form.get("content")
    type=request.form.get("type")
    if(type=='0'):
        rid=cid
    else:
        rid=request.form.get("rid")
    reply=Reply(from_id=from_id,cid=cid,content=content,to_id=to_id,to_name=to_name,reply_id=rid,type=type)
    try:
        db.session.add(reply)
        db.session.commit()
        return(jsonify({"static":1}))
    except Exception as e:
        print(e)
        return(jsonify({"static":0}))
#获得评论的回复
@app.route("/replyDetail",methods=["POST"])
@login_required
def replyDetail():
    #id=request.form.get("uid")
    cid=request.form.get("cid")#评论的id
    page=request.form.get("page")
    #获得回复
    reply=Reply.query.filter_by(cid=cid).order_by(Reply.time).offset(int(page)*5-5).limit(5).all()
    if(reply==None):
        return(jsonify({"static":0}))
    else:
        data=[]
        for each in reply:
            if(each.type==1):
                print(each.reply_id)
                rep=Reply.query.filter_by(id=each.reply_id).first()
                user=User.query.filter_by(id=each.from_id).first()
                data.append({
            "to_id":each.to_id,
            "to_name":each.to_name,
            "imgUrl":user.pic,
            "content":each.content,
            "time":each.time,
            "zan":each.like_num,
            "from_name":user.username,
            "from_id":user.id,
            "rid":each.id,
            "rcontent":rep.content[0:10]
        })
            else:
                user=User.query.filter_by(id=each.from_id).first()
                data.append({
            "to_id":each.to_id,
            "to_name":each.to_name,
            "imgUrl":user.pic,
            "content":each.content,
            "time":each.time,
            "zan":each.like_num,
            "from_name":user.username,
            "from_id":user.id,
            "rid":each.id
                    })

        return(jsonify(data))

  
#评论和回复点赞
@app.route("/dianZanComment",methods=["POST"])
@login_required
def dianZanComment():
    id=int(request.form.get('id'))
    uid=int(request.form.get('uid'))
    type=request.form.get("type")
    zan=Zan(article_id=id,uid=uid,type=type)
    db.session.add(zan)
    if(type=='0'):#指评论
        comment=Comment.query.get(id)
        comment.like_num+=1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
    elif(type=='-1'):#指回复
        #pdb.set_trace()
        reply=Reply.query.get(id)
        reply.like_num+=1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
    else:#微头条
        user_headline=User_headline.query.get(id)
        user_headline.like_num+=1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
@app.route("/removeZanComment",methods=["POST"])
def removeZanComment():
    id=request.form.get('id')
    uid=request.form.get('uid')
    type=request.form.get("type")
    Zan.query.filter_by(article_id=id,uid=uid).delete()
    db.session.commit()
    if(type=='0'):#指评论
        comment=Comment.query.get(id)
        comment.like_num=comment.like_num-1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
    elif(type=='-1'):#指回复
        reply=Reply.query.get(id)
        reply.like_num-=1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))
    else:#微头条
        user_headline=User_headline.query.get(id)
        user_headline.like_num-=1
        try:
            db.session.commit()
            return(jsonify({"static":1}))
        except Exception as e:
            print(e)
            return(jsonify({"static":0}))     
#用户自定义头像上传
@app.route("/customeAvatar",methods=["POST"])
@login_required
def customeAvatar():
    file=request.files["pic"]
    uid=request.form.get("uid")
    if file and allowed_file(file.filename):
            user=User.query.get(uid)
            filename=str(user.id)+"_Avatar"+"."+file.filename.rsplit('.',1)[1]
            file.save(os.path.join(UPLOAD_PATH,filename))
            #os.path.join将多个路径组合后返回
            user=User.query.get(uid)
            user.pic=os.path.join(UPLOAD_PATH,filename)
            db.session.commit()
            return(jsonify({"static":1}))
    else:
        return(jsonify({"static":0}))
def allowed_file(filename):
    #验证文件的合法性
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


# #详细页面
# @app.route("/articleDetail",methods=["POST"])
# def articleDetail():
#     id=request.form.get("id")
#     article=Article.query.get(id)
#     if(current_user.is_anonymous):
#         isStart=0
#     else:
#         collection=Collection.query.filter_by(article_id=id,uid=current_user.get_id()).first()
#         if(collection is None):
#             isStart=0
#         else:
#             isStart=1
#     data=[
#         {
#             "content":article.content,
#             "isStart":isStart,
#             "time":article.time,
#             "author":article.author,
#             "title":article.title,
#             "type":article.category,
#             "commentNum":article.comment_num,
#             "id":id          
#         }
#             ]
#     article.read_Num=+1
#     db.session.commit()
#     return(jsonify(data))
#详细页面
@app.route("/articleDetail",methods=["POST"])
def articleDetail():
    id=request.form.get("id")
    article=Article.query.get(id)
    if(current_user.is_anonymous):
        isStart=0
    else:
        collection=Collection.query.filter_by(article_id=id,uid=current_user.get_id()).first()
        if(collection is None):
            isStart=0
        else:
            isStart=1
    data=[
        {
            "content":article.content,
            "isStart":isStart,
            "time":article.time,
            "author":article.author,
            "title":article.title,
            "type":article.category,
            "commentNum":article.comment_num,
            "id":id   
        }
            ]
    article.read_Num=+1
    db.session.commit()
    response=make_response(jsonify(data))
    #pdb.set_trace()
    past=request.cookies.get("past")
    if(past==None):
        past=[]
    else:
        past=ast.literal_eval(past)
    print(past)
    times=history(past,id)
    response.set_cookie("past",str(times),max_age=10000,domain="0.0.0.0")
    return(response)
@app.route("/weiDetail",methods=["POST"])
def weiDetail():
    
    id=request.form.get("id")
    user_headline=User_headline.query.get(id)
    #pdb.set_trace()
    user=User.query.get(user_headline.uid)
    if(current_user.is_anonymous):
        isStart=0
    else:
        collection=Ucollection.query.filter_by(article_id=id,uid=current_user.get_id()).first()
        if(collection==None):
            isStart=0
        else:
            isStart=1
    picture=[]
    if(len(user_headline.pic) != 0):
        pics=user_headline.pic.strip('#').split('#')
    #pdb.set_trace()
        for pic in pics:
            picture.append("./static/img/%s"%(pic))  
    print(picture)
    data=[
        {
            "id":id,
            "type":"微头条",
            "uid":user.id,
            "content":user_headline.content+"<br/><br/>",
            "isStart":isStart,
            "author":user.username,
            'pic':picture,
            "time":user_headline.time,
        }
    ]
    user_headline.read_Num=+1
    db.session.commit()
    return(jsonify(data))  

@app.route("/searchUserData")
def searchUserData():
    keyWord=request.args.get("keyWord")
    page=request.args.get("page")
    user=User.query.filter(User.username.like("%"+keyWord+"%")).order_by(User.fans_num).offset(int(page)*30-30).limit(30).all()
    if(user==None):
        return(jsonify({"static":0})) 
    else:
        data=[]
        for each in user:
            data.append(
            {
                "username":each.username,
                "uid":each.id,
                "imgUrl":each.pic

        }
            )
        return(jsonify(data))
@app.route("/searchComprehensiveData")
def searchComprehensiveData():
    keyWord=request.args.get("keyWord")
    page=request.args.get("page")
    article=Article.query.filter(Article.title.like("%"+keyWord+"%")).order_by(Article.time.desc()).offset(int(page)*20-20).limit(20).all()
    if(article==None):
        return(jsonify({"static":0})) 
    else:
        data=[]
        for each in article:
            num=Comment.query.filter_by(article_id=each.id).count()
            data.append(
            {
            "id":each.id,
            "title":each.title,
            "author":each.author,
            "commentNum":num,
            "time":each.time,
            "contentUrl":each.pic
        }
          )
        return(jsonify(data))
@app.route("/getUserInfo",methods=["POST"])
def getUserInfo():
    uid=request.form.get("uid")
    user=User.query.get(uid)
    return(
        jsonify(
            {
                "username":user.username,
                "imgUrl":user.pic,
                "follow":user.follow_num,
                "fans":user.fans_num
            }
        )
    )
@app.route("/changeUsername",methods=["POST"])
def changeUsername():
    uid=request.form.get("uid")
    rename=request.form.get("rename")
    user=User.query.get(uid)
    user.username=rename
    try:
        db.session.commit()
        return(jsonify({"static":1}))
    except Exception as e:
        print(e)
        return(jsonify({"static":0}))
