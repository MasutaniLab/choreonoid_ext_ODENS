import os
from cnoid.Util import *
from cnoid.Base import *
from cnoid.BodyPlugin import *

try:
    from cnoid.MulticopterPlugin import *
except:
    pass

try:
    from cnoid.AGXDynamicsPlugin import *
except:
    pass

try:
    from cnoid.ROSPlugin import *
except:
    pass

def loadProject(
    view, task, simulatorProjects, robotProjects,
    enableMulticopterSimulation = False, enableVisionSimulation = False, 
    targetVisionSensors = "", remoteType = "", taskType = "WRS2020"):

    projectdir = os.path.join(shareDirectory, "WRS2020", "project")
    projectdir_odens = os.path.join(shareDirectory, "ODENS", "project")
    taskdir = os.path.join(shareDirectory, taskType, "project")
    
    itv = ItemTreeView.instance
    pm = ProjectManager.instance

    viewProject = SubProjectItem()
    viewProject.name = "ViewProject"
    viewProject.load(os.path.join(projectdir, view + ".cnoid"))
    RootItem.instance.addChildItem(viewProject)
    itv.setExpanded(viewProject, False)

    world = WorldItem()
    world.name = "World"
    RootItem.instance.addChildItem(world)

    taskProject = SubProjectItem()
    taskProject.name = task
    taskProject.load(os.path.join(taskdir, task + ".cnoid"))
    world.addChildItem(taskProject)
    itv.setExpanded(taskProject, False)

    if not isinstance(simulatorProjects, list):
        simulatorProjects = [ simulatorProjects ]
    for project in simulatorProjects:
        pm.loadProject(os.path.join(projectdir, project + ".cnoid"), world)

    # Deselect the simulator items except the first one
    selectedSimulatorItems = RootItem.instance.getSelectedItems(SimulatorItem)
    for i in range(1, len(selectedSimulatorItems)):
        selectedSimulatorItems[i].setSelected(False)

    if not isinstance(robotProjects, list):
        robotProjects = [ robotProjects ]

    robotOffset = 0.0

    for robotProject in robotProjects:

        loadedItems = pm.loadProject(os.path.join(projectdir_odens, robotProject + ".cnoid"), world)
        if not loadedItems:
            continue
        robot = loadedItems[0]
        if not isinstance(robot, BodyItem):
            continue

        rootLink = robot.body.rootLink;
        p = rootLink.translation
        p[1] -= robotOffset
        rootLink.setTranslation(p)
        robot.notifyKinematicStateChange(True)
        robot.storeInitialState()
        robotOffset += 1.5

        if remoteType:
            if remoteType != "ROS_odens":
                joystickInput = SimpleControllerItem()
                joystickInput.name = robot.name + "-JoystickInput"
                mainController = robot.findItem(SimpleControllerItem)
                mainController.addChildItem(joystickInput)

            if remoteType == "ROS":
                joystickInput.setController("JoyTopicSubscriberController")
                bodyPublisher = BodyPublisherItem()
                bodyPublisher.name = "BodyPublisher"
                robot.addChildItem(bodyPublisher)

            elif remoteType == "ROS_odens":
                bodyROS = BodyROSItem()
                bodyROS.name = "BodyROS"
                robot.addChildItem(bodyROS)

        if enableMulticopterSimulation:
            multicopterSimulator = MulticopterSimulatorItem()
            for simulator in world.getDescendantItems(SimulatorItem):
                simulator.addChildItem(multicopterSimulator.duplicate())

        if enableVisionSimulation:
            visionSimulator = GLVisionSimulatorItem()
            visionSimulator.setTargetSensors(targetVisionSensors)
            visionSimulator.setBestEffortMode(True)
            for simulator in world.getDescendantItems(SimulatorItem):
                simulator.addChildItem(visionSimulator.duplicate())

    logItem = WorldLogFileItem()
    logItem.setLogFile(task + ".log")
    logItem.setTimeStampSuffixEnabled(True)
    logItem.setRecordingFrameRate(100)
    world.addChildItem(logItem)

    pm.setCurrentProjectName(task + "-" + robotProjects[0])
