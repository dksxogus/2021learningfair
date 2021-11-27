import pygame   #파이 게임 모듈 가져오기
import random    
import time
import math     #수학 함수에 대한 액세스를 제공

pygame.init() #pygame 초기화(초기화를 하지 않을 시, 일부 기능이 정상 동작하지 않을 수 있다.)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정(가로 1000, 세로 750)
clock = pygame.time.Clock() 

#변수

GREEN = (155, 229, 200)   # 게임 배경화면 색깔
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont('malgungothic', 72)   #폰트를 맑은고딕체 72크기로 지정
small_font = pygame.font.SysFont('malgungothic', 36)   #폰트를 맑은고딕체 36크기로 지정
score = 0
start_time = int(time.time()) #0시 0분 0초 부터 현재까지 초 
remain_second = 50  # 제한시간 50초
game_over = False

virus_image = pygame.image.load('virus.png')   # 바이러스 이미지 불러오기
viruss = []   #바이러스들을 담을 리스트 선언
for i in range(15): 
    virus = virus_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - virus_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - virus_image.get_height())
    degree = random.randint(0, 360)   #0 이상 360 이하 랜덤한 정수(int)
    viruss.append((virus, degree))   #객체와 각도를 바이러스들 리스트 안에 삽입

mask_image = pygame.image.load('mask.png')   # 마스크 이미지 불러오기
masks = []   #마스크들을 담을 리스트 선언
for i in range(10):  
    mask = mask_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - mask_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - mask_image.get_height()) 
    degree = random.randint(0, 360)
    masks.append((mask, degree))   #객체와 각도를 마스크 리스트들 안에 삽입

pygame.mixer.music.load('music.mp3')   #배경 음악
pygame.mixer.music.play(-1)   #-1: 무한 반복, 0: 한번
squish_sound = pygame.mixer.Sound('squish.mp3')   #소리 정의하기 
game_over_sound = pygame.mixer.Sound('game_over.mp3')   # 제한 시간 종류 후 사운드

while True: #게임 루프
    screen.fill(GREEN)  # 단색으로 채워 화면 지우기

    #변수 업데이트

    event = pygame.event.poll()   #이벤트 처리
    if event.type == pygame.QUIT:   #창 닫기 버튼 클릭시 코드 멈춤
        break
    elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:   #마우스 버튼을 눌렀을 때
        for virus, degree in viruss:
            if virus.collidepoint(event.pos):   #충돌 체크(접속을 판단)
                viruss.remove((virus, degree))   #접속했다면, 바이러스와 각도를 리스트에서 제거
                virus = virus_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - virus_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - virus_image.get_height())
                degree = random.randint(0, 360)
                viruss.append((virus, degree))
                score += 1   # 바이러스를 누르면 1점 추가와 사운드 재생
                squish_sound.play()
                if score>=40:
                    game_over = True
                    pygame.mixer.music.stop()
                    game_over_sound.play()
               

    if not game_over:
        current_time = int(time.time()) 
        remain_second = 50 - (current_time - start_time)

        if remain_second <= 0:
            game_over = True   #게임 종료시 기존의 음악이 멈추고, 게임 오버 사운드 
            pygame.mixer.music.stop()
            game_over_sound.play()

        for virus, degree in viruss:
            radian = degree * (math.pi / 180)   # math.pi / 180은 1도의 값
            dx = 7 * math.cos(radian)   # 바이러스의 가로축 속도 
            dy =  - 7 * math.sin(radian)   # 바이러스의 세로축 속도 
            virus.left += dx
            virus.top += dy

        for virus, degree in viruss:
            if not virus.colliderect(screen.get_rect()):   #바이러스를 클릭하지 않았을 때
               viruss.remove((virus, degree))   #리스트에서 삭제
               virus = virus_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - virus_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - virus_image.get_height())
               degree = random.randint(0, 360)
               viruss.append((virus, degree))   #리스트에 추가
               
               event = pygame.event.poll() #이벤트 처리

     #위의 바이러스 코드와 일치
    if event.type == pygame.QUIT:  
        break
    elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
        for mask, degree in masks:
            if mask.collidepoint(event.pos):
                masks.remove((mask, degree))
                mask = mask_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - mask_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - mask_image.get_height())
                degree = random.randint(0, 360)
                masks.append((mask, degree))
                score -= 1
                squish_sound.play()

    if not game_over:
        current_time = int(time.time())
        remain_second = 50 - (current_time - start_time)

        if remain_second <= 0:
            game_over = True
            pygame.mixer.music.stop()
            game_over_sound.play()

        for mask, degree in masks:
            radian = degree * (math.pi / 180)
            dx = 4 * math.cos(radian)
            dy =  - 4 * math.sin(radian)
            mask.left += dx
            mask.top += dy

        for mask, degree in masks:
            if not mask.colliderect(screen.get_rect()):
               masks.remove((mask, degree))
               mask = mask_image.get_rect(left=random.randint(0, SCREEN_WIDTH) - mask_image.get_width(), top=random.randint(0, SCREEN_HEIGHT) - mask_image.get_height())
               degree = random.randint(0, 360)
               masks.append((mask, degree))

    #화면 그리기

    for virus, degree in viruss: 
        rotated_virus_image = pygame.transform.rotate(virus_image, degree)
        screen.blit(rotated_virus_image, (virus.left, virus.top))   #이미지 복사 (바이러스 이미지, 해당 위치)
        
    for mask, degree in masks: 
        rotated_mask_image = pygame.transform.rotate(mask_image, degree)
        screen.blit(rotated_mask_image, (mask.left, mask.top))   #이미지 복사 (마스크 이미지, 해당 위치)


    score_image = small_font.render('점수 {}'.format(score), True, YELLOW)   #점수는 맑은고딕체 36크기인 노란 색깔의 글씨이다. 
    screen.blit(score_image, (10, 10))

    remain_second_image = small_font.render('바이러스에 감염되기까지 {}'.format(remain_second), True, YELLOW)   #맑은고딕체 36크기인 노란 색깔의 글씨이다.
    screen.blit(remain_second_image, remain_second_image.get_rect(right=SCREEN_WIDTH - 10, top=10))   #글씨 위치 설정

    if game_over:
        if score>=40:
            game_over_image = large_font.render('바이러스를 퇴치하였습니다.', True, RED)    #맑은고딕체 72크기인 빨간 색깔의 글씨이다.
            screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))   #화면 중앙에 복사
        else:
            game_over_image = large_font.render('바이러스에 감염되었습니다.', True, RED)    #맑은고딕체 72크기인 빨간 색깔의 글씨이다.
            screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))   #화면 중앙에 복사
        

    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값


pygame.quit() 
