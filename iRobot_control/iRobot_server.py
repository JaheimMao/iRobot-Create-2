import math
import time
import pycreate2


def create_init():
    # 对iRobot Create 2串口进行配置
    # 默认波特率为115200

    port = 'com5'
    baud = {
        'default': 115200,
        'alt': 19200
    }

    bot = pycreate2.Create2(port, baud['default'])
    return bot


bot = create_init()


def create_start(bot):
    # iRobot Create 2开启串口
    # 配置到safe模式

    bot.start()
    time.sleep(1)

    bot.safe()
    time.sleep(1)

    print("Starting......")


def create_stop(bot):
    bot.stop()
    time.sleep(1)

    print("Stopping......")


def create_left(bot):
    print("Turn left starting......")
    bot.safe()
    bot.drive_turn(100, 2)
    time.sleep(1)

    bot.drive_straight(0)
    time.sleep(0.1)


def create_right(bot):
    print("Turn right starting......")
    bot.safe()
    bot.drive_turn(-100, 2)
    time.sleep(1)

    bot.drive_straight(0)
    time.sleep(0.1)


def create_go(bot):
    print("Go straight starting......")
    bot.safe()
    bot.drive_straight(200)
    time.sleep(1)

    bot.drive_straight(0)
    time.sleep(0.1)


def create_back(bot):
    print("Go back starting......")
    bot.safe()
    bot.drive_straight(-200)
    time.sleep(1)

    bot.drive_straight(0)
    time.sleep(0.1)


def create_clean(bot):
    print("iRobot start to clean")
    bot.clean()
    time.sleep(1)


def create_spot(bot):
    print("iRobot start to spot")
    bot.spot()
    time.sleep(1)


def get_voltage(bot):
    # 获取iRobot Create 2运行过程中的实时电压变化
    # 电压单位转换为V

    voltage = bot.get_sensors().voltage / 1000

    return voltage


def get_current(bot):
    # 获取iRobot Create 2运行过程中的实时电流变化

    current = bot.get_sensors().current

    return current


def get_encoder_counts(bot):
    encoder_counts_left = bot.get_sensors().encoder_counts_left
    encoder_counts_right = bot.get_sensors().encoder_counts_right

    return encoder_counts_left, encoder_counts_right


def calculate_distance_wheel(encoder_counts_old, encoder_counts_new):
    # 通过计算获得iRobot Create 2的运行距离
    # 计算公式为N counts * (mm in 1 wheel revolution / counts in 1 wheel revolution) = mm
    wheel_revolution_mm = math.pi * 72.0
    wheel_revolution_counts = 508.8
    n_counts = encoder_counts_new - encoder_counts_old

    if encoder_counts_new < 200 and encoder_counts_old > 65000:
        n_counts = encoder_counts_new + 65536 - encoder_counts_old

    elif encoder_counts_old < 200 and encoder_counts_new > 65000:
        n_counts = encoder_counts_new - 65536 - encoder_counts_old

    distance = n_counts * wheel_revolution_mm / wheel_revolution_counts

    return distance


def calculate_distance(encoder_counts_left_old, encoder_counts_left_new,
                       encoder_counts_right_old, encoder_counts_right_new):
    # 通过计算获得iRobot Create 2的运行距离
    # 计算公式为N counts * (mm in 1 wheel revolution / counts in 1 wheel revolution) = mm

    wheel_revolution_mm = math.pi * 72.0
    wheel_revolution_counts = 508.8
    n_counts_left = encoder_counts_left_new - encoder_counts_left_old
    n_counts_right = encoder_counts_right_new - encoder_counts_right_old
    if encoder_counts_left_new < 200 and encoder_counts_left_old > 65000:
        n_counts_left = encoder_counts_left_new + 65536 - encoder_counts_left_old

    elif encoder_counts_left_old < 200 and encoder_counts_left_new > 65000:
        n_counts_left = encoder_counts_left_new - 65536 - encoder_counts_left_old

    if encoder_counts_right_new < 200 and encoder_counts_right_old > 65000:
        n_counts_right = encoder_counts_right_new + 65536 - encoder_counts_right_old

    elif encoder_counts_left_old < 200 and encoder_counts_left_new > 65000:
        n_counts_right = encoder_counts_right_new - 65536 - encoder_counts_right_old

    n_counts_average = (n_counts_left + n_counts_right) / 2

    distance = n_counts_average * wheel_revolution_mm / wheel_revolution_counts / 10
    # 单位转换为厘米

    return distance


def get_velocity(bot):
    # 获取iRobot Create 2运行过程中的速度

    velocity = bot.get_sensors().velocity
    return velocity


def get_angle(encoder_counts_left_old, encoder_counts_left_new, encoder_counts_right_old, encoder_counts_right_new):
    # 获取iRobot Create 2运行过程中转过的角度值
    # 计算公式为angle in radians = (left wheel distance – right wheel distance) / wheel base distance

    right_wheel_distance = calculate_distance_wheel(encoder_counts_right_old, encoder_counts_right_new)
    left_wheel_distance = calculate_distance_wheel(encoder_counts_left_old, encoder_counts_left_new)
    wheel_base_distance = 253.00

    angle_in_radians = (left_wheel_distance - right_wheel_distance) / wheel_base_distance

    return angle_in_radians


def get_location(last_x, last_y, distance, angle):
    location_x = last_x + distance * math.sin(angle)
    location_y = last_y + distance * math.cos(angle)

    return location_x, location_y
