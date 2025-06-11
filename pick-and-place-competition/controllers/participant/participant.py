"""Sample Webots controller for the pick and place benchmark."""

from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Initialize wheels
wheels = [robot.getDevice(f"wheel{i+1}") for i in range(4)]
for wheel in wheels:
    wheel.setPosition(float('+inf'))

# Initialize arm motors
armMotors = [robot.getDevice(f"arm{i+1}") for i in range(5)]
armMotors[0].setVelocity(0.2)
armMotors[1].setVelocity(0.5)
armMotors[2].setVelocity(0.5)
armMotors[3].setVelocity(0.7)

# Initialize arm sensors
armPositionSensors = [robot.getDevice(f"arm{i+1}sensor") for i in range(5)]
for sensor in armPositionSensors:
    sensor.enable(timestep)

# Initialize gripper
finger1 = robot.getDevice("finger1")
finger2 = robot.getDevice("finger2")
finger1.setVelocity(0.05)
finger2.setVelocity(0.05)
fingerMinPosition = finger1.getMinPosition()
fingerMaxPosition = finger1.getMaxPosition()

# Andar para frente
omega = 12
distancia = 2.912
angulo = distancia / 0.05
tempo = angulo / omega
for wheel in wheels:
    wheel.setVelocity(omega)
robot.step(int(tempo * 1000) + 16)
for wheel in wheels:
    wheel.setVelocity(0.0)

# Posicionar braço
armMotors[0].setPosition(0.05)
armMotors[1].setPosition(-0.55)
armMotors[2].setPosition(-0.95)
armMotors[3].setPosition(-1.35)
finger1.setPosition(fingerMaxPosition)
finger2.setPosition(fingerMaxPosition)

# === MALHA FECHADA no armMotors[3] ===
# Ativar modo de velocidade
armMotors[3].setPosition(float('inf'))
# Controle proporcional
target = -1.5
kp = 3.0
tolerance = 0.03
while robot.step(timestep) != -1:
    erro = target - armPositionSensors[3].getValue()
    if abs(erro) < tolerance:
        break
    armMotors[3].setVelocity(max(min(kp * erro, 1.57), -1.57))
armMotors[3].setVelocity(0.0)
# ======================================

# Fechar garra
finger1.setPosition(0.013)
finger2.setPosition(0.013)
robot.step(50 * timestep)

# Levantar braço
armMotors[1].setPosition(0)
robot.step(200 * timestep)

# Girar robô
omega_rot = 7
tempo_rot = 27.5 / omega_rot
wheels[0].setVelocity(omega_rot)
wheels[1].setVelocity(-omega_rot)
wheels[2].setVelocity(omega_rot)
wheels[3].setVelocity(-omega_rot)
robot.step(int(tempo_rot * 1000))
for wheel in wheels:
    wheel.setVelocity(0.0)

# Andar para frente
omega = 2.5
distancia = 1.8
tempo = (distancia / 0.05) / omega
for wheel in wheels:
    wheel.setVelocity(omega)
robot.step(int(tempo * 1000))

# Ajustes finos
wheels[0].setVelocity(1.0)
wheels[1].setVelocity(-1.0)
wheels[2].setVelocity(1.0)
wheels[3].setVelocity(-1.0)
robot.step(200 * timestep)

wheels[1].setVelocity(1.0)
wheels[3].setVelocity(1.0)
robot.step(300 * timestep)

wheels[0].setVelocity(1.0)
wheels[1].setVelocity(-1.0)
wheels[2].setVelocity(1.0)
wheels[3].setVelocity(-1.0)
robot.step(130 * timestep)

wheels[1].setVelocity(1.0)
wheels[3].setVelocity(1.0)
robot.step(310 * timestep)

for wheel in wheels:
    wheel.setVelocity(0.0)

# Descarregar objeto
armMotors[3].setPosition(0)
armMotors[2].setPosition(-0.3)
robot.step(200 * timestep)
armMotors[1].setPosition(-1.0)
robot.step(200 * timestep)
armMotors[3].setPosition(-1.0)
robot.step(200 * timestep)
armMotors[2].setPosition(-0.4)
robot.step(50 * timestep)

# Abrir garra
finger1.setPosition(fingerMaxPosition)
finger2.setPosition(fingerMaxPosition)
robot.step(50 * timestep)

# Levantar braço
armMotors[1].setPosition(0)
robot.step(200 * timestep)
