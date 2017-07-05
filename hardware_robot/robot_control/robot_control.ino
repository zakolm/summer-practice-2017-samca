/*
 * Arduino Robot 2 Wheel with Motor Shield, UltraSonic distance sensor
 * Arduino робот-гид, 2 колесный, с платой управления моторами, ультразвуковой измеритель расстояния
 * SAMCA
 */
#define VERSION "RobotGuide2W ver.2017.00.00.01.01" 
 /*
 * Виды поворотов.
 */
 int test = 0;
#define STRIEGHT_STEP 1
#define RIGHT_STEP 2
#define LEFT_STEP 3
int step_robot;
/*
 * Задержки для езды, поворотов на месте и плавных поворотов.
 * Подбираются экспериментально.
 * Пока в разработке.
 */
const int DELAY_RUN = 2;
const int DELAY_RUN_BACK = 50;
const int DELAY_ROTATE = 500;
const int DELAY_TURN = 500;
const int DELAY_TURN_BACK = 500;
/* Пины для подключения двигателя L298N 
 * 9, 6 цифровые пины для регулировки скорости.
 * 14, 15, 16, 17 аналоговые пины A0, A1, A2 и A3 соответственно, для подключения к мотору.
 */
// Первый двигатель.  
int inA = 14;
int inB = 15;
// Второй двигатель.  
int inC = 16;
int inD = 17;
// Подключение пинов скорости.  
int EN1 = 9; // первый двигатель.
int EN2 = 6; // второй двигатель.
/* Пины для подключения датчика скорости двигателя Q86(энкодеры)
 * 2, 3 специальные пины для работы с "внешним прерыванием"
 */
// Тестовые данные об энекодере.  
int ENC1 = 2;
int ENC2 = 3;
int pulses_left, pulses_right; // счетчик.
/*
 * Массив(вектор) пути робота.
 */
// "Переданный массив".  
//int a[] = {1, 2, 3, 1, 2, 3};
int a[] = {1, 1, 1, 1};
int* pa = a;
int count = sizeof(a)/sizeof(int);
int i = 0;

//-------------------------------------------------------------------------------------------//
/*
 * Функции для энкодера при повороте направо или влево.
 */
void counter_right(){
  if ( pulses_right >= 33 ){
    analogWrite(EN1, 255);
    digitalWrite(inC, LOW);
    digitalWrite(inD, LOW);
    test = 5;
  }
 pulses_right++;
}
void counter_left(){
  if ( pulses_left >= 33 ){
    analogWrite(EN2, 0);
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
    test = 6;
  }
 pulses_left++;
}
//-------------------------------------------------------------------------------------------//
/******************************************
  Main program
******************************************/
// Инициализируем все пины для управления двигателями как outputs.  
void setup() {
  /* 
   * некоторые переменные необходимо инициализировать именно здесь. 
   * Я из будущего: "Просто прими это как данность!"
   */  
  step_robot = 0;
  pulses_left = 0; pulses_right = 0;
  // Подключение модулей для работы с монитором порта.
  Serial.begin(9600);
  Serial.println(VERSION);
  // Подключаем энкодеры.
  pinMode(ENC1, INPUT);
  pinMode(ENC2, INPUT);
  attachInterrupt(digitalPinToInterrupt(ENC1), counter_left, FALLING);
  attachInterrupt(digitalPinToInterrupt(ENC2), counter_right, FALLING);
  // Подключаем все необходимые пины для движения и управления скоростью
  pinMode(EN1, OUTPUT);
  pinMode(inA, OUTPUT);
  pinMode(inB, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(inC, OUTPUT);
  pinMode(inD, OUTPUT);
}

void loop() {
  Serial.print(pulses_left);
  Serial.print(' ');
  Serial.print(pulses_right);
  Serial.print(' ');
  Serial.println(test);
  if ( !step_robot ) left(); 
  
  /*Serial.println("\n*** new loop() start ***\n");
  //Serial.print("%d", i);
  int step_robot = 0;
  if ( i < count ){
    step_robot = a[i];
    switch(step_robot){
      case STRIEGHT_STEP:
        streight();
        delay(5000);
        break;
      case RIGHT_STEP:
        right();
        delay(1000);
        break;
      case LEFT_STEP:
        left();
        delay(1000);
        break;
    }
    i++;
    stop_robot();*/
    
  //}
  //-------------------------
  /*
  analogWrite(EN1, 255);
  analogWrite(EN2, 200);
  digitalWrite(inA, HIGH);
  //digitalWrite(inB, LOW);
  //digitalWrite(inC, LOW);
  digitalWrite(inD, HIGH);
  */
  //-------------------------
  
}
//-------------------------------------------------------------------------------------------//
/******************************************
  Functions
******************************************/
// Подача тока на оба двигателя.
void turn_on(){
  analogWrite(EN1, 255);
  analogWrite(EN2, 255);
}
// Движение прямо.
void streight(){
  turn_on();
  digitalWrite(inA, HIGH);
  digitalWrite(inB, LOW);
  digitalWrite(inC, LOW);
  digitalWrite(inD, HIGH);
}
// Поворот направо.
void right(){
  pulses_left = 0; pulses_right = 0;
  turn_on();
  digitalWrite(inA, HIGH);
  digitalWrite(inB, LOW);
  digitalWrite(inC, HIGH);
  digitalWrite(inD, LOW);
}
// Поворот налево.
void left(){
  pulses_left = 0; pulses_right = 0;
  turn_on();
  digitalWrite(inA, LOW);
  digitalWrite(inB, HIGH);
  digitalWrite(inC, LOW);
  digitalWrite(inD, HIGH);
  step_robot = 1;
}
// Полная остановка робота.
// Просто пока оставим это здесь, пожалуйста!
void stop_robot(){
  analogWrite(EN1, 0);
  analogWrite(EN2, 0);
  digitalWrite(inA, LOW);
  digitalWrite(inB, LOW);
  digitalWrite(inC, LOW);
  digitalWrite(inD, LOW);
}