import cv2
import sys
import pytesseract as ocr
import csv

def write_to_csv(frame_num, time):
    with open(output_file, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([frame_num, time])

video_path = sys.argv[1]
output_file = video_path.split('.')[0]+"_map_v1.csv"
cap = cv2.VideoCapture(video_path)
with open(output_file, 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['frame_num', 'timestamp'])

frame_num = 0
while(cap.isOpened()):
  ret, frame = cap.read()
  frame_num += 1
  frame = frame[10:75, 50:450]  
  #cv2.imshow('frame',frame)
  
  time = ocr.image_to_string(frame)
  write_to_csv(frame_num, time)
  print(time)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
