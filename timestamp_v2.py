import cv2
import sys
import pytesseract as ocr
import csv


video_path = sys.argv[1]
output_file = video_path.split('.')[0]+"_map.csv"
cap = cv2.VideoCapture(video_path)
fps = 24


with open(output_file, 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['frame_num', 'timestamp'])
    jump_frame = 0
    frame_num = 0
    first_start_pint = True
    continuous = True
    jump = False
    state = 'first'
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while(cap.isOpened()):
        #cv2.imshow('frame',frame)
        if state == 'first':
            ret, frame = cap.read()
            frame = frame[10:75, 50:450]
            time = ocr.image_to_string(frame)  
            pre_time = time
            state = 'continuous'
            print(state)
            writer.writerow([cap.get(cv2.CAP_PROP_POS_FRAMES), time])
            print([cap.get(cv2.CAP_PROP_POS_FRAMES), time])
        elif state ==  'continuous':
            ret, frame = cap.read()
            frame = frame[10:75, 50:450]
            time = ocr.image_to_string(frame)
            writer.writerow([cap.get(cv2.CAP_PROP_POS_FRAMES), time])
            if pre_time != time:
                jump_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                if(jump_frame+22 <= frame_count):
                    state = 'jump'
                    print(state)
                    print(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    pre_time = time
                else:
                    pre_time = time  
        elif state == 'jump':
            cap.set(cv2.CAP_PROP_POS_FRAMES, jump_frame+22)        
            ret, frame = cap.read()
            print(cap.get(cv2.CAP_PROP_POS_FRAMES))
            frame = frame[10:75, 50:450]
            time = ocr.image_to_string(frame)
            print(time)
            if(time != pre_time):
                cap.set(cv2.CAP_PROP_POS_FRAMES, jump_frame)
                state = 'continuous'
                print('back to jump point')
            else:
                print('Fill up...')
                for i in range(1, 24):
                    writer.writerow([jump_frame+i, pre_time])
                state = 'continuous'


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
