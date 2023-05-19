from flask import Flask, render_template, request, jsonify
import requests
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.3u10amg.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)   #db의 주소   
db = client.dbsparta   # db연결

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sub/<username>')  # Path Variable 로 원하는 정보 보내기  나중에 mbti로도 검사 
def sub(username):     #받기   Path Variable 데이터가 들어감  <username><mbti>

   
    print(username)
    mbti = username[-4:]  ## mbti만 분류하기
    print(mbti)
    name = username.replace(mbti,"") ## mbti를 공백으로 만들고 이름만 분류하기
    print(name)
    data_receive = db.firstproject.find_one({'name':name , 'mbti':mbti},{'_id':False})  ## 데이터 가져오기 성공
    print(data_receive)
    print(data_receive["name"]) ##확인용 print
    print(data_receive["mbti"])
    print(data_receive["image"])
    print(data_receive["image2"])

    name = data_receive["name"]
    comment = data_receive["comment"]
    pandc = data_receive["pandc"]
    pandc2 = data_receive["pandc2"]
    mbti = data_receive["mbti"]
    Deter = data_receive["Deter"]
    image = data_receive["image"]
    image2 = data_receive["image2"]

    print(image)
    print(image2)

    return render_template('sub.html', name=name , comment=comment , pandc=pandc , pandc2=pandc2 , mbti=mbti , Deter=Deter , image="."+image , image2="."+image2) #html 실행하기  , 값 전달해주기 


@app.route("/first_project", methods=["POST"])   #post 경로를 같게 해야함 create 추가
def teamadd():  ## POST 
    #index.html에서 데이터 전달받기 
    name_receive = request.form['name_give']     
    comment_receive = request.form['comment_give']
    pandc_receive = request.form['pandc_give']
    pandc2_receive = request.form['pandc2_give']
    mbti_receive = request.form['mbti_give']
    Deter_receive = request.form['Deter_give']   
    image_receive = request.form['image_give']    #이미지 
    image2_receive = request.form['image2_give'] 
    imageall_receice = request.files["imageall_give"]   # 이미지파일 데이터를 가져오기
    imageall2_receice = request.files["imageall2_give"] 
    # save_to = static/????   # 저장할 폴더의 파일
    # imageall_receice.save(save_to)  저장하기
    # image2_receive = request.form['image_give']
    # image3_receive = request.form['image_give']
    print(imageall_receice)
    print(image_receive)
    print(imageall2_receice)
    print(image2_receive)

    imageall_receice.save('./static/'+image_receive)
    imageall2_receice.save('./static/'+image2_receive)

    # image_receive
      
    doc = {'name':name_receive,'comment':comment_receive,'pandc':pandc_receive,'pandc2':pandc2_receive,'mbti':mbti_receive,'Deter':Deter_receive , 'Deter':Deter_receive , 'image':'./static/'+image_receive, 'image2':'./static/'+image2_receive}
    db.firstproject.insert_one(doc)

    return jsonify({'msg':'POST 연결 완료! 겸 기록완료'})

@app.route("/firstproject1", methods=["POST"]) #댓글남기기
def add(): 
    name1_receive = request.form['name1_give']
    comment1_receive = request.form['comment1_give']

    doc = {'name1':name1_receive,
           'comment1':comment1_receive
        }
    db.fan.insert_one(doc)

    return jsonify({'msg':'POST 연결 완료! 겸 기록완료'})

@app.route("/sub", methods=["POST"])  #update 변경 
def teamchange():
    #sub.html에서 데이터 전달받기 findname
    findname_receive = request.form['findname_give'] 
    findmbti_receive = request.form['findmbti_give'] 
    changename_receive = request.form['changename_give']     
    changecomment_receive = request.form['changecomment_give']
    changepandc_receive = request.form['changepandc_give']
    changepandc2_receive = request.form['changepandc2_give']
    changembti_receive = request.form['changembti_give']
    changeDeter_receive = request.form['changeDeter_give']   
    changechooseFile_receive = request.form['changechooseFile']
    changechooseFileall_receice = request.files["changechooseFileall_give"]   # 이미지파일 데이터를 가져오기
    changechooseFile2_receive = request.form['changechooseFile2']
    changechooseFileall2_receice = request.files["changechooseFileall2_give"]   # 이미지파일 데이터를 가져오기
    print("aaaaaaa")
    print(findname_receive)
    print(changename_receive)
    print(changechooseFile_receive)
    print(changechooseFileall_receice)

    changechooseFileall_receice.save('./static/'+changechooseFile_receive)
    changechooseFileall2_receice.save('./static/'+changechooseFile2_receive)
    #수정할 데이터를 딕셔너리 형태로 저장
    doc = {'name':changename_receive,'comment':changecomment_receive,'pandc':changepandc_receive,'pandc2':changepandc2_receive,'mbti':changembti_receive,'Deter':changeDeter_receive , 'image':'./static/'+changechooseFile_receive , 'image2':'./static/'+changechooseFile2_receive}  
    db.firstproject.update_one({'name':findname_receive , 'mbti':findmbti_receive},{'$set':doc})
    return jsonify({'msg':'POST 연결 완료! 겸 기록완료'})

@app.route("/firstproject", methods=["GET"])
def firstproject_get():
    print("진입")
    firstproject_data = list(db.firstproject.find({},{'_id':False}))
    return jsonify({'result': firstproject_data})

@app.route("/firstproject1", methods=["GET"]) #댓글조회
def select():
    print("진입")
    all_comment = list(db.fan.find({},{'_id':False}))
    return jsonify({'result': all_comment})




if __name__ == '__main__':  # 서버실행
    app.run('0.0.0.0', port=5000, debug=True)


    