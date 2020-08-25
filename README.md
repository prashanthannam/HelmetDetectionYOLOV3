# HelmetDetectionYOLOV3

<h2>Detecting Helmet Violators in Traffic using YOLO and OCR</h2>

Project description: The system aims at detecting riders without helmet along with their number plates from traffic footage to extract Registration number. 

It tries to detect all the bikes in the image and segragates them into non-helmet bikes and helmet-bikes using the trained model. If there is no helmet, the number plate of the bike is cropped and sent to OCR where the registration number will be extracted and displayed on the screen.

For implementing this project we used YOLOv3(3rd version of You only look once which is a real-time object detection system) for the backend Machine Learning part and the UI is built using Django.

<a href="http://ec2-18-191-242-212.us-east-2.compute.amazonaws.com/detect/helmetview/">Link of the project</a>

<img src="Helmet_Detection.gif" width="900">
