import cv2
from darkflow.net.build import TFNet
import numpy as np
import time,imutils,requests
import os,io,json
def sp(img,file):
    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)
    result = requests.post(url_api,
              files = {file: file_bytes},
              data = {"apikey": "392502ece188957",
                      "language": "eng",
                      "OCREngine":"2"})
    result = result.content.decode()
    result = json.loads(result)
    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    fin_t=''
    for i in text_detected:
        if i.isalnum() or i==' ':
            fin_t=fin_t+i
    return(fin_t)
def ma1(file,tfnet, tfnet1):
    colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
    colors1 = [tuple(255 * np.random.rand(3)) for _ in range(10)]

    CWD_PATH = os.getcwd()

    capture = cv2.VideoCapture(file)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    i=0
    p_no=0
    b_no=0
    f_no=0
    plate_dic=[]
    while True:
        stime = time.time()
        ret, frame = capture.read()
        
        try:
            frame = imutils.resize(frame, width=1000)
        except AttributeError:
            capture.release()
            re=[p_no,b_no,plate_dic]
            return re
        frame_fin=frame.copy()


        i=i+1
        f_no=f_no+1
        if ret and int(i%30)==0:
            cv2.imwrite('media/frame_or.png',frame)
            results = tfnet.return_predict(frame)
            print(results)
            results1 = tfnet1.return_predict(frame)
            print(results1)
            # results1=[]
            
            for result in results:
                if result['label']=='z':
                    results1.append(result)
            for color, result in zip(colors, results):
                tl = (result['topleft']['x'], result['topleft']['y'])
                br = (result['bottomright']['x']+20, result['bottomright']['y'])
                label = result['label']
                confidence = result['confidence']
                if label=='0':
                    b_no=b_no+1
                    nohel_img=frame_fin[tl[1]:br[1],tl[0]:br[0]]
                    # nohel_img=imutils.resize(nohel_img, width=100)
                    cv2.imwrite('media/bike'+str(b_no)+'.png',nohel_img)

                    cr_im=frame
                    for color1, result1 in zip(colors1, results1):
                        tl1 = (result1['topleft']['x'], result1['topleft']['y'])
                        br1 = (result1['bottomright']['x'], result1['bottomright']['y'])
                        label1 = result1['label']
                        confidence1 = result1['confidence']
                        x=tl[0]-100
                        if tl1[0]>x and tl1[0]<br[0] and tl1[1]>tl[1] and tl1[1]<br[1] and br1[0]<br[0] and br1[0]>x and br1[1]<br[1] and br1[1]>tl[1]:
                            p_no=p_no+1
                            print("plate"+" "+str(confidence)+" "+str(tl1[0])+" "+str(tl1[1])+" "+str(br1[0])+" "+str(br1[1])+" "+str(tl[0])+" "+str(tl[1])+" "+str(br[0])+" "+str(br[1]))
                            plate_img=frame_fin[tl1[1]-30:br1[1]+20,tl1[0]-20:br1[0]+20]
                            plate_img = imutils.resize(plate_img, width=500)
                            # plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

                            cv2.imwrite('media/plate'+str(p_no)+'.png',plate_img)
                            # tess(plate_img)
                            plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)
                            # plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV)

                            plate_text=sp(plate_img,'C:/detection_helmet/djano-project/Helmet/media/frame_or.png')
                            plate_dic.append(plate_text)
                            cv2.waitKey(0)
                            text1='{}: {:.0f}%'.format(label1,confidence1*100)
                            frame=cv2.rectangle(frame,tl1,br1,color1,5)
                            frame=cv2.putText(frame,text1,tl1,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
                            break
                # if label!='z':
                text = '{}: {:.0f}%'.format(label, confidence * 100)
                frame = cv2.rectangle(frame, tl, br, color, 5)
                frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            frame=imutils.resize(frame,width=350)   
            cv2.imwrite('media/frame.png', frame)
    capture.release()
    re=[p_no,b_no,plate_dic]
    return re
