from PIL import Image, ImageDraw, ImageFont
import os, json, math, zipfile
ROOT='/mnt/data/havrakah_levels_3d'
OUT=f'{ROOT}/diagrams'
os.makedirs(OUT,exist_ok=True)
FT='/usr/share/fonts/truetype/lato/Lato-Bold.ttf'
FR='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
font=lambda s,b=False: ImageFont.truetype(FT if b else FR,s)
COL={'ink':'#293149','navy':'#252C4A','line':'#D2C7B8','sand':'#F8F3E9','green':'#CDE8D3','teal':'#5FADA3','blue':'#5C90D7','violet':'#8975C9','gold':'#E7B65A','rose':'#E58B9A','grey':'#A9B1C1','brown':'#A37C5D'}
scene={'P00': {'title':'P00  |  KITCHEN  |  Tutorial','caption':'Tap clues -> inspect dog tag -> choose the dog', 'n': [('K1','Cake stand',-2.,1.1),('K2','Paw trail',0.2,0.15),('K3','Dog',2.5,1.9),('K4','Dog tag',2.8,1.55),('K5','Closed window',-2.8,2.8),('K6','Garden door',2.8,2.8)]},
'P01': {'title':'P01  |  DOGHOUSE  |  Easy','caption':'Move bowl -> inspect toy -> open seam -> collect key (D4/D5 callouts)','n':[('D1','Dog',2.3,1.6),('D2','Bowl: x -1.8 to -0.6',-1.8,-0.45),('D3','Toy basket',-1.8,0.9),('D4','Toy / seam',-1.6,1.06),('D5','Key inside toy',-1.35,1.27),('D6','Workshop gate',3.1,2.7)]},
'P02': {'title':'P02  |  WORKSHOP  |  Medium','caption':'Use key -> install 6-tooth gear -> crank -> map right','n':[('W1','Door / keyhole',0,-2.8),('W2','Note / diagram',2.4,2.8),('W3','Small gear (6 teeth)',-1.5,0.55),('W4','Large gear (10 teeth)',-0.65,0.55),('W5','Gear socket',0.35,0.8),('W6','Crank',1.3,0.75),('W7','Clock: hand to 3',0,2.85),('W8','Map: right tower',2.6,1.15)]},
'P03': {'title':'P03  |  CLOCK TOWER  |  Hard','caption':'Lamp center + wheel at 90 deg -> shadow -> secret panel','n':[('T1','Lamp rail',0,-1.2),('T2','Lamp starts at x -1.6',-1.6,-1.2),('T3','Stencil wheel',0,0.9),('T4','Fixed star mark',0,1.3),('T5','Shadow on rear wall',0,2.85),('T6','Secret wall panel',2.25,2.82),('T7','Decorative lever',-3.2,1.3)]}}

W,H=1530,1110
X0,X1=122,902
Y0,Y1=207,822
R=(X1-X0)/8
SZ=(Y1-Y0)/6
xy=lambda x,z:(round(X0+(x+4)*R),round(Y1-(z+3)*SZ))

def arrow(dr,points,fill,width=6):
    dr.line(points, fill=fill, width=width,joint='curve')
    x1,y1=points[-2]; x2,y2=points[-1]
    a=math.atan2(y2-y1,x2-x1)
    r=16; b=0.54
    p=[(x2,y2),(x2-r*math.cos(a-b),y2-r*math.sin(a-b)),(x2-r*math.cos(a+b),y2-r*math.sin(a+b))]
    dr.polygon(p,fill=fill)

def marker(d,id,name,x,z,kind=None):
    cx,cy=xy(x,z)
    clr=COL['blue'] if id[0] in 'KD' else COL['violet'] if id[0]=='W' else COL['teal']
    if 'Key' in name or 'Secret' in name or id=='K4':clr=COL['gold']
    d.ellipse((cx-23,cy-23,cx+23,cy+23),fill=clr,outline='white',width=4)
    bb=d.textbbox((0,0),id,font=font(20,True)); tw=bb[2]-bb[0]
    d.text((cx-tw/2,cy-12),id,font=font(20,True),fill='#FFFFFF')

for pid,p in scene.items():
    im=Image.new('RGB',(W,H),'#FCFAF6'); d=ImageDraw.Draw(im)
    d.rounded_rectangle((45,38,1484,1010),radius=30,fill='white',outline='#DDD5CB',width=3)
    d.text((95,70),p['title'],font=font(45,True),fill=COL['navy'])
    d.text((95,129),p['caption'],font=font(27),fill='#647087')
    d.rounded_rectangle((X0-6,Y0-6,X1+6,Y1+6),radius=9,fill='#E9F0E6',outline='#B9CEBF',width=3)
    # 1m grid
    for i in range(-4,5):
        xp=xy(i,0)[0];d.line([(xp,Y0),(xp,Y1)],fill='#CADBCF',width=1)
        d.text((xp-10,Y1+14),f'{i}',font=font(19),fill='#65756C')
    for i in range(-3,4):
        yp=xy(0,i)[1];d.line([(X0,yp),(X1,yp)],fill='#CADBCF',width=1)
        d.text((X0-32,yp-12),f'{i}',font=font(19),fill='#65756C')
    d.text((455,865),'X  (right +)',font=font(23,True),fill=COL['navy'])
    d.text((140,181),'BACK WALL   (Z +)',font=font(23,True),fill=COL['navy'])
    d.text((140,900),'FRONT / CAMERA  (Z -)',font=font(23,True),fill=COL['navy'])
    d.text((58,555),'Z',font=font(28,True),fill=COL['navy'])

    # 2d furnishings and visual paths
    if pid=='P00':
        a=xy(-3,0.3);b=xy(-1.0,1.7)
        d.rounded_rectangle((a[0],b[1],b[0],a[1]),radius=20,fill='#E5C5A0',outline='#AD8A64',width=3)
        arrow(d,[xy(-1.4,-.2),xy(-.4,.1),xy(.4,.5),xy(1.2,1.),xy(2.3,1.7)],'#9B7C66',5)
        d.rectangle((*xy(2.45,2.95),*xy(3.6,2.6)),fill='#BED8EC')
    elif pid=='P01':
        cx,cy=xy(-1.8,.9); d.ellipse((cx-65,cy-45,cx+65,cy+45),fill='#E6CB9D',outline='#AB8055',width=4)
        cx,cy=xy(2.3,1.6);d.rounded_rectangle((cx-85,cy-60,cx+70,cy+65),radius=18,fill='#DBC6A0',outline='#9C7953',width=3)
        arrow(d,[xy(-1.8,-.45),xy(-.6,-.45)],COL['gold'],8)
    elif pid=='P02':
        a=xy(-2.1,1.1);b=xy(1.6,0.1)
        d.rounded_rectangle((a[0],a[1],b[0],b[1]),radius=15,fill='#E8D3BD',outline=COL['brown'],width=4)
        d.rounded_rectangle((xy(2.0,1.75)[0],xy(2.0,1.75)[1],xy(3.25,.55)[0],xy(3.25,.55)[1]),radius=12,fill='#F2E9CD',outline='#B4A884',width=3)
        arrow(d,[xy(-1.4,.55),xy(.35,.8)],COL['gold'],5)
        arrow(d,[xy(.35,.8),xy(1.3,.75)],COL['gold'],4)
    elif pid=='P03':
        a=xy(-1.6,-1.2);b=xy(1.6,-1.2)
        d.line((a,b),fill=COL['brown'],width=12)
        for x in [-1.6,0,1.6]:
            cx,cy=xy(x,-1.2);d.ellipse((cx-11,cy-11,cx+11,cy+11),fill=COL['gold'])
        arrow(d,[xy(-1.6,-1.2),xy(0,-1.2)],COL['gold'],6)
        arrow(d,[xy(0,-1.2),xy(0,.9),xy(0,2.65),xy(2.1,2.65)],'#D6A44C',5)
        cx,cy=xy(0,.9); d.ellipse((cx-40,cy-40,cx+40,cy+40),outline=COL['violet'],width=7)
        c=xy(2.25,2.82);d.rectangle((c[0]-50,c[1]-16,c[0]+50,c[1]+16),outline=COL['rose'],width=6)
    # rear wall thick border
    d.line([(X0,Y0),(X1,Y0)],fill='#8C958C',width=8)
    # markers; nested toy parts appear as labelled callouts around the basket
    for code,name,x,z in p['n']:
        if pid=='P01' and code in ('D4','D5'):
            newx,newz=(-2.7,1.85) if code=='D4' else (-.75,1.85)
            d.line((xy(newx,newz),xy(-1.8,.9)),fill='#B68C5D',width=3)
            marker(d,code,name,newx,newz)
        elif pid=='P03' and code=='T4':
            newx,newz=(.85,1.55)
            d.line((xy(newx,newz),xy(0,.9)),fill='#B68C5D',width=3)
            marker(d,code,name,newx,newz)
        else:
            marker(d,code,name,x,z)
    # legend
    lx=957; d.text((lx,207),'OBJECT / HOTSPOT KEY',font=font(28,True),fill=COL['navy'])
    d.line((lx,254,1430,254),fill='#D8D3CD',width=2)
    yy=275
    for code,name,x,z in p['n']:
        clr=COL['blue'] if code[0] in 'KD' else COL['violet'] if code[0]=='W' else COL['teal']
        d.rounded_rectangle((lx,yy,lx+67,yy+38),radius=12,fill=clr)
        d.text((lx+12,yy+5),code,font=font(23,True),fill='white')
        # wrap name
        words=name.split(); chunks=[];curr=''
        for wd in words:
            if len(curr+' '+wd)>25:
                chunks.append(curr);curr=wd
            else: curr=(curr+' '+wd).strip()
        if curr:chunks.append(curr)
        for k,chunk in enumerate(chunks):
            d.text((lx+82,yy+3+k*25),chunk,font=font(22),fill=COL['ink'])
        yy+=75 if len(chunks)<2 else 93
    d.rounded_rectangle((95,950,1430,988),radius=10,fill='#F3EEE6')
    d.text((112,959),'SCHEMATIC TOP VIEW  |  Positions in Unity meters  |  Labels correspond to specification tables',font=font(22),fill=COL['navy'])
    fn={'P00':'P00-kitchen.png','P01':'P01-doghouse.png','P02':'P02-workshop.png','P03':'P03-clocktower.png'}[pid]
    im.save(os.path.join(OUT,fn))

# JSON built from deterministic level data (schema for implementation, not executable Unity code)
level_data={
 'project':'Havrakah', 'version':'1.0', 'coordinateUnit':'unity_meter', 'axis':'x right; y up; z toward rear wall',
 'timer':{'starts':'press StartPuzzle; reveal scene', 'stops':'solve', 'pauses':['PauseOverlay','HintOverlay','ApplicationBackground'], 'replayLeaderboard':'first_solve_only'},
 'scenes':[
 {'id':'P00','name':'Kitchen','category':'tutorial','preconditions':[], 'objects':[
 {'id':'K_CakeStand','position':[-2,.95,1.1],'action':'tap','effect':'cakeSeen=true'},
 {'id':'K_PawTrail','position':[.2,.02,.15],'action':'tap','effect':'tracksSeen=true'},
 {'id':'K_Dog','position':[2.5,0,1.9],'action':'tap','effect':'focus K_Tag'},
 {'id':'K_Tag','localPosition':[0,.8,-.1],'parent':'K_Dog','action':'rotate180','effect':'tagFrostSeen=true'},
 {'id':'K_Window','position':[-2.8,1.5,2.8],'action':'tap','effect':'show ClosedWindowText'},
 {'id':'K_Door','position':[2.8,0,2.8],'action':'locked until solve'}],
 'completion':'tracksSeen && tagFrostSeen && selectedAnswer == DOG','destination':'P01','hints':['בדקי גם את הרצפה','למי יכולים להשתייך סימני הכפות?','אפשר לבדוק גם את הצד השני של התליון']},
 {'id':'P01','name':'Doghouse','category':'easy','preconditions':['P00Solved'],'objects':[
 {'id':'D_Dog','position':[2.3,0,1.6],'action':'tap','effect':'look at basket'},
 {'id':'D_Bowl','position':[-1.8,.2,-.45],'action':'dragX','snapX':-.6,'effect':'bowlMoved=true'},
 {'id':'D_Basket','position':[-1.8,0,.9],'action':'tap','requires':'bowlMoved','effect':'focus D_Toy'},
 {'id':'D_Toy','localPosition':[-.15,.35,0],'parent':'D_Basket','action':'rotate180','effect':'seamVisible=true'},
 {'id':'D_ToySeam','parent':'D_Toy','action':'dragDown80Pixels','requires':'seamVisible','effect':'seamOpened=true'},
 {'id':'D_Key','parent':'D_Toy','action':'tapCollect','requires':'seamOpened','effect':'keyCollected=true'},
 {'id':'D_WorkshopGate','position':[3.1,0,2.7],'action':'locked until solve'}],
 'completion':'bowlMoved && seamVisible && seamOpened && keyCollected','destination':'P02','hints':['הכלב מסתכל על משהו ליד הקערה','אולי יש משהו שמסתתר מאחורי הקערה','הצעצוע מצלצל; אפשר להפוך אותו ולבדוק את התפר']},
 {'id':'P02','name':'Workshop','category':'medium','preconditions':['P01Solved','inventory key'],'objects':[
 {'id':'W_Door','position':[0,0,-2.8],'action':'opens after W_Lock'},
 {'id':'W_Lock','position':[.65,1,-2.75],'action':'drop key','effect':'doorOpen=true; consume key'},
 {'id':'W_Note','position':[2.4,1.45,2.8],'action':'tap','effect':'noteRead=true'},
 {'id':'W_SmallGear','position':[-1.5,1.05,.55],'action':'dragTo W_GearSocket','effect':'smallGearInstalled=true'},
 {'id':'W_LargeGear','position':[-.65,1.05,.55],'action':'dragTo W_GearSocket','effect':'return to tray'},
 {'id':'W_GearSocket','position':[.35,1.12,.8],'action':'accept small gear only'},
 {'id':'W_Crank','position':[1.3,1,.75],'action':'rotateClockwise90','requires':'smallGearInstalled','effect':'clockActivated=true'},
 {'id':'W_Clock','position':[0,1.85,2.85],'action':'tap','effect':'show hand pointing 3 after activation'},
 {'id':'W_Map','position':[2.6,1.1,1.15],'action':'choose among Fountain,Bakery,ClockTower','requires':'clockActivated','effect':'mapChoice=chosen'}],
 'completion':'doorOpen && smallGearInstalled && clockActivated && mapChoice == CLOCK_TOWER','destination':'P03','reward':'notebook lamp-center star-up schematic','hints':['הידית לא עובדת כי חסר חלק','השווי בין מספר השיניים של התושבת לגלגלים','מה אומר מחוג שמצביע ימינה על המפה?']},
 {'id':'P03','name':'ClockTower','category':'hard','preconditions':['P02Solved','notebook schematic'],'objects':[
 {'id':'T_LampRail','position':[0,.8,-1.2],'action':'rail with slots -1.6,0,1.6'},
 {'id':'T_Lamp','position':[-1.6,1.05,-1.2],'action':'dragOnRail','snapX':[-1.6,0,1.6],'effect':'lampSlot CENTER only if x=0'},
 {'id':'T_StencilWheel','position':[0,1.45,.9],'action':'rotateSnap','snapDegrees':[0,90,180,270],'effect':'wheelAngle=value'},
 {'id':'T_TowerMark','position':[0,2.25,1],'action':'static clue star at 12 oclock'},
 {'id':'T_ArchiveNote','action':'openNotebook','effect':'show previous schematic'},
 {'id':'T_ShadowWall','position':[0,1.5,2.85],'action':'tap when shadow visible','effect':'shadowSeen=true'},
 {'id':'T_SecretPanel','position':[2.25,1.2,2.82],'action':'tap','requires':'lampSlot == CENTER && wheelAngle == 90 && shadowSeen','effect':'secretPanelOpened=true'},
 {'id':'T_DecorLever','position':[-3.2,1.3,1.3],'action':'tap','effect':'feedback only'}],
 'completion':'lampSlot == CENTER && wheelAngle == 90 && shadowSeen && secretPanelOpened','destination':'ChapterComplete','hints':['חזרי לשרטוט שמצאת בסדנה','בדקי את שלוש נקודות העצירה של הפנס','הכוכב שעל הגלגל צריך להצביע אל הכוכב הקבוע']}
 ]
}
with open(f'{ROOT}/data/puzzle-data.json','w',encoding='utf-8') as f:json.dump(level_data,f,ensure_ascii=False,indent=2)
print('Created:',[(os.path.basename(x),os.path.getsize(os.path.join(OUT,x))) for x in os.listdir(OUT)])
