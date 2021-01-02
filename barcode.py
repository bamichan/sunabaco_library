from pyzbar import pyzbar
import cv2
import numpy as np

camera_port = 0
cap_cam = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)
cv2.namedWindow('frame')
# カメラが接続できない場合は、exit
if not cap_cam.isOpened():
    print("カメラを開けません")
    exit()

while True:
    # フレームごとにキャプチャ
    ret, frame = cap_cam.read()
    #フレームが正しく読み取られた場合、retはTrue
    if not ret:
        print("フレームは受信できません。終了しています...")
        break

    # グレースケール化してコントラストを調整する
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = edit_contrast(gray_scale, 5)

    # 結果のフレーム表示
    cv2.imshow('frame',gray_scale)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

    # 加工した画像からフレームQRコードを取得してデコードする
    codes = decode(image)
    if len(codes) > 0:
        output = codes[0][0].decode('utf-8', 'ignore')
        print(output)
        # CSVファイルに書き込み
        # output_csv = output
        with open('qr.csv', 'w') as csv_file:
            writer = csv.writer(csv_file,
                                lineterminator='\n')  # 改行コード（\n）を指定しておく
            writer.writerow([output])
        if 'output' != None:
            cap_cam.read()
            # cap_cam.release()

    # すべて完了したらキャプチャーを解放する
    cap_cam.release()
    cv2.destroyAllWindows()