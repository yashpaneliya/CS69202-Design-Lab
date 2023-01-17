
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CLOSEABBR CLOSEDATA CLOSEFINAL CLOSEHEADER CLOSEHREF CLOSELIST CLOSEPOINTTABLE CLOSEROW CONTENT FRIGHTDIV GARBAGE OPENABBR OPENDATA OPENFINAL OPENHEADER OPENHREF OPENLINK OPENLIST OPENMATCHDIV OPENPOINTTABLE OPENROW OPENTABLE SEPARATORstart : before OPENFINAL skip SEPARATOR handlematches CLOSEFINALhandlematches : skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches\n    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches\n    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails\n    | skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches\n    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches\n    | OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails\n    |handlescorer : skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer\n    |handlepenscorer : skip OPENLIST CONTENT OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlepenscorer\n    |handledetails : OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT OPENHREF CONTENT CLOSEHREF skipbefore : CONTENT before\n    | OPENHREF before\n    | CLOSEHREF before\n    | OPENHEADER before\n    | CLOSEHEADER before\n    | OPENDATA before\n    | CLOSEDATA before\n    | OPENROW before\n    | CLOSEROW before\n    | OPENLIST before\n    | CLOSELIST before\n    | OPENTABLE before\n    | OPENLINK before\n    | CLOSEPOINTTABLE before\n    | OPENMATCHDIV before\n    | FRIGHTDIV before\n    | SEPARATOR before\n    |skip : CONTENT skip\n    | OPENHREF skip\n    | CLOSEHREF skip\n    |'
    
_lr_action_items = {'CONTENT':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,39,40,41,42,48,56,59,60,63,68,71,72,76,78,81,84,86,87,89,92,95,110,113,117,121,124,125,128,132,134,136,140,143,144,147,151,166,170,172,176,178,179,185,191,193,194,198,200,202,206,207,211,215,216,222,228,232,234,236,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,39,39,39,39,39,39,58,61,62,65,70,73,39,39,82,85,88,90,91,93,96,99,39,39,39,39,129,39,39,39,39,39,39,39,39,39,39,171,175,39,181,182,39,188,194,39,197,39,203,205,39,210,39,39,219,225,39,39,39,39,]),'OPENHREF':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,39,40,41,42,48,54,57,66,69,72,76,82,85,88,91,110,113,117,119,121,125,128,132,134,136,140,143,144,147,151,162,165,169,172,173,179,181,193,197,198,206,211,215,219,226,228,230,232,234,236,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,40,40,40,40,40,40,56,59,68,71,40,40,86,89,92,95,40,40,40,124,40,40,40,40,40,40,40,40,40,40,40,166,170,166,40,178,40,185,40,200,40,40,40,40,222,166,40,166,40,40,40,]),'CLOSEHREF':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,39,40,41,42,48,58,61,70,72,73,76,90,93,96,99,110,113,117,121,125,128,129,132,134,136,140,143,144,147,151,171,172,175,179,182,188,193,198,203,206,211,215,225,228,232,234,236,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,41,41,41,41,41,41,60,63,72,41,76,41,94,97,100,103,41,41,41,41,41,41,134,41,41,41,41,41,41,41,41,176,41,180,41,186,191,41,41,206,41,41,41,228,41,41,41,41,]),'OPENHEADER':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,52,55,64,67,75,77,80,83,161,168,199,204,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,54,57,66,69,78,81,84,87,165,173,202,207,]),'CLOSEHEADER':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,39,40,41,43,44,45,62,65,72,74,76,79,94,97,100,103,180,186,205,210,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,-35,-35,-35,-32,-33,-34,64,67,75,77,80,83,98,101,104,107,184,189,208,212,]),'OPENDATA':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,106,109,112,116,120,123,127,131,135,138,142,146,190,195,208,212,],[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,110,113,117,121,125,128,132,136,140,143,147,151,193,198,211,215,]),'CLOSEDATA':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,39,40,41,43,44,45,110,113,115,117,118,121,122,125,126,128,130,132,133,136,137,140,141,143,144,145,147,148,149,151,152,155,193,196,198,201,211,214,215,218,234,237,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,-35,-35,-35,-32,-33,-34,-10,-10,120,-10,123,-10,127,-35,131,-35,135,-35,138,-35,142,-10,146,-10,-10,150,-10,153,-9,-10,156,159,-10,199,-10,204,-12,217,-12,221,-12,-11,]),'OPENROW':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,49,53,102,105,108,111,157,163,187,192,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,52,55,106,109,112,116,161,168,190,195,]),'CLOSEROW':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,98,101,104,107,150,153,156,159,184,189,217,221,],[12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,102,105,108,111,154,157,160,163,187,192,220,224,]),'OPENLIST':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,39,40,41,43,44,45,110,113,114,117,121,140,143,144,147,151,193,198,211,213,215,234,],[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-35,-35,-35,-32,-33,-34,-35,-35,119,-35,-35,-35,-35,-35,-35,-35,-35,-35,-35,216,-35,-35,]),'CLOSELIST':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,39,40,41,43,44,45,134,139,228,231,],[14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-35,-35,-35,-32,-33,-34,-35,144,-35,234,]),'OPENTABLE':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,39,40,41,42,43,44,45,46,48,51,172,179,232,236,],[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-35,-35,-35,-35,-32,-33,-34,49,-35,53,-35,-35,-35,-35,]),'OPENLINK':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,],[16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,]),'CLOSEPOINTTABLE':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,154,160,220,224,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,158,164,223,227,]),'OPENMATCHDIV':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,42,172,179,232,236,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,48,48,48,48,48,]),'FRIGHTDIV':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,158,164,223,227,],[19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,162,169,226,230,]),'SEPARATOR':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,38,39,40,41,43,44,45,167,174,206,209,229,233,],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,-35,42,-35,-35,-35,-32,-33,-34,172,179,-35,-13,232,236,]),'OPENFINAL':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,],[-31,20,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-31,-30,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,]),'$end':([1,50,],[0,-1,]),'CLOSEFINAL':([39,40,41,42,43,44,45,47,172,174,177,179,183,206,209,232,233,235,236,238,],[-35,-35,-35,-8,-32,-33,-34,50,-8,-4,-2,-8,-3,-35,-13,-8,-7,-5,-8,-6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'before':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,],[2,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,]),'skip':([20,39,40,41,42,48,72,76,110,113,117,121,125,128,132,134,136,140,143,144,147,151,172,179,193,198,206,211,215,228,232,234,236,],[38,43,44,45,46,51,74,79,114,114,114,114,130,133,137,139,141,114,114,114,114,114,46,46,114,114,209,213,213,231,46,213,46,]),'handlematches':([42,172,179,232,236,],[47,177,183,235,238,]),'handlescorer':([110,113,117,121,140,143,144,147,151,193,198,],[115,118,122,126,145,148,149,152,155,196,201,]),'handledetails':([162,169,226,230,],[167,174,229,233,]),'handlepenscorer':([211,215,234,],[214,218,237,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> before OPENFINAL skip SEPARATOR handlematches CLOSEFINAL','start',6,'p_start','finals.py',152),
  ('handlematches -> skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches','handlematches',37,'p_handlematches','finals.py',156),
  ('handlematches -> OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches','handlematches',38,'p_handlematches','finals.py',157),
  ('handlematches -> OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails','handlematches',36,'p_handlematches','finals.py',158),
  ('handlematches -> skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches','handlematches',56,'p_handlematches','finals.py',159),
  ('handlematches -> OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails SEPARATOR handlematches','handlematches',57,'p_handlematches','finals.py',160),
  ('handlematches -> OPENMATCHDIV skip OPENTABLE OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENHEADER OPENHREF CONTENT CLOSEHREF skip CLOSEHEADER OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENDATA skip CLOSEDATA OPENDATA handlescorer CLOSEDATA CLOSEROW OPENROW OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER CLOSEROW OPENROW OPENDATA handlescorer CLOSEDATA OPENHEADER CONTENT CLOSEHEADER OPENDATA handlepenscorer CLOSEDATA CLOSEROW CLOSEPOINTTABLE FRIGHTDIV handledetails','handlematches',55,'p_handlematches','finals.py',161),
  ('handlematches -> <empty>','handlematches',0,'p_handlematches','finals.py',162),
  ('handlescorer -> skip OPENLIST OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlescorer','handlescorer',8,'p_handlescorer','finals.py',170),
  ('handlescorer -> <empty>','handlescorer',0,'p_handlescorer','finals.py',171),
  ('handlepenscorer -> skip OPENLIST CONTENT OPENHREF CONTENT CLOSEHREF skip CLOSELIST handlepenscorer','handlepenscorer',9,'p_handlepenscorer','finals.py',177),
  ('handlepenscorer -> <empty>','handlepenscorer',0,'p_handlepenscorer','finals.py',178),
  ('handledetails -> OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT OPENHREF CONTENT CLOSEHREF skip','handledetails',13,'p_handledetails','finals.py',184),
  ('before -> CONTENT before','before',2,'p_before','finals.py',191),
  ('before -> OPENHREF before','before',2,'p_before','finals.py',192),
  ('before -> CLOSEHREF before','before',2,'p_before','finals.py',193),
  ('before -> OPENHEADER before','before',2,'p_before','finals.py',194),
  ('before -> CLOSEHEADER before','before',2,'p_before','finals.py',195),
  ('before -> OPENDATA before','before',2,'p_before','finals.py',196),
  ('before -> CLOSEDATA before','before',2,'p_before','finals.py',197),
  ('before -> OPENROW before','before',2,'p_before','finals.py',198),
  ('before -> CLOSEROW before','before',2,'p_before','finals.py',199),
  ('before -> OPENLIST before','before',2,'p_before','finals.py',200),
  ('before -> CLOSELIST before','before',2,'p_before','finals.py',201),
  ('before -> OPENTABLE before','before',2,'p_before','finals.py',202),
  ('before -> OPENLINK before','before',2,'p_before','finals.py',203),
  ('before -> CLOSEPOINTTABLE before','before',2,'p_before','finals.py',204),
  ('before -> OPENMATCHDIV before','before',2,'p_before','finals.py',205),
  ('before -> FRIGHTDIV before','before',2,'p_before','finals.py',206),
  ('before -> SEPARATOR before','before',2,'p_before','finals.py',207),
  ('before -> <empty>','before',0,'p_before','finals.py',208),
  ('skip -> CONTENT skip','skip',2,'p_skip','finals.py',212),
  ('skip -> OPENHREF skip','skip',2,'p_skip','finals.py',213),
  ('skip -> CLOSEHREF skip','skip',2,'p_skip','finals.py',214),
  ('skip -> <empty>','skip',0,'p_skip','finals.py',215),
]
