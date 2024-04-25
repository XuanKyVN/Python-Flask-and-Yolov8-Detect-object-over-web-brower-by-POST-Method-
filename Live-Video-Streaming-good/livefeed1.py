from flask import Flask, render_template, Response,request
import cv2 as cv
from time import sleep
from ultralytics import YOLO
import imutils
#cap = cv.VideoCapture(1)
cap =cv.VideoCapture(r"C:\Users\Admin\PythonLession\pic\Traffic1.mp4")

fourcc = cv.VideoWriter_fourcc(*'vp80')
video=cv.VideoWriter('static/myvideo.webm',fourcc ,6,(800,600))
currentframe=0
app = Flask(__name__, static_folder='static')
flag = True
@app.route('/')
def index():
    	return render_template('index.html')

def gen(flag):
	#print(cap.read())
	while(cap.isOpened()):
		ret, img = cap.read()
		if ret == True:
			model = YOLO(r"C:\Users\Admin\PythonLession\yolo_dataset\yolov8n.pt")
			result = model.predict(img, device =[0])
			img = result[0].plot()

			name = str(currentframe)+ '.png'
			img = imutils.resize(img,width =1000)
			#print(img.shape)
			cv.imwrite(name, img)
			k=(cv.imread(str(currentframe)+'.png'))
			video.write(k)
			frame = cv.imencode('.png', img)[1].tobytes()
			yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
			sleep(0)
		else: 
			break
@app.route('/',methods=['POST'])
def getval():
	k=request.form['psw1']
	if k=='4':
		cap.open(r"C:\Users\Admin\PythonLession\pic\Traffic4.mp4")
		return render_template("index.html")

	if k=='3':
		cap.open(r"C:\Users\Admin\PythonLession\pic\Traffic1.mp4")
		return render_template("index.html")
	if k=='2':
		cap.open(1)
		return render_template("index.html")
	if k=='1':
		cap.release()
		return render_template("index.html")
	if k=='0':
		return render_template("saved.html")
@app.route('/video_feed')
def video_feed():
	return Response(gen(flag), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
