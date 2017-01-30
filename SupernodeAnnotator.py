import ast

from labelannotator import *
import re

def GrididExists(row_dict):
  if row_dict['gridid']:
    return True
  else:
    return False

def PriorityMap(in_fields, out_field):
  def annotate_fn(row_dict):
    for in_field in in_fields:
      if in_field in row_dict and row_dict[in_field]:
        return {out_field: row_dict[in_field]}
    return {}

  return annotate_fn

def BackgroundColor(row_dict):
  if row_dict['cost']:
    return {'bg_color': '#FFC0C0'}
  return {'bg_color': '#FFFFFF'}

def ColoredPackage(row_dict):
  if not row_dict['parametrics']:
    return {'dippack': '', 'pack': row_dict['package']}

  parametrics = ast.literal_eval(row_dict['parametrics'])
  if (('Mounting Type' in parametrics and parametrics['Mounting Type'].find('Through Hole') >= 0) or
      (re.match(".*DIP$", row_dict['package'])) or
  (re.match("Axial", row_dict['package']))):
    return {'dippack': row_dict['package'], 'pack': ''}
  else:
    return {'dippack': '', 'pack': row_dict['package']}

load() \
    .filter(GrididExists) \
    .map_append(PriorityMap(['manual_title', 'dist_title'], 'title')) \
    .map_append(PriorityMap(['manual_package', 'dist_package'], 'package')) \
    .map_append(PriorityMap(['manual_quickdesc', 'dist_quickdesc'], 'quickdesc')) \
    .map_append(PriorityMap(['manual_mfrpn', 'dist_mfrpn'], 'mfrpn')) \
    .map_append(PriorityMap(['manual_desc', 'dist_desc'], 'desc')) \
    .map_append(BackgroundColor) \
    .map_append(ColoredPackage) \
    .write()
