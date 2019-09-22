O#include<Servo.h>

Servo servo[4];

int prevAngles[4] = {600, 1500, 600, 600};
int angleCalib[4] = {710, 100, 880, 960};
int TD = 3;

void runServo(int n, int angle1, int angle2){
  int delta = angle2 - angle1;
  if(delta >= 0){
    for(int i=0;i<=delta;i++){
      servo[n].writeMicroseconds(angle1+i+ angleCalib[n]);
      delay(TD);
    }  
  } else {
    delta = delta * -1;
    for(int i=0;i<=delta;i++){
      servo[n].writeMicroseconds(angle1-i+ angleCalib[n]);
      delay(TD);
    }
  }
}

void Split(String sData, char cSeparator)
{ 
  int arr[4];
  int nCount = 0;
  int nGetIndex = 0 ;
  int cnt = 0;

  //임시저장
  String sTemp = "";

  //원본 복사
  String sCopy = sData;

  while(true)
  {
    //구분자 찾기
    nGetIndex = sCopy.indexOf(cSeparator);

    //리턴된 인덱스가 있나?
    if(-1 != nGetIndex)
    {
      //있다.

      //데이터 넣고
      sTemp = sCopy.substring(0, nGetIndex);
      
      arr[cnt++] = sTemp.toInt();
      
      //Serial.println( sTemp );
    
      //뺀 데이터 만큼 잘라낸다.
      sCopy = sCopy.substring(nGetIndex + 1);
    }
    else
    {
      //없으면 마무리 한다.
      //Serial.println( sCopy );
      arr[cnt] = sCopy.toInt();
      break;
    }

    //다음 문자로~
    ++nCount;
  }
  for(int i=0;i<4;i++){
      int x = arr[i] + 600;

      runServo(i, prevAngles[i], x);

      
      Serial.print("Prev: ");
      Serial.print(prevAngles[i]-600);
      Serial.print(" Now: ");
      Serial.print(x-600);
      Serial.print(" / ");
      prevAngles[i] = x;
      
  }
  Serial.println("");
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0;i<4;i++){
    servo[i].attach(11-i, 600, 2400);
    servo[i].writeMicroseconds(prevAngles[i] +angleCalib[i]);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    String str = Serial.readString();
    Split(str, ':');
  }
}
