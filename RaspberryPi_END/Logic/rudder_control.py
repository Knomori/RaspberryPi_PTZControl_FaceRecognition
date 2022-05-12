# from time import sleep
# import RPi.GPIO as GPIO
# from Logic import raspi_parameter
# import atexit
#
#
# def set_servo_angle(gpio_num, angle):
#     atexit.register(GPIO.cleanup)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(gpio_num, GPIO.OUT, initial=False)
#     p = GPIO.PWM(gpio_num, 50)  # 50HZ
#     p.start(0)
#
#     p.ChangeDutyCycle(2.5 + 10 * angle / 180)  # 设置转动角度
#     sleep(0.02)  # 等该20ms周期结束
#     p.ChangeDutyCycle(0)  # 归零信号
#
#
# def rudder_move_down():
#     gpio_num = raspi_parameter.rudder_gpioNUM_portrait
#     raspi_parameter.rudder_angleNOW_portrait += 2
#     angel = raspi_parameter.rudder_angleNOW_portrait
#
#     if angel <= raspi_parameter.rudder_max_down:
#         set_servo_angle(gpio_num, angel)
#     else:
#         print("无法完成动作（已经到了下极限距离）")
#         raspi_parameter.rudder_angleNOW_portrait -= 2
#
#
# def rudder_move_up():
#     gpio_num = raspi_parameter.rudder_gpioNUM_portrait
#     raspi_parameter.rudder_angleNOW_portrait -= 2
#     angel = raspi_parameter.rudder_angleNOW_portrait
#
#     if angel >= raspi_parameter.rudder_max_up:
#         set_servo_angle(gpio_num, angel)
#     else:
#         print("无法完成动作（已经到了上极限距离）")
#         raspi_parameter.rudder_angleNOW_portrait += 2
#
#
# def rudder_move_left():
#     gpio_num = raspi_parameter.rudder_gpioNUM_landscape
#     raspi_parameter.rudder_angleNOW_landscape -= 2
#     angel = raspi_parameter.rudder_angleNOW_landscape
#
#     if angel >= raspi_parameter.rudder_max_left:
#         set_servo_angle(gpio_num, angel)
#     else:
#         print("无法完成动作（已经到了左极限距离）")
#         raspi_parameter.rudder_angleNOW_landscape += 2
#
#
# def rudder_move_right():
#     gpio_num = raspi_parameter.rudder_gpioNUM_landscape
#     raspi_parameter.rudder_angleNOW_landscape += 2
#     angel = raspi_parameter.rudder_angleNOW_landscape
#
#     if angel <= raspi_parameter.rudder_max_right:
#         set_servo_angle(gpio_num, angel)
#     else:
#         print("无法完成动作（已经到了右极限距离）")
#         raspi_parameter.rudder_angleNOW_landscape -= 2
