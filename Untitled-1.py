def grip_close():
    set_digital_output(1,ON)
    set_digital_output(2,OFF)
    wait(0.5)

def grip_open():
    set_digital_output(1,OFF)
    set_digital_output(2,ON)
    wait(0.5)

x1=posx(400, -50, 300, 20.7806, 179.5791, 21.3655)
x2=posx(400, -150, 300, 48.4023, 179.2170, 49.3191)
x3=posx(500, -150, 300, 76.9858, 178.9296, 77.5844)
x4=posx(500, -50, 300, 45.2451, 179.4428, 45.9098)

y1=posx(400, 50, 300,    158.491,    179.965,    158.877)
y2=posx(490, 50, 300,    158.491,    179.965,    158.877)
y3=posx(490, 160, 300,    158.491,    179.965,    158.877)
y4=posx(400, 160, 300,    158.491,    179.965,    158.877)

direction = 0
row = 3 
column = 3
stack = 1
thickness = 0 
point_offset = [0, 0, 0]

# Total count
total_count = row * column * stack

# 도착지 위치 지정을 위한 변수 지정
cnt_large = 0
cnt_mid = 0
cnt_small = 0

# 높이 측정을 위한 grip_close
grip_close()

# 인덱스 부여
for pallet_index in range(0, total_count): 
    Pallet_Pose = get_pattern_point(x1,x2,x3,x4, pallet_index, direction, row, column, stack, thickness, point_offset) 
    movel(Pallet_Pose,v=50,a=50)
    
    # compliance 작동
    task_compliance_ctrl() 
    set_stiffnessx([200, 200, 200, 100, 100, 100]) 
    set_desired_force(fd = [0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0]) 
    
    # movel(0, 0, -50, 0, 0, 0, v=20, a=20, mod=DR_MV_MOD_REL)

    while True:
        # DR_AXIS_Z 방향으로 설정한 힘이 감지되는지 확인
        if check_force_condition(DR_AXIS_Z, min=0.5): 
            break
        wait(0.5)

    # 힘 제어 해제		  
    release_force(time=0.5)
    release_compliance_ctrl()

	# 크기분류를 위한 변수 지정
    block_size = 0
    current_z = get_current_posx()[2] 
    # 대
    if current_z >= 283.5:
        block_size = 1
    # 중
    elif current_z>= 275.3:
        block_size = 2
    # 소
    else:
        block_size = 3

    
    # z방향 상승 
    movel([0,0,30,0,0,0],
      v=50, a=30,
      mod=DR_MV_MOD_REL)
    # Z방향 하강
    movel([0,0,-40,0,0,0],
      v=50, a=30,
      mod=DR_MV_MOD_REL
      )
        

    grip_close()
    
    # Z축 상승
    movel([0,0,80,0,0,0],
    v=50, a=30,
    ref=DR_TOOL,
    mod=DR_MV_MOD_REL)

    # 도착지 이동
    Pick_Pose = get_pattern_point(
		  y1, y2, y3, y4,
		  pallet_index,
		  direction,
		  row, column, stack,
		  thickness, point_offset
		)

    if block_size == 1:
        Target_Pose = get_pattern_point(y1, y2, y3, y4, cnt_large, direction, row, column, stack, thickness, point_offset)
        movel(Target_Pose, v=100, a=50)
        cnt_large += 1
    elif block_size ==2:
        Target_Pose = get_pattern_point(y1, y2, y3, y4, cnt_mid, direction, row, column, stack, thickness, point_offset)
        movel(Target_Pose, v=100, a=50)
        cnt_mid += 1
    elif block_size ==3:
        Target_Pose = get_pattern_point(y1, y2, y3, y4, cnt_small, direction, row, column, stack, thickness, point_offset)
        movel(Target_Pose, v=100, a=50)
        cnt_small += 1
    
    movel([0,0,-20,0,0,0], v=50, a=20, mod=DR_MV_MOD_REL)
    grip_open()
