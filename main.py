# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2023 lanneq-dev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####


bl_info = {
    "name": "ProCutter",
    "author": "Ruslan Nurgaleev / Lanneq-dev",
    "version": (1, 0, 2),
    "blender": (2, 93, 0),
    "location": "View 3D > Tool Shelf > ProCutter",
    "description": "ProCutter is intended for optimizing rectangular nesting.",
    "warning": "Work with Astra R-Nesting and optiCutter",
    "wiki_url": "https://github.com/Lanneq/ProCutter",
    "tracker_url": "https://github.com/Lanneq/ProCutter/issues",
    "category": "3D View"}

import os
import re
import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.utils import register_class, unregister_class
import csv
import webbrowser
from bpy.types import AddonPreferences

def astra():
    def console_get():
        for area in bpy.context.screen.areas:
            if area.type == 'CONSOLE':
                for space in area.spaces:
                    if space.type == 'CONSOLE':
                        return area, space
        return None, None

    def console_write(text):
        area, space = console_get()
        if space is None:
            return
        context = bpy.context.copy()
        context.update(dict(
            space=space,
            area=area,
        ))
        for line in text.split("\n"):
            bpy.ops.console.scrollback_append(context, text=line, type='OUTPUT')

    selection = bpy.context.selected_objects
    result = ''
    go = ''
    result_csv = ''
    rot = 'y'
    count = 0
    i = 0

    # i=25.4 if max have no mm. i=1, when max file correct
    converting = 1
    result_csv = ''
    
    
    for sel in selection:
        dims = sel.dimensions * 1000 / converting
        
        min_detail_size = 30

        X = dims.x
        Y = dims.y
        Z = dims.z

        obj_name = sel.name

        try:
            mat_name = sel.active_material.name
        except:
            mat_name = "No material"

        mat_type = ''

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        rot = re.compile('@')  # sel.name
        match1 = rot.search(sel.name)

        rot2 = re.compile('#')  # sel.name
        match2 = rot2.search(sel.name)


        if (X < Y < Z) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Z, Y)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Z, Y)
                count += 1

        if (X < Z < Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Z, Y)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Z, Y)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1

        if (X < Z == Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, X, Y, Z)
                count += 1

        if (Y < X < Z) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, Z, X)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, Z, X)
                count += 1

        if (Y < Z < X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, Z, X)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, Z, X)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1

        if (Y < Z == X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Y, X, Z)
                count += 1

        if (Z < X < Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, Y, X)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, Y, X)
                count += 1

        if (Z < Y < X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, Y, X)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, Y, X)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1

        if (Z < Y == X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                    count += 1
                    continue
                result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
                count += 1

        if (Z == Y == X):
            result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f; %.0f\n" % (mat_name, obj_name, Z, X, Y)
            count += 1

    console_write(result)
    os.startfile(bpy.context.scene.my_tool.astra_path)

    path = bpy.context.scene.my_tool.save_path
    os.makedirs(path, exist_ok=True)
    with open(path + "astra.txt", "w") as file:
        file.write(result)


def exceptions():
    for material in bpy.data.materials:
        try:
            pass
        except(TypeError):
            print("Type Errrrror")


def opticutter():
    def console_get():
        for area in bpy.context.screen.areas:
            if area.type == 'CONSOLE':
                for space in area.spaces:
                    if space.type == 'CONSOLE':
                        return area, space
        return None, None

    def console_write(text):
        area, space = console_get()
        if space is None:
            return
        context = bpy.context.copy()
        context.update(dict(
            space=space,
            area=area,
        ))
        for line in text.split("\n"):
            bpy.ops.console.scrollback_append(context, text=line, type='OUTPUT')

    selection = bpy.context.selected_objects
    result = ''
    go = ''
    result_csv = ''
    rot = 'y'
    count = 0
    i = 0

    # i=25.4 if max have no mm. i=1, when max file correct
    converting = 1

    result_csv = ''

    for sel in selection:
        dims = sel.dimensions * 1000 / converting

        min_detail_size = 30

        X = dims.x
        Y = dims.y
        Z = dims.z

        obj_name = sel.name

        try:
            mat_name = sel.active_material.name
        except:
            mat_name = "No material"

        mat_type = ''

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        rot = re.compile('@')  # sel.name
        match1 = rot.search(sel.name)

        rot2 = re.compile('#')  # sel.name
        match2 = rot2.search(sel.name)

        if (X < Y < Z) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (Z, Y, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (Z, Y, obj_name) + ",y\n"
                count += 1

        if (X < Z < Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (Z, Y, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (Z, Y, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",y\n"
                count += 1

        if (X < Z == Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (Y, Z, obj_name) + ",y\n"
                count += 1

        if (Y < X < Z) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                result += "0; 1; " + mat_type + "%s; %s; %.0f; %.0f\n" % (mat_name, obj_name, X, Z)
                go += "P," + "%.0f, %.0f,1, %s" % (Z, X, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (Z, X, obj_name) + ",y\n"
                count += 1

        if (Y < Z < X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (Z, X, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (Z, X, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",y\n"
                count += 1

        if (Y < Z == X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    result += "1; 1; " + mat_type + "%s; %s; %.0f; %.0f\n" % (mat_name, obj_name, Z, X)
                    go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (X, Z, obj_name) + ",y\n"
                count += 1

        if (Z < X < Y) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (Y, X, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (Y, X, obj_name) + ",y\n"
                count += 1

        if (Z < Y < X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                    Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (Y, X, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (Y, X, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",y\n"
                count += 1

        if (Z < Y == X) and ((X and Y >= min_detail_size and Z >= min_detail_size) or (
                Y and X >= min_detail_size and Z >= min_detail_size) or (
                                     Z and X >= min_detail_size and Y >= min_detail_size)):
            if (match1 != None) and (match2 != None):
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",\n"
                count += 1
                continue
            if match2 != None:
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",\n"
                count += 1
            else:
                if match1 != None:
                    go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",y\n"
                    count += 1
                    continue
                go += "P," + "%.0f, %.0f,1, %s" % (X, Y, obj_name) + ",\n"
                count += 1

    result_csv = 'N,Blender\n' + 'M,MDF\n' + '@,Length,Width,Quantity\n' + 'S,2750,1830,1000\n' + 'K,4\n' + '@,Length,Width,Quantity,Label,Can turn\n' + str(
        go)

    console_write(result_csv)

    path = bpy.context.scene.my_tool.save_path
    os.makedirs(path, exist_ok=True)
    with open(path + "opticutter.csv", "w") as file:
        file.write(result_csv)

    webbrowser.open('https://www.opticutter.com/import2d/csv')


def reset_all():
    selection = bpy.context.selected_objects
    for sel in selection:
        res = re.compile(r"#")
        res2 = re.compile(r"@")
        match = res.search(sel.name)
        match2 = res2.search(sel.name)

        if match != None or match2 != None:
            sel.name = sel.name.replace('#', '')
            sel.name = sel.name.replace('@', '')
        sel.show_name = True


def rotate():
    selection = bpy.context.selected_objects
    for sel in selection:
        res = re.compile(r"#")
        res2 = re.compile(r"@")
        match = res.search(sel.name)
        match2 = res2.search(sel.name)

        if match != None and match2 != None:
            sel.name = sel.name.replace('@', '')
            sel.name = sel.name.replace('#', '')
            continue
        if match != None and match2 == None:
            sel.name = sel.name.replace('@', '')
            sel.name = sel.name.replace('#', '')
            sel.name = "#@" + str(sel.name)
        if match == None and match2 != None:
            sel.name = sel.name.replace('@', '')
            sel.name = sel.name.replace('#', '')
            sel.name = "#@" + str(sel.name)
        else:
            sel.name = sel.name.replace('@', '')
            sel.name = sel.name.replace('#', '')
            sel.name = "#@" + str(sel.name)
        sel.show_name = True


def fix():
    selection = bpy.context.selected_objects
    for sel in selection:
        res = re.compile(r"#")
        res2 = re.compile(r"@")
        match = res.search(sel.name)
        match2 = res2.search(sel.name)

        if match != None:
            sel.name = sel.name.replace('#', '')
            sel.name = sel.name.replace('@', '')
            if match != None and match2 != None:
                sel.name = sel.name.replace('@', '')
                sel.name = "#" + str(sel.name)
        else:
            sel.name = "#" + str(sel.name)
        sel.show_name = True


def remove_unused_slots():
    selection = bpy.context.selected_objects
    for sel in selection:
        bpy.ops.object.material_slot_remove_unused()


def hide_name():
    selection = bpy.context.selected_objects
    for sel in selection:
        sel.show_name = False


def show_name():
    selection = bpy.context.selected_objects
    for sel in selection:
        sel.show_name = True


def group_rename():
    selection = bpy.context.selected_objects
    for sel in selection:
        bpy.ops.object.make_links_data(type='MATERIAL')


class Reset_all(bpy.types.Operator):
    bl_idname = "reset.func"
    bl_label = "Reset all"

    def execute(self, context):
        reset_all()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}

class Rotate(bpy.types.Operator):
    bl_idname = "rotate.func"
    bl_label = "Rotate"

    def execute(self, context):
        rotate()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Fix(bpy.types.Operator):
    bl_idname = "fix.func"
    bl_label = "Fix"

    def execute(self, context):
        fix()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Remove_Unused_Slots(bpy.types.Operator):
    bl_idname = "remove_unused_slots.func"
    bl_label = "Remove_Unused_Slots"

    def execute(self, context):
        remove_unused_slots()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Show_Name(bpy.types.Operator):
    bl_idname = "show_name.func"
    bl_label = "Show Name"

    def execute(self, context):
        show_name()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Hide_Name(bpy.types.Operator):
    bl_idname = "hide_name.func"
    bl_label = "Hide Name"

    def execute(self, context):
        hide_name()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Group_Rename(bpy.types.Operator):
    bl_idname = "group_rename.func"
    bl_label = "Group Rename"
    
    def execute(self, context):
        group_rename()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class Astra(bpy.types.Operator):
    bl_idname = "astra.func"
    bl_label = "Exporter_Astra"
    bl_description = "Make and Export *.txt file for Astra R-Nesting and run Astra"

    def execute(self, context):
        astra()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class OptiCutter(bpy.types.Operator):
    bl_idname = "opticutter.func"
    bl_label = "Exporter_Astra"
    bl_description = "Make *.csv file and export to https://www.opticutter.com for cutting"

    def execute(self, context):
        opticutter()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


def rename_all():
    selection = bpy.context.selected_objects
    for sel in selection:
        sel.name = bpy.context.scene.rename_all.rename_sel


class RenameSel(bpy.types.Operator):
    bl_idname = "rename_all.func"
    bl_label = "Rename All"
    bl_description = "Rename all selected objects"

    def execute(self, context):
        rename_all()
        self.report({'INFO'}, 'This is %s' % self.bl_idname)
        return {'FINISHED'}


class MyProperties(bpy.types.PropertyGroup):
    astra_path : bpy.props.StringProperty(name="Astra path:", default="C:\Program Files (x86)\Astra R-Nesting\Astra.exe")
    save_path : bpy.props.StringProperty(name="Export path:", default="C:/tmp/")
    rename_sel : bpy.props.StringProperty(name="")

class IV_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Download Astra R-Nesting")
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "astra_path")
        row.scale_x = 0.5
        row.operator("wm.url_open", text="En", icon='URL').url = "http://www.astranest.com/"
        row.operator("wm.url_open", text="Ru", icon='URL').url = "http://astrapro.ru/default.asp?page=astra-raskroj"

        row = layout.row()
        scene = context.scene
        mytool = scene.my_tool
        layout.prop(mytool, "save_path")

        row = layout.row()
        row.label(text="DATA ORDER PRIORITY: Rotate | Quantity | Material | Name | Thickness | Length | Width ")


class EXAMPLE_PT_panel(bpy.types.Panel):
    bl_label = "ProCutter"
    bl_category = "Item"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        obj = context.object
        layout = self.layout

        row = layout.row()
        
        row = layout.row()
        row.scale_y = 1.4
        row.operator(Rotate.bl_idname, icon='CON_ROTLIMIT', text="ROTATE")

        row.scale_y = 1.4
        row.operator(Fix.bl_idname, icon='CON_LOCLIMIT', text="FIX")

        row = layout.row()
        row.scale_y = 1.0
        row.operator(Reset_all.bl_idname, icon="FILE_REFRESH", text='RESET fix and rotate')
        row = layout.row()

        row = layout.row()
        row.scale_y = 1.4
        row.operator(Hide_Name.bl_idname, text='Hide names', icon='HIDE_ON')
        row.operator(Show_Name.bl_idname, text='Show names', icon='HIDE_OFF')
 
        row = layout.row()
   
        try:
            row.label(text="Change Material for Selected")
            row = layout.row()
            row.prop(obj, "active_material", text='')
            row.scale_x = 0.35
            row.operator(Group_Rename.bl_idname, text='Apply')
        except:
            row = layout.row()

        row = layout.row()
        row.scale_y = 1.2
        row.operator(Remove_Unused_Slots.bl_idname, icon='ANCHOR_TOP', text="Remove unused slots")
        row = layout.row()

        row = layout.row()
        scene = context.scene
        mytool = scene.rename_all
        layout.prop(mytool, "rename_sel")
        
        row.label(text="Rename Selected Objects")
        row = layout.row()
        row.operator(RenameSel.bl_idname, text='Rename Selected', icon='SORTALPHA')
        row.scale_y = 1.3
        
        row = layout.row()
        row = layout.row()
        row.label(text="EXPORT TO:")
        row = layout.row()
        row.scale_y = 1.5
        row.operator(Astra.bl_idname, text='ASTRA', icon="UV_SYNC_SELECT")
        row.scale_y = 1.5
        row.operator(OptiCutter.bl_idname, text='WEB', icon="UV_SYNC_SELECT")


classes = (
    MyProperties,
    Astra,
    Reset_all,
    Rotate,
    Fix,
    Remove_Unused_Slots,
    Show_Name,
    Hide_Name,
    Group_Rename,
    OptiCutter,
    EXAMPLE_PT_panel,
    IV_Preferences,
    RenameSel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)
    bpy.types.Scene.rename_all = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_tool
    del bpy.types.Scene.rename_all


if __name__ == "__main__":
    register()
