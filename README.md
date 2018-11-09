# Face Recognition 

A docker image that provides the ability to find faces on images. It uses the face_detection_cli.py written by Adam Geitgey (https://github.com/ageitgey/face_recognition)

## How to build/start?
```

git clone https://github.com/danzarov/face_recog.git

cd face_recog

docker build -t face_recog .

docker run -d --name face_recogn_container -p 8080:8080 face_recog

```

## How to use?
```
curl -X POST -F "file=@my_image.jpg" http://<ip-addr>:8080/
```

* It will return a boolean (True) when a face has been found and (False) when not found.
