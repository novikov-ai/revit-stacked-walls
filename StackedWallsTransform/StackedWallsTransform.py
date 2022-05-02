import clr #необходимо для модуля библиотек .NET
clr.AddReference('RevitAPI') #ссылка на библиотеку dll
from Autodesk.Revit.DB import * #импорт всех классов

clr.AddReference('RevitServices') #импорт библиотеки для загрузки классов DM и TM
from RevitServices.Persistence import DocumentManager as DM
from RevitServices.Transactions import TransactionManager as TM

doc=DM.Instance.CurrentDBDocument #ссылка на текущий документ

SW=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StackedWalls).WhereElementIsNotElementType().ToElements() #получение всех стен в проекте

WI=[] #выбор id стен, входящих в состав составных

for i in SW :
	WI.append(i.GetStackedWallMemberIds())
	
W=[] #выбор стен, входящих в состав составных

for i in WI:
	for j in i:
		W.append(doc.GetElement(j))
		
TM.Instance.EnsureInTransaction(doc)

if IN[0]==True:
	for i in W:	
		H=int(i.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM).AsValueString().split(',')[0])/304.8 #получение высоты элемента и переведенное в мм (так как в API используются футы)			
		O=int(i.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET).AsValueString().split(',')[0])/304.8 #получение смещения				
		Wall.Create(doc,i.Location.Curve,i.WallType.Id,i.LevelId,H,O,i.Flipped,False) #создание стен		
	OUT="Created "+str(len(W))+" Walls."	
else:
	OUT="<True> is expected."
	
if IN[1]==True:
	for i in SW:
		doc.Delete(i.Id) #удаление стен
	OUT="Deleted "+str(len(SW))+" Stacked Walls"

if IN[0]*IN[1]==True:
	OUT="Created "+str(len(W))+" Walls. Deleted "+str(len(SW))+" Stacked Walls"

TM.Instance.TransactionTaskDone()