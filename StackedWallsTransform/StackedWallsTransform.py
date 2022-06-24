import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager as DM
from RevitServices.Transactions import TransactionManager as TM

doc=DM.Instance.CurrentDBDocument

SW=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StackedWalls).WhereElementIsNotElementType().ToElements()

WI=[]

for i in SW :
	WI.append(i.GetStackedWallMemberIds())
	
W=[]

for i in WI:
	for j in i:
		W.append(doc.GetElement(j))
		
TM.Instance.EnsureInTransaction(doc)

if IN[0]==True:
	for i in W:	
		H=int(i.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsValueString().split(',')[0])/304.8		
		O=int(i.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET).AsValueString().split(',')[0])/304.8
		Wall.Create(doc,i.Location.Curve,i.WallType.Id,i.LevelId,H,O,i.Flipped,False)
	OUT="Created "+str(len(W))+" Walls."	
else:
	OUT="<True> is expected."
	
if IN[1]==True:
	for i in SW:
		doc.Delete(i.Id)
	OUT="Deleted "+str(len(SW))+" Stacked Walls"

if IN[0]*IN[1]==True:
	OUT="Created "+str(len(W))+" Walls. Deleted "+str(len(SW))+" Stacked Walls"

TM.Instance.TransactionTaskDone()