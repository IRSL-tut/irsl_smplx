from irsl_robots.hrp4c_model.hrp4c_model import HRP4C
robot = HRP4C()
#import cnoid.PoseSeqPlugin
from cnoid.PoseSeqPlugin import createPoseSeqItem

ret = createPoseSeqItem(robot.item, 'poseseq/seq_001.pseq')

ret.interpolator.seek(0.0)
ret.interpolator.update()

ret.interpolator.seek(3.0)
robot.angleVector(ret.interpolator.getJointDisplacements())
if ret.interpolator.baseLinkIndex == 0:
  cds = coordinates(ret.interpolator.baseLinkPosition)
  robot.rootCoords(cds)
