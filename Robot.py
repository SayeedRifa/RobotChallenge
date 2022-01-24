import fileinput

ENABLE_DEBUG = False
def debugLog(message):
  if ENABLE_DEBUG:
    print(f"[DEBUG] {message}")

class Command:
  def __init__(self, name):
    self.name = name

class PlaceCommand(Command):
  def __init__(self, name, x, y, direction):
    Command.__init__(self, name)
    self.x = x
    self.y = y
    self.direction = direction

class RobotCommand(Command):
  def __init__(self, name, robotID):
    Command.__init__(self, name)
    self.robotID = robotID
  
# Commands:
# PLACE X,Y,F
# MOVE
# LEFT
# RIGHT
# REPORT
# ROBOT <number>
def parseCommand(commandText) -> Command:
  commandComponents = commandText.split()
  commandName = commandComponents[0]
  command = None
  if commandName == "PLACE":
    commandSubComponents = commandComponents[1].split(",")
    x = int(commandSubComponents[0])
    y = int(commandSubComponents[1])
    direction = commandSubComponents[2]
    command = PlaceCommand(commandName, x, y, direction)
  elif commandName == "MOVE" or commandName == "LEFT" or commandName == "RIGHT" or commandName == "REPORT":
    command = Command(commandName)
  elif commandName == "ROBOT":
    robotID = int(commandComponents[1])
    command = RobotCommand(commandName, robotID)
  else:
    debugLog("Command not supported!")
  return command

class Robot:
  def __init__(self, x, y, direction, identifier) -> None:
    self.x = x
    self.y = y
    self.direction = direction
    self.identifier = identifier

  def getNextPositionIfMoveForward(self):
    x = self.x
    y = self.y
    if self.direction == "NORTH":
      y = y + 1
    elif self.direction == "SOUTH":
      y = y - 1
    elif self.direction == "WEST":
      x = x - 1
    elif self.direction == "EAST":
      x = x + 1
    return (x, y)

  def moveForward(self):
    if self.direction == "NORTH":
      self.y = self.y + 1
    elif self.direction == "SOUTH":
      self.y = self.y - 1
    elif self.direction == "WEST":
      self.x = self.x - 1
    elif self.direction == "EAST":
      self.x = self.x + 1
  
  def rotateLeft(self):
    if self.direction == "NORTH":
      self.direction = "WEST"
    elif self.direction == "WEST":
      self.direction = "SOUTH"
    elif self.direction == "SOUTH":
      self.direction = "EAST"
    elif self.direction == "EAST":
      self.direction = "NORTH"

  def rotateRight(self):
    if self.direction == "NORTH":
      self.direction = "EAST"
    elif self.direction == "EAST":
      self.direction = "SOUTH"
    elif self.direction == "SOUTH":
      self.direction = "WEST"
    elif self.direction == "WEST":
      self.direction = "NORTH"

class Board:
  def __init__(self) -> None:
    self.robots = []
    self.activeRobotIndex = 1
    
  def getActiveRobot(self) -> Robot:
    for robot in self.robots:
      if robot.identifier == self.activeRobotIndex:
        return robot
    return None

  def isInsideBoard(x, y):
    return 0 <= x and x < 5 and 0 <= y and y < 5

  def canMoveForward(self, robot: Robot):
    nextPosition = robot.getNextPositionIfMoveForward()
    return Board.isInsideBoard(nextPosition[0], nextPosition[1])

  def excecuteCommand(self, command):
    if command.name == "PLACE":
      robotID = len(self.robots) + 1
      self.robots.append(Robot(command.x, command.y, command.direction, robotID))
    
    if command.name == "MOVE":
      robot = self.getActiveRobot()
      if robot != None:
        if self.canMoveForward(robot):
          robot.moveForward()
        else:
          debugLog("cannot move forward")
      else:
        debugLog("There is no robot")

    if command.name == "LEFT":
      robot = self.getActiveRobot()
      if robot != None:
        robot.rotateLeft()
      else:
        debugLog("There is no robot")
    
    if command.name == "RIGHT":
      robot = self.getActiveRobot()
      if robot != None:
        robot.rotateRight()
      else:
        debugLog("There is no robot")
    
    if command.name == "REPORT":
      self.report()

    if command.name == "ROBOT":
      self.activeRobotIndex = command.robotID

  def report(self):
    print(f"There is/are {len(self.robots)} robot(s):")
    for robot in self.robots:
      activeText = ""
      if self.activeRobotIndex == robot.identifier:
        activeText = " (Active)"
      print(f"{robot.x},{robot.y},{robot.direction}{activeText}")

if __name__ == "__main__":
  board = Board()
  for commandText in fileinput.input():
    command = parseCommand(commandText)
    if command == None:
      continue
    board.excecuteCommand(command)
    
