# 샴네트워크를 활용한 음성 키워드 회원가입/로그인 기능

## 기능

### 1. 녹음

static/js/login.js, static/js/register.js

자바스크립트의 MediaRecorder 기능을 사용하여 녹음을 진행.

녹음이 완료되면 FormData에 blob형태로 저장하여 파일을 전송함.

### 2. 변환

src/convert.py

위 녹음을 통해 들어온 wav 파일의 소리를 이미지로 변환해준다.

2D 음파 그래프, 푸리에, 2D+푸리에, MFCC, Mel-Spectrogram으로 총 4가지 변환 방법이 있음

그 중 Mel-Spectrogram이 가장 좋은 성능을 나타내어 Mel-Spectrogram 변환을 사용

(다른 변환 방법을 사용해보고 싶다면 convert.py에 run 함수 부분을 수정하면 됨)

++ 전체 녹음 파일을 저장하면 소리가 없는 부분도 저장 되기 때문에, 소리가 임계치를 넘지 않는 부분은 find_idx 함수를 사용하여 제외

### 3. 학습

src/siamese.py, src/siameseDataset.py, src/train.py

회원가입이 발생하면 작동하는 기능.

변환을 통해 sounds 폴더에 저장된 데이터로 학습을 진행함.

폴더명이 해당 라벨의 이름이고, 각각 폴더 내부엔 해당 키워드의 mel-spectogram 이미지 3장씩 들어있다.

학습이 완료되면 model폴더에 학습 모델이 저장됨

### 4. 추론

src/siamese.py, src/siameseDataset.py, src/inference.py

로그인이 발생하면 작동하는 기능.

변환을 통한 이미지를 login폴더에 임시 저장함.

model폴더에 저장된 학습 모델을 이용하여 login 시 이미지와 sounds에 저장된 데이터를 비교함.

유클리디안 거리가 가장 짧은 라벨을 리턴함.

## Demo

### 1. 메인 및 로그인 페이지

![main](https://user-images.githubusercontent.com/77189999/217685011-4c5a61e2-74c2-498c-929f-d724c5150fa0.png)

#### 로그인 버튼 클릭 시

![login recording](https://user-images.githubusercontent.com/77189999/217685129-9b9e89ff-612e-4cdc-a37a-a256542468da.png)

#### '안녕하세요' 입력 후 성공

![success](https://user-images.githubusercontent.com/77189999/217685594-33fd266f-fb32-4a05-a0cb-5245c1bfe452.png)

### 2. 회원가입 페이지

![register](https://user-images.githubusercontent.com/77189999/217685068-66ec449f-afc4-45cf-9180-33a5f850f3aa.png)

#### 총 3차 녹음을 한 후 회원가입이 가능함

![recording](https://user-images.githubusercontent.com/77189999/217685372-ac1d8a8c-e884-4b87-8729-e444cca72d17.png)

#### 회원가입 버튼 클릭시 데이터베이스에 저장 및 학습 시작
