# ============================================
# 🏺 Hieroglyph Manual Annotator - GUI Version
# ============================================
# Author: Hesham
# Description:
# Interactive GUI tool to zoom, pan, and draw bounding boxes
# for hieroglyph symbol extraction and labeling by Gardiner category.
# ============================================

import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import threading

class HieroglyphAnnotatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏺 Hieroglyph Manual Annotator")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configuration
        self.INPUT_DIR = "Temple_Images"  # Updated to match your folder
        self.OUTPUT_DIR = "dataset_labeled"
        self.SAVE_SIZE = (224, 224)
        
        # Complete Gardiner symbol descriptions
        self.SYMBOL_DESCRIPTIONS = {
            # A. Man and his occupations
            "A1": "Seated man", "A2": "Man with hand to mouth", "A3": "Man sitting on heel", "A4": "Man with arms raised", 
            "A5": "Man hiding", "A5a": "Man hiding (variant)", "A6": "Man purifying", "A6a": "Man purifying (variant)", 
            "A6b": "Man purifying (variant)", "A7": "Fatigued man", "A8": "Man performing hnw", "A9": "Man with basket on head", 
            "A10": "Man holding an oar", "A11": "Man with scepter and crook", "A12": "Man with bow and quiver", 
            "A13": "Man with arms bound", "A14": "Man with bleeding head", "A14a": "Man with axe to head", 
            "A15": "Man falling", "A16": "Man bowing", "A17": "Child with hand to mouth", "A17a": "Child sitting", 
            "A18": "Child wearing red crown", "A19": "Aged man bending with stick", "A20": "Man leaning on forked stick", 
            "A21": "Man with stick", "A22": "Statue of man with stick and scepter", "A23": "King with stick and mace", 
            "A24": "Man striking with stick in both hands", "A25": "Man striking with stick in one hand", 
            "A26": "Man beckoning", "A27": "Man running", "A28": "Man with arms raised", "A29": "Man upside down", 
            "A30": "Man with arms outstretched", "A31": "Man with arms turned behind him", "A32": "Man dancing", 
            "A33": "Man with stick and bundle", "A34": "Man pounding in a mortar", "A35": "Man building a wall", 
            "A36": "Man straining into a vessel", "A37": "Commoner form A36", "A38": "Man holding two animal emblems", 
            "A39": "Man holding two giraffes", "A40": "Seated god", "A40a": "Seated god (variant)", "A41": "Seated king", 
            "A42": "Seated king holding flail", "A42a": "Seated king holding flail (variant)", "A43": "King wearing white crown of Upper Egypt", 
            "A43a": "King wearing white crown (variant)", "A44": "King holding flail and wearing white crown", 
            "A45": "King wearing red crown of Lower Egypt", "A45a": "King wearing red crown (variant)", 
            "A46": "King holding flail and wearing red crown", "A47": "Seated shepherd", "A48": "Man holding knife", 
            "A49": "Foreigner with stick", "A50": "Noble seated on chair", "A51": "Noble seated on chair with flagellum", 
            "A52": "Kneeling noble with flail", "A53": "Upright mummy", "A54": "Recumbent mummy", "A55": "Mummy on bed", 
            "A59": "Man threatening stick with one hand",
            
            # Aa. Unclassified signs  
            "Aa1": "Placenta?", "Aa2": "Pustule or gland?", "Aa3": "Aa2 with substance issuing", "Aa4": "Pot", 
            "Aa5": "Part of ship?", "Aa6": "Unknown", "Aa7": "Unknown", "Aa8": "Irrigation canal?", 
            "Aa9": "Unknown", "Aa10": "Unknown", "Aa11": "Unknown", "Aa12": "Unknown", "Aa13": "Unknown", 
            "Aa14": "Unknown", "Aa15": "Var. Aa13", "Aa16": "Short form Aa13", "Aa17": "Back of something?", 
            "Aa18": "Var. of Aa17", "Aa19": "Unknown", "Aa20": "Unknown", "Aa21": "Unknown", "Aa22": "Combination of Aa21 + D36", 
            "Aa23": "Warp between stakes?", "Aa24": "Var. Aa23", "Aa25": "Unknown", "Aa26": "Unknown", 
            "Aa27": "Unknown", "Aa28": "Builder's tool?", "Aa29": "Var. of Aa28", "Aa30": "Frieze element?", "Aa31": "Var. of Aa30",
            
            # B. Woman and her occupations
            "B1": "Seated Woman", "B2": "Pregnant woman", "B3": "Woman giving birth", "B4": "Var. B3", 
            "B5": "Woman nursing child", "B6": "Woman and seated child", "B7": "Seated queen holding flower",
            
            # C. Anthropomorphic deities
            "C1": "God with sun-disk and uraeus", "C2": "God with falcon head and sun-disk holding ʿnḫ", 
            "C3": "God with ibis head", "C4": "God with ram head", "C5": "God with ram head holding ʿnḫ", 
            "C6": "God with jackal head", "C7": "God with Seth head", "C8": "Min", "C9": "Goddess with horned sun-disk", 
            "C10": "God with feather", "C10a": "Goddess with feather holding ʿnḫ", "C11": "ḥḥ-figure", "C12": "Amun", 
            "C17": "Montu", "C18": "Tatjenen", "C19": "Ptah", "C20": "Variant C19",
            
            # D. Parts of the human body
            "D1": "Head", "D2": "Face", "D3": "Hair", "D4": "Eye", "D5": "Eye with paint", "D6": "Eye with paint", 
            "D7": "Eye with paint", "D8": "Eye enclosed", "D9": "Eye weeping", "D10": "Eye with falcon's head marking", 
            "D11": "White part of w3ḏt eye", "D12": "Eye pupil", "D13": "Eyebrow", "D14": "White part of w3ḏt eye", 
            "D15": "Part of w3ḏt eye markings", "D16": "Part of w3ḏt eye markings", "D17": "Markings of w3ḏt eye", 
            "D18": "Ear", "D19": "Eye, nose, and cheek", "D20": "Var. D19", "D21": "Mouth", "D22": "Mouth with two lines", 
            "D23": "Mouth with three lines", "D24": "Upper lip with teeth", "D25": "Lips with teeth", "D26": "Lips spewing water", 
            "D27": "Breast", "D27a": "Var. of D27", "D28": "Two arms", "D29": "Var. of D28", "D30": "Two arms with tail", 
            "D31": "Combination of signs D32 and U36", "D32": "Two arms embracing", "D33": "Arms holding oar", 
            "D34": "Arms with shield and axe", "D34a": "Arms with shield and mace", "D35": "Negative arms", "D36": "Arm", 
            "D37": "Arm holding sign X8", "D38": "Arm holding bread", "D39": "Arm holding W24", "D40": "Arm holding stick", 
            "D41": "Arm with downward facing palm", "D42": "Arm with downward facing palm", "D43": "Arm with flail", 
            "D44": "Arm with scepter", "D45": "Arm with brush", "D46": "Hand", "D46a": "Hand with water", "D47": "Hand", 
            "D48": "Palm without thumb", "D49": "Fist", "D50": "Vertical finger", "D51": "Horizontal finger", 
            "D52": "Penis", "D53": "Penis with liquid", "D54": "Legs walking", "D55": "Legs walking (reverse of D54)", 
            "D56": "Leg", "D57": "Leg with T30", "D58": "Foot", "D59": "Foot with D36", "D60": "Foot with water streaming", 
            "D61": "Toes", "D62": "Var. D61", "D63": "Var. D61",
            
            # E. Mammals
            "E1": "Bull", "E2": "Bull preparing to charge", "E3": "Calf", "E4": "Sacred cow", "E5": "Cow with calf", 
            "E6": "Horse", "E7": "Donkey", "E8": "Kid", "E9": "Newborn bubalis", "E10": "Ram", "E11": "Ram", 
            "E12": "Pig", "E13": "Cat", "E14": "Dog", "E15": "Recumbent Jackal", "E16": "Recumbent Jackal on shrine", 
            "E17": "Jackal", "E18": "Jackal on standard R12", "E19": "O.K. form of last", "E20": "Seth animal", 
            "E21": "Recumbent Seth animal", "E22": "Lion", "E23": "Recumbent Lion", "E24": "Panther", 
            "E25": "Hippopotamus", "E26": "Elephant", "E27": "Giraffe", "E28": "Oryx", "E29": "Gazelle", 
            "E30": "Ibex", "E31": "Goat with collar", "E32": "Baboon", "E33": "Monkey", "E34": "Hare",
            
            # F. Parts of mammals
            "F1": "Head of ox", "F2": "Head of charging ox", "F3": "Head of hippopotamus", "F4": "Forepart of lion", 
            "F5": "Head of bubalis", "F6": "Forepart of bubalis", "F7": "Head of ram", "F8": "Forepart of ram", 
            "F9": "Head of leopard", "F10": "Head and neck of animal", "F11": "O.K. form of F10", "F12": "Head and neck of jackal", 
            "F13": "Horns of ox", "F14": "Combination of F13 and M4", "F15": "Combination of F14 and N5", "F16": "Horn", 
            "F17": "Combination of F16 and D60 water vessel", "F18": "Tusk of elephant", "F19": "Jawbone of ox", 
            "F20": "Tongue", "F21": "Ear of ox", "F22": "Hindquarters of leopard or lion", "F23": "Foreleg of ox", 
            "F24": "Reverse of F23", "F25": "Leg and hoof of ox", "F26": "Goatskin", "F27": "Cowskin", "F28": "Var. of F27", 
            "F29": "Combination of F28 + arrow", "F30": "Water skin", "F31": "Three fox skins", "F32": "Animal belly and tail", 
            "F33": "Tail", "F34": "Heart", "F35": "Heart and windpipe", "F36": "Lung and windpipe", "F37": "Backbone and ribs", 
            "F38": "Var. of F37", "F39": "Backbone and spinal cord", "F40": "Backbone and spinal cord at each end", 
            "F41": "Vertebrae", "F42": "Rib", "F43": "Ribs", "F44": "Leg bone with meat", "F45": "Heifer uterus", 
            "F46": "Intestine", "F47": "Var. of F46", "F48": "Var. of F46", "F49": "Var. of F46", "F50": "Combination of F46 and S29", 
            "F51": "Piece of flesh", "F52": "Excrement",
            
            # G. Birds
            "G1": "Vulture", "G2": "Two Vultures", "G3": "Combination of G1 + U1", "G4": "Buzzard", "G5": "Falcon", 
            "G6": "Falcon with flail", "G7": "Falcon on standard", "G7a": "Var of G7, Falcon in boat", 
            "G7b": "Var of G7, G7a", "G8": "Combination of G5 + S12", "G9": "Falcon with sun disk", "G10": "Falcon in sacred bark", 
            "G11": "Falcon image", "G12": "Falcon image with flail", "G13": "Falcon image with S9", "G14": "Vulture", 
            "G15": "Vulture with flail", "G16": "Nehkbet and Edjo", "G17": "Owl", "G18": "Two Owls", "G19": "Combination of G17 + D37", 
            "G20": "Combination of G17 + D36", "G21": "Guinea fowl", "G22": "Hoopoe", "G23": "Lapwing", "G24": "Var. of G23", 
            "G25": "Crested Ibis", "G26": "Sacred ibis on standard", "G26a": "Sacred ibis", "G27": "Flamingo", 
            "G28": "Black ibis", "G29": "Jabiru", "G30": "Three jabirus", "G31": "Heron", "G32": "Heron on perch", 
            "G33": "Egret", "G34": "Ostrich", "G35": "Cormorant", "G36": "Swallow", "G37": "Sparrow", "G38": "Goose", 
            "G39": "Duck", "G40": "Duck flying", "G41": "Duck landing", "G42": "Fattened bird", "G43": "Quail chick, var. Z7", 
            "G44": "Two quail chicks", "G45": "Combination of G43 + D36", "G46": "Combination of G43 + U1", "G47": "Duckling", 
            "G48": "Three ducklings in nest", "G49": "Ducks' heads protruding from pool", "G50": "Two plovers", 
            "G51": "Bird pecking fish", "G52": "Goose feeding", "G53": "Human headed bird", "G54": "Plucked bird",
            
            # H. Parts of birds
            "H1": "Head of duck", "H2": "Head of crested bird", "H3": "Head of spoonbill", "H4": "Head of vulture", 
            "H5": "Wing", "H6": "Feather", "H7": "Claw", "H8": "Egg",
            
            # I. Amphibious animals, reptiles, etc.
            "I1": "Lizard", "I2": "Turtle", "I3": "Crocodile", "I4": "Crocodile on shrine", "I5": "Crocodile with curved tail", 
            "I6": "Crocodile scales", "I7": "Frog", "I8": "Tadpole", "I9": "Horned viper", "I10": "Cobra", 
            "I11": "Two cobras", "I12": "Erect cobra", "I13": "Combination of I12 + V30", "I14": "Snake", "I15": "Var. of I15",
            
            # K. Fish and parts of fish
            "K1": "Bulti fish", "K2": "Barbel fish", "K3": "Mullet fish", "K4": "Oxyrhynchus fish", "K5": "Pike fish", 
            "K6": "Fish scale", "K7": "Blowfish",
            
            # L. Invertebrates and lesser animals
            "L1": "Scarab beetle", "L2": "Bee", "L3": "Fly", "L4": "Locust", "L5": "Centipede", "L6": "Shell", "L7": "Scorpion",
            
            # M. Trees and plants
            "M1": "Tree", "M2": "Plant", "M3": "Branch", "M4": "Stripped palm branch", "M5": "Combination of M4 + X1", 
            "M6": "Combination of M4 + D21", "M7": "Combination of M4 + Q3", "M8": "Pool with lilies", "M9": "Lily", 
            "M10": "Lily bud", "M11": "Flower and stem", "M12": "Lily plant", "M13": "Papyrus stem", "M14": "Combination of M13 and I10", 
            "M15": "Papyrus clump with downward facing buds", "M16": "Papyrus clump", "M17": "Reed leaf", 
            "M18": "Combination of M17 + D54", "M19": "Conical cakes between signs M17 and U36", "M20": "Reed field", 
            "M21": "Reed field with root", "M22": "Rush with shoots", "M23": "Sedge", "M24": "Combination of M23 + D21", 
            "M25": "Combination of M26 + M24", "M26": "Sedge", "M27": "Combination of M26 + D36", "M28": "Combination of M26 + V20", 
            "M29": "Pod", "M30": "Root", "M31": "Rhizome", "M32": "Var of M31", "M33": "Grain", "M34": "Emmer sheaf", 
            "M35": "Grain heap", "M36": "Flax bundle", "M37": "Flax bundle with stems", "M38": "Flax bundle", 
            "M39": "Basket of fruit or grain", "M40": "Reed bundle", "M41": "Wood log", "M42": "Flower", 
            "M43": "Grape vines on props", "M44": "Thorn",
            
            # N. Sky, earth, water
            "N1": "Sky", "N2": "Sky with broken S40", "N3": "Var. of N2", "N4": "Sky with rain", "N5": "Sun", 
            "N6": "Sun with uraeus", "N7": "Combination of N5 + T28", "N8": "Sun with rays", "N9": "Moon", "N10": "Var of N9", 
            "N11": "Crescent moon", "N12": "Var. of N11", "N13": "Combination of half of N11 and N14", "N14": "Star", 
            "N15": "Star encircled", "N16": "Flat land with grain", "N17": "Var. of N16", "N18": "Strip of sand", 
            "N19": "Two strips of sand", "N20": "Tongue of land", "N21": "Tongue of land", "N22": "Tongue of land", 
            "N23": "Canal", "N24": "Irrigation canal system", "N25": "Mountain range", "N26": "Mountain", 
            "N27": "Sunrise over mountain", "N28": "Hill with sun rays", "N29": "Sandy slope", "N30": "Hill with shrubs", 
            "N31": "Road bordered by shrubs", "N32": "Lump of clay, Var. Aa2 and F52", "N33": "Grain of sand", 
            "N33b": "Grain of sand (variant)", "N34": "Metal Ingot", "N35": "Water ripple", "N35a": "Three ripples", 
            "N36": "Canal", "N37": "Pool", "N38": "Var. of N37", "N39": "Var. of N37", "N40": "Combination of N37 and D54", 
            "N41": "Well with water", "N42": "Var. of N41", "N58": "Well with water",
            
            # O. Buildings, parts of buildings, etc.
            "O1": "House plan", "O2": "Combination of O1 + T3", "O3": "Combination of O1 + P8 + X3 + W22", "O4": "Reed shelter", 
            "O5": "Winding wall", "O6": "Plan of rectangular enclosure", "O7": "Var of O6", "O8": "Combination of O7 + O29", 
            "O9": "Combination of O7 + O30", "O10": "Combination of O6 + G5", "O12": "Palace with battlements", 
            "O13": "Enclosure with battlements", "O14": "Var. of O13", "O15": "Walled enclosure with buttresses + W10 + X1", 
            "O16": "Gateway with serpents", "O17": "Var. of O16", "O18": "Shrine in profile", "O19": "Shrine in profile with poles", 
            "O20": "Shrine", "O21": "Shrine Facade", "O22": "Booth supported by pole", "O23": "Double platform", 
            "O24": "Pyramid surrounded by wall", "O25": "Obelisk", "O26": "Stela", "O27": "Hall with columns", 
            "O28": "Column with tenon", "O29": "Wood column", "O29V": "Vertical wood column", "O30": "Supporting pole", 
            "O31": "Door", "O32": "Gateway", "O33": "Palace or tomb facade", "O34": "Door bolt", "O35": "Combination of O34 + D54", 
            "O36": "Wall", "O37": "Falling wall", "O38": "Corner of wall", "O39": "Stone slab", "O40": "Stairway", 
            "O41": "Double stairway", "O42": "Fence", "O43": "Var. of O42", "O44": "Min emblem", "O45": "Domed building", 
            "O46": "Var. of O45", "O47": "Enclosed mound", "O48": "Var. of O47", "O49": "Area with crossroads", 
            "O50": "Threshing floor with grain", "O51": "Grain mound on mud floor",
            
            # P. Ships and parts of ships
            "P1": "Boat on water", "P1a": "Boat upside down", "P2": "Ship sailing", "P3": "Sacred bark", "P4": "Boat with net", 
            "P5": "Sail", "P6": "Mast", "P7": "Combination of P6 +D36", "P8": "Oar", "P9": "Combination of P8 + I9", 
            "P10": "Steering oar", "P11": "Mooring post",
            
            # Q. Domestic and funerary furniture
            "Q1": "Seat", "Q2": "Portable seat", "Q3": "Stool", "Q4": "Headrest", "Q5": "Chest", "Q6": "Coffin", "Q7": "Brazier with flame",
            
            # R. Temple furniture and sacred emblems
            "R1": "Table with jug and loaves", "R2": "Table with bread slices", "R3": "Low table with Jug and loaves", 
            "R4": "Bread loaf on mat", "R5": "Censer", "R6": "Var. of R5", "R7": "Incense bowl", "R8": "Flag", 
            "R9": "Combination of R8 + V33", "R10": "Combination of R8 + T28 + N29", "R11": "Reed column", "R12": "Standard", 
            "R13": "Combination of G5 + R14", "R14": "Var of R13", "R15": "Spear as standard", "R16": "Scepter with feathers", 
            "R17": "Feathered wig with pole", "R18": "Var. of R17", "R19": "Combination of S40 + feather", "R20": "Seshat emblem", 
            "R21": "Var. of R20", "R22": "Min emblem", "R23": "Var. of R22", "R24": "Neith emblem", "R25": "Var. of R24",
            
            # S. Crowns, dress, staves, etc.
            "S1": "White crown of Upper Egypt", "S2": "Combination of S1 + V30", "S3": "Red crown of Lower Egypt", 
            "S4": "Combination of S3 + V30", "S5": "Combination of red and white crown", "S6": "Combination of S5 + V30", 
            "S7": "Blue Crown", "S8": "Atef crown", "S9": "Double plumes", "S10": "Headband", "S11": "Collar", 
            "S12": "Collar of beads", "S13": "Combination of S12 + D58", "S14": "Combination of S12 + T3", 
            "S14a": "Combination of S12 + S40", "S15": "Faience pectoral", "S16": "Var. of S15", "S17": "Var of S15", 
            "S18": "Bead necklace", "S19": "Necklace and cylinder seal", "S20": "Necklace and cylinder seal", "S21": "Ring", 
            "S22": "Shoulder knot", "S23": "Knotted cloth", "S24": "Knotted belt", "S25": "Garment with ties", "S26": "Apron", 
            "S27": "Horizontal strips of cloth", "S28": "Cloth with fringe + S29", "S29": "Folded cloth", 
            "S30": "Combination of S29 + I9", "S31": "Combination of S29 + U1", "S32": "Cloth with fringe", "S33": "Sandal", 
            "S34": "Sandal strap", "S35": "Sunshade", "S36": "Var. of S35", "S37": "Fan", "S38": "Crook", "S39": "Crook", 
            "S40": "Scepter with Seth animal", "S41": "Scepter with spiral shaft and Seth animal", "S42": "Scepter", 
            "S43": "Staff", "S44": "Staff with flail", "S45": "Flail",
            
            # T. Warfare, hunting, butchery
            "T1": "Angular headed mace", "T2": "T3 tilted", "T3": "Pear shaped mace", "T4": "Var of T3", 
            "T5": "Combination of T3 + I10", "T6": "Combination of T5 + extra I10", "T7": "Axe", "T7a": "Axe", 
            "T8": "Dagger", "T8a": "Dagger", "T9": "Bow", "T9a": "Var of T9", "T10": "Composite bow", "T11": "Arrow", 
            "T12": "Bowstring", "T13": "Wood tied together", "T14": "Throw stick", "T15": "Var. of T14", "T16": "Scimitar", 
            "T17": "Chariot", "T18": "Crook with package", "T19": "Bone harpoon head", "T20": "Var. of T19", "T21": "Harpoon", 
            "T22": "Arrowhead", "T23": "Var. of T22", "T24": "Fishing net", "T25": "Reed Float", "T26": "Bird Trap", 
            "T27": "Var. of T26", "T28": "Butcher's block", "T29": "Combination of T28 + T30", "T30": "Knife", 
            "T31": "Knife sharpener", "T32": "Combination of T31 + D54", "T33": "Butcher's knife sharpener", 
            "T34": "Butcher's knife", "T35": "Var. of T34",
            
            # U. Agriculture, crafts, and professions
            "U1": "Sickle", "U2": "Var. of U1", "U3": "Combination of U1 + D4", "U4": "Combination of U1 + Aa11", 
            "U5": "Var. of U4", "U6": "Hoe", "U7": "Var. of U6", "U8": "Hoe", "U9": "Grain measure with grain streaming outwards", 
            "U10": "Combination of U9 + M33", "U11": "Combination of S38 + U9", "U12": "Combination of D50 + U9", 
            "U13": "Plow", "U14": "Two branches joined", "U15": "Sled", "U16": "Sled with jackal head bearing a load", 
            "U17": "Pick with pool", "U18": "Var. U17", "U19": "Adze", "U20": "Var. of U19", "U21": "Adze with wood block", 
            "U22": "Chisel", "U23": "Chisel", "U24": "Drill for stone", "U25": "Var. of U24", "U26": "Drill for beads", 
            "U27": "Var. of U26", "U28": "Fire drill", "U29": "Var. of U28", "U30": "Kiln", "U31": "Baker's rake", 
            "U32": "Mortar and pestle", "U33": "Pestle", "U34": "Spindle", "U35": "Combination of U34 + I9", 
            "U36": "Club used in washing", "U37": "Razor", "U38": "Scale", "U39": "Scale post", "U40": "Var. of U39", "U41": "Plumb bob",
            
            # V. Rope, fiber, baskets, bags, etc.
            "V1": "Rope coil", "V2": "Combination of V1 + O34", "V3": "Same as V2, but with two additional coils", 
            "V4": "Lasso", "V5": "Looped rope", "V6": "Cord with loop facing downwards", "V7": "Cord with loop facing upwards", 
            "V8": "Var. of V7", "V9": "Round cartouche", "V10": "Oval cartouche", "V11": "End of cartouche", "V12": "String", 
            "V13": "Tethering rope", "V14": "Var. of V13", "V15": "Combination of V13 and D54", "V16": "Hobble for cattle", 
            "V17": "Herdsman's shelter", "V18": "Var. of V17", "V19": "Hobble for cattle", "V20": "Hobble for cattle sans crossbar", 
            "V21": "Combination of V20 + I10", "V22": "Whip", "V23": "Var. of V22", "V24": "Cord on Stick", "V25": "Var. of V24", 
            "V26": "Spool with thread", "V27": "Var. of V26", "V28": "Wick", "V29": "Swab", "V30": "Basket", "V31": "Basket with handle", 
            "V31a": "V31 reversed", "V32": "Wicker satchel", "V33": "Linen bag", "V34": "Var. of V33", "V35": "Var. of V33", 
            "V36": "Receptacle", "V37": "Bandage", "V38": "Bandage", "V39": "Tie",
            
            # W. Vessels of stone and earthenware
            "W1": "Oil jar", "W2": "Oil jar without ties", "W3": "Alabaster basin", "W4": "Combination of W3 + O22", 
            "W5": "Combination of W3 + T28", "W6": "Vessel", "W7": "Granite bowl", "W8": "Var. of W7", "W9": "Stone jug", 
            "W10": "Cup", "W10a": "Pot", "W11": "Ring stand", "W12": "Ring stand", "W13": "Pot", "W14": "Tall jar", 
            "W15": "Tall jar with water", "W16": "Combination of W15 + W12", "W17": "Tall jars in rack", "W18": "Var. W17", 
            "W19": "Milk jug", "W20": "Milk jug with leaf", "W21": "Wine jars", "W22": "Beer jugs", "W23": "Jug with handles", 
            "W24": "Bowl", "W25": "Combination of W24 + legs",
            
            # X. Vessels of glass and similar materials
            "X1": "Small bread loaf", "X2": "Tall bread loaf", "X3": "Var. of X2", "X4": "Bread roll", "X5": "Var. of X4", 
            "X6": "Round loaf with baker's mark", "X7": "Half loaf of bread", "X8": "Conical Loaf",
            
            # Y. Writing, games, music
            "Y1": "Papyrus scroll", "Y1v": "Papyrus scroll (vertical)", "Y2": "Var. of Y1", "Y3": "Scribal kit", 
            "Y4": "Y4 reversed", "Y5": "Game board", "Y6": "Game piece", "Y7": "Harp", "Y8": "Sistrum",
            
            # Z. Strokes, geometrical figures, etc.
            "Z1": "Stroke", "Z2": "Triple stroke", "Z3": "Three Z1 vertical strokes", "Z3a": "Z2 vertical", 
            "Z4": "Two diagonal strokes", "Z4a": "Two vertical strokes", "Z5": "Diagonal stroke in hieratic", 
            "Z6": "Hieratic var. of A13 and A14", "Z7": "From hieratic var. of G43", "Z8": "Oval", "Z9": "Crossed sticks", 
            "Z10": "Var. of Z9", "Z11": "Crossed planks", "Z1b": "Stroke variant",
            
            # Not Listed
            "Not Listed": "Symbol not in standard Gardiner classification"
        }
        
        # Create the list of symbols from the descriptions dictionary
        self.GARDINER_CATEGORIES = list(self.SYMBOL_DESCRIPTIONS.keys())
        self.CATEGORY_CODES = self.GARDINER_CATEGORIES.copy()
        
        # Create output directories
        for code in self.CATEGORY_CODES:
            os.makedirs(os.path.join(self.OUTPUT_DIR, code), exist_ok=True)
        
        # State variables
        self.current_image = None
        self.current_image_path = None
        self.image_files = []
        self.current_image_index = 0
        self.boxes = []
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.current_box = None
        
        # Free shape variables
        self.free_shape_mode = False
        self.polygon_points = []
        self.polygons = []  # Store completed polygons
        
        # Display transformation tracking
        self.display_scale_x = 1.0
        self.display_scale_y = 1.0
        self.display_x1 = 0
        self.display_y1 = 0
        
        self.setup_gui()
        self.load_images()
        
    def setup_gui(self):
        """Setup the GUI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Image viewer
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Image canvas with scrollbars
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', highlightthickness=0)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Image controls
        controls_frame = ttk.Frame(left_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(controls_frame, text="🔍 Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🔍 Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🔄 Reset View", command=self.reset_view).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(controls_frame, text="🗑️ Clear Boxes", command=self.clear_boxes).pack(side=tk.LEFT, padx=(0, 5))
        
        # Free shape mode toggle
        self.free_shape_button = ttk.Button(controls_frame, text="🔷 Free Shape", command=self.toggle_free_shape)
        self.free_shape_button.pack(side=tk.LEFT, padx=(10, 5))
        
        # Panning controls
        pan_frame = ttk.Frame(controls_frame)
        pan_frame.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(pan_frame, text="←", command=self.pan_left, width=3).pack(side=tk.LEFT, padx=(0, 1))
        ttk.Button(pan_frame, text="→", command=self.pan_right, width=3).pack(side=tk.LEFT, padx=(0, 1))
        ttk.Button(pan_frame, text="↑", command=self.pan_up, width=3).pack(side=tk.LEFT, padx=(0, 1))
        ttk.Button(pan_frame, text="↓", command=self.pan_down, width=3).pack(side=tk.LEFT)
        
        # Right panel - Symbol list and controls
        right_frame = ttk.Frame(main_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Image info
        info_frame = ttk.LabelFrame(right_frame, text="📷 Current Image", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.image_info_label = ttk.Label(info_frame, text="No image loaded")
        self.image_info_label.pack()
        
        self.progress_label = ttk.Label(info_frame, text="")
        self.progress_label.pack()
        
        # Symbol list
        symbol_frame = ttk.LabelFrame(right_frame, text="🏷️ Hieroglyph Symbols", padding=10)
        symbol_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Search box
        search_frame = ttk.Frame(symbol_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_categories)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Category listbox with scrollbar
        listbox_frame = ttk.Frame(symbol_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.category_listbox = tk.Listbox(listbox_frame, height=15, font=('Arial', 10))
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.category_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.category_listbox.configure(yscrollcommand=listbox_scrollbar.set)
        
        # Populate category list
        self.populate_categories()
        
        # Selected symbol information
        selected_frame = ttk.LabelFrame(symbol_frame, text="📋 Selected Symbol", padding=10)
        selected_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Symbol name
        name_frame = ttk.Frame(selected_frame)
        name_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(name_frame, text="🏷️ Name:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.symbol_name_label = ttk.Label(name_frame, text="None", foreground='#2196F3', font=('Arial', 10, 'bold'))
        self.symbol_name_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Symbol description
        desc_frame = ttk.Frame(selected_frame)
        desc_frame.pack(fill=tk.X)
        ttk.Label(desc_frame, text="📝 Description:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.symbol_description_label = ttk.Label(desc_frame, text="None", foreground='#4CAF50', 
                                                font=('Arial', 9), wraplength=350, justify=tk.LEFT)
        self.symbol_description_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Action buttons
        action_frame = ttk.LabelFrame(right_frame, text="⚡ Actions", padding=10)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="👁️ Preview Boxes", command=self.preview_boxes).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="💾 Save Symbol", command=self.save_current_symbol).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="➡️ Next Image", command=self.next_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="⬅️ Previous Image", command=self.previous_image).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(action_frame, text="📁 Open Folder", command=self.open_output_folder).pack(fill=tk.X)
        
        # Keyboard shortcuts help
        shortcuts_frame = ttk.LabelFrame(right_frame, text="⌨️ Keyboard Shortcuts", padding=10)
        shortcuts_frame.pack(fill=tk.X, pady=(0, 10))
        
        shortcuts_text = """Navigation:
• N/P: Next/Previous image
• ← → ↑ ↓: Pan image
• +/-: Zoom in/out
• R: Reset view
• C: Clear boxes
• S: Save symbol

Free Shape Mode:
• F: Toggle free shape mode
• Left-click: Add polygon points
• Right-click: Complete polygon"""
        
        ttk.Label(shortcuts_frame, text=shortcuts_text, font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Bind events
        self.image_canvas.bind("<Button-1>", self.on_canvas_click)
        self.image_canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.image_canvas.bind("<Button-3>", self.on_right_click)  # Right-click
        self.image_canvas.bind("<B3-Motion>", self.do_pan)   # Right-drag
        self.image_canvas.bind("<MouseWheel>", self.on_canvas_scroll)
        self.image_canvas.bind("<Button-4>", self.on_canvas_scroll)  # Linux
        self.image_canvas.bind("<Button-5>", self.on_canvas_scroll)  # Linux
        
        self.category_listbox.bind("<<ListboxSelect>>", self.on_category_select)
        
        # Keyboard shortcuts
        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()
        
    def populate_categories(self):
        """Populate the category listbox"""
        self.category_listbox.delete(0, tk.END)
        for i, symbol in enumerate(self.GARDINER_CATEGORIES):
            description = self.SYMBOL_DESCRIPTIONS.get(symbol, "Unknown")
            self.category_listbox.insert(tk.END, f"{i+1:3d}. {symbol} - {description}")
    
    def filter_categories(self, *args):
        """Filter categories based on search text"""
        search_text = self.search_var.get().lower()
        self.category_listbox.delete(0, tk.END)

        for i, symbol in enumerate(self.GARDINER_CATEGORIES):
            description = self.SYMBOL_DESCRIPTIONS.get(symbol, "Unknown")
            if search_text in symbol.lower() or search_text in description.lower():
                self.category_listbox.insert(tk.END, f"{i+1:3d}. {symbol} - {description}")
    
    def on_category_select(self, event):
        """Handle category selection"""
        selection = self.category_listbox.curselection()
        if selection:
            index = selection[0]
            # Get the actual symbol index from the filtered list
            search_text = self.search_var.get().lower()
            filtered_symbols = [symbol for symbol in self.GARDINER_CATEGORIES 
                              if search_text in symbol.lower() or search_text in self.SYMBOL_DESCRIPTIONS.get(symbol, "").lower()]
            if index < len(filtered_symbols):
                selected_symbol = filtered_symbols[index]
                description = self.SYMBOL_DESCRIPTIONS.get(selected_symbol, "Unknown")
                
                # Update the new name and description labels
                self.symbol_name_label.config(text=selected_symbol)
                self.symbol_description_label.config(text=description)
    
    def load_images(self):
        """Load image files from input directory"""
        if not os.path.exists(self.INPUT_DIR):
            messagebox.showerror("Error", f"Input directory '{self.INPUT_DIR}' not found!")
            return
            
        self.image_files = [f for f in os.listdir(self.INPUT_DIR) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not self.image_files:
            messagebox.showwarning("Warning", f"No images found in '{self.INPUT_DIR}'!")
            return
            
        self.current_image_index = 0
        self.load_current_image()
    
    def load_current_image(self):
        """Load the current image"""
        if not self.image_files:
            return
            
        image_path = os.path.join(self.INPUT_DIR, self.image_files[self.current_image_index])
        self.current_image_path = image_path
        
        # Load image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", f"Could not load image: {image_path}")
            return
            
        # Convert BGR to RGB
        self.current_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Update UI
        self.update_image_info()
        self.reset_view()
        self.clear_boxes()
        self.display_image()
    
    def update_image_info(self):
        """Update image information display"""
        if self.current_image is not None:
            filename = os.path.basename(self.current_image_path)
            progress = f"{self.current_image_index + 1} / {len(self.image_files)}"
            self.image_info_label.config(text=filename)
            self.progress_label.config(text=progress)
    
    def display_image(self):
        """Display the current image on canvas"""
        if self.current_image is None:
            return

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.display_image)
            return

        h, w = self.current_image.shape[:2]

        # Compute scaled dimensions
        scaled_w = int(w * self.zoom)
        scaled_h = int(h * self.zoom)

        # Resize the image for display
        resized_img = cv2.resize(self.current_image, (scaled_w, scaled_h), interpolation=cv2.INTER_LINEAR)

        # Determine the visible region (for panning)
        x1 = max(0, self.offset_x)
        y1 = max(0, self.offset_y)
        x2 = min(x1 + canvas_width, scaled_w)
        y2 = min(y1 + canvas_height, scaled_h)

        # Crop the visible region
        visible = resized_img[y1:y2, x1:x2]

        # Convert to ImageTk
        display_img = Image.fromarray(visible)
        self.photo = ImageTk.PhotoImage(display_img)
        self.image_canvas.delete("all")
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Store transformation data for coordinate conversion
        self.display_scale_x = scaled_w / w
        self.display_scale_y = scaled_h / h
        self.display_x1 = x1
        self.display_y1 = y1

        self.draw_boxes()
        self.draw_polygons()
    
    def start_pan(self, event):
        """Start panning with right-click"""
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def do_pan(self, event):
        """Pan the image with right-drag"""
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        
        # Calculate new offsets
        new_offset_x = self.offset_x - dx
        new_offset_y = self.offset_y - dy
        
        # Ensure we don't pan beyond image boundaries
        if self.current_image is not None:
            h, w = self.current_image.shape[:2]
            scaled_w = int(w * self.zoom)
            scaled_h = int(h * self.zoom)
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            max_offset_x = max(0, scaled_w - canvas_width)
            max_offset_y = max(0, scaled_h - canvas_height)
            
            self.offset_x = max(0, min(new_offset_x, max_offset_x))
            self.offset_y = max(0, min(new_offset_y, max_offset_y))
        
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.display_image()
    
    def draw_boxes(self):
        """Draw all bounding boxes on the canvas"""
        if not self.boxes:
            return
            
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        for i, (x, y, w, h) in enumerate(self.boxes):
            # Convert image coordinates to canvas coordinates
            # First scale the box coordinates, then adjust for panning
            scaled_x1 = x * self.zoom
            scaled_y1 = y * self.zoom
            scaled_x2 = (x + w) * self.zoom
            scaled_y2 = (y + h) * self.zoom
            
            # Adjust for current pan offset
            canvas_x1 = int(scaled_x1 - self.offset_x)
            canvas_y1 = int(scaled_y1 - self.offset_y)
            canvas_x2 = int(scaled_x2 - self.offset_x)
            canvas_y2 = int(scaled_y2 - self.offset_y)
            
            # Only draw if box is visible
            if (canvas_x2 > 0 and canvas_x1 < canvas_width and 
                canvas_y2 > 0 and canvas_y1 < canvas_height):
                
                self.image_canvas.create_rectangle(
                    canvas_x1, canvas_y1, canvas_x2, canvas_y2,
                    outline='#00FF00', width=2, tags=f"box_{i}"
                )
                # Add box number
                self.image_canvas.create_text(
                    canvas_x1 + 5, canvas_y1 + 5,
                    text=str(i+1), fill='#00FF00', font=('Arial', 12, 'bold'),
                    tags=f"box_text_{i}"
                )
    
    def on_canvas_click(self, event):
        """Handle canvas click"""
        if self.free_shape_mode:
            # Add point to polygon
            self.polygon_points.append((event.x, event.y))
            print(f"Added point {len(self.polygon_points)}: ({event.x}, {event.y})")
            
            # Draw the point
            self.image_canvas.create_oval(
                event.x - 3, event.y - 3, event.x + 3, event.y + 3,
                fill='#00FF00', outline='#00FF00', tags="polygon_point"
            )
            
            # Draw line to previous point if exists
            if len(self.polygon_points) > 1:
                prev_x, prev_y = self.polygon_points[-2]
                self.image_canvas.create_line(
                    prev_x, prev_y, event.x, event.y,
                    fill='#00FF00', width=2, tags="polygon_line"
                )
        else:
            # Normal rectangle mode
            self.start_x = event.x
            self.start_y = event.y
            self.drawing = True
    
    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if self.drawing:
            # Clear previous temporary box
            self.image_canvas.delete("temp_box")
            
            # Draw temporary box
            self.image_canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='#FF0000', width=2, tags="temp_box"
            )
    
    def on_canvas_release(self, event):
        """Handle canvas release"""
        if self.drawing:
            self.drawing = False
            self.image_canvas.delete("temp_box")

            if self.current_image is None:
                return

            # Convert canvas coordinates → original image coordinates
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)

            # Convert canvas coordinates to scaled image coordinates
            # Add the pan offset to get the position in the scaled image
            scaled_x1 = x1 + self.offset_x
            scaled_y1 = y1 + self.offset_y
            scaled_x2 = x2 + self.offset_x
            scaled_y2 = y2 + self.offset_y

            # Convert scaled coordinates back to original image coordinates
            img_x1 = int(scaled_x1 / self.zoom)
            img_y1 = int(scaled_y1 / self.zoom)
            img_x2 = int(scaled_x2 / self.zoom)
            img_y2 = int(scaled_y2 / self.zoom)

            # Clip to image bounds
            h, w = self.current_image.shape[:2]
            img_x1 = max(0, min(w, img_x1))
            img_y1 = max(0, min(h, img_y1))
            img_x2 = max(0, min(w, img_x2))
            img_y2 = max(0, min(h, img_y2))

            if abs(img_x2 - img_x1) > 10 and abs(img_y2 - img_y1) > 10:
                self.boxes.append((img_x1, img_y1, img_x2 - img_x1, img_y2 - img_y1))
                self.display_image()
                print(f"Added box: ({img_x1},{img_y1}) to ({img_x2},{img_y2})")
    
    def on_canvas_scroll(self, event):
        """Handle canvas scroll for zooming"""
        if event.delta > 0 or event.num == 4:  # Zoom in
            self.zoom *= 1.1
        else:  # Zoom out
            self.zoom /= 1.1
            
        self.zoom = max(0.5, min(self.zoom, 5.0))
        self.display_image()
    
    def zoom_in(self):
        """Zoom in"""
        self.zoom *= 1.2
        self.zoom = min(self.zoom, 5.0)
        self.display_image()
    
    def zoom_out(self):
        """Zoom out"""
        self.zoom /= 1.2
        self.zoom = max(self.zoom, 0.5)
        self.display_image()
    
    def reset_view(self):
        """Reset zoom and pan"""
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.display_image()
    
    def pan_left(self):
        """Pan the image left (move view right)"""
        if self.current_image is not None:
            self.offset_x = max(0, self.offset_x - 50)
            self.display_image()
    
    def pan_right(self):
        """Pan the image right (move view left)"""
        if self.current_image is not None:
            h, w = self.current_image.shape[:2]
            scaled_w = int(w * self.zoom)
            canvas_width = self.image_canvas.winfo_width()
            max_offset_x = max(0, scaled_w - canvas_width)
            self.offset_x = min(self.offset_x + 50, max_offset_x)
            self.display_image()
    
    def pan_up(self):
        """Pan the image up (move view down)"""
        if self.current_image is not None:
            self.offset_y = max(0, self.offset_y - 50)
            self.display_image()
    
    def pan_down(self):
        """Pan the image down (move view up)"""
        if self.current_image is not None:
            h, w = self.current_image.shape[:2]
            scaled_h = int(h * self.zoom)
            canvas_height = self.image_canvas.winfo_height()
            max_offset_y = max(0, scaled_h - canvas_height)
            self.offset_y = min(self.offset_y + 50, max_offset_y)
            self.display_image()
    
    def clear_boxes(self):
        """Clear all bounding boxes"""
        self.boxes.clear()
        self.display_image()
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.keysym == 'n':
            self.next_image()
        elif event.keysym == 'p':
            self.previous_image()
        elif event.keysym == 'r':
            self.reset_view()
        elif event.keysym == 'c':
            self.clear_boxes()
        elif event.keysym == 's':
            self.save_current_symbol()
        elif event.keysym == 'f':
            self.toggle_free_shape()
        elif event.keysym == 'Left':
            self.pan_left()
        elif event.keysym == 'Right':
            self.pan_right()
        elif event.keysym == 'Up':
            self.pan_up()
        elif event.keysym == 'Down':
            self.pan_down()
        elif event.keysym == 'plus' or event.keysym == 'equal':
            self.zoom_in()
        elif event.keysym == 'minus':
            self.zoom_out()
    
    def toggle_free_shape(self):
        """Toggle free shape mode"""
        self.free_shape_mode = not self.free_shape_mode
        if self.free_shape_mode:
            self.free_shape_button.config(text="🔷 Free Shape ON", style="Accent.TButton")
            self.image_canvas.config(cursor="crosshair")
            print("Free shape mode: ON - Left-click to add points, Right-click to complete")
        else:
            self.free_shape_button.config(text="🔷 Free Shape", style="TButton")
            self.image_canvas.config(cursor="")
            # Clear any incomplete polygon
            self.polygon_points.clear()
            self.image_canvas.delete("polygon_point")
            self.image_canvas.delete("polygon_line")
            print("Free shape mode: OFF")
    
    def on_right_click(self, event):
        """Handle right-click"""
        if self.free_shape_mode and len(self.polygon_points) > 2:
            # Complete the polygon
            self.complete_polygon()
        else:
            # Start panning
            self.start_pan(event)
    
    def complete_polygon(self):
        """Complete the current polygon"""
        if len(self.polygon_points) > 2:
            # Close the polygon by connecting to the first point
            first_x, first_y = self.polygon_points[0]
            last_x, last_y = self.polygon_points[-1]
            
            # Draw the closing line
            self.image_canvas.create_line(
                last_x, last_y, first_x, first_y,
                fill='#00FF00', width=2, tags="polygon_line"
            )
            
            # Add to completed polygons
            self.polygons.append(self.polygon_points.copy())
            self.polygon_points.clear()
            
            # Clear temporary drawing elements
            self.image_canvas.delete("polygon_point")
            self.image_canvas.delete("polygon_line")
            
            # Redraw to show completed polygon
            self.display_image()
            print(f"Completed polygon with {len(self.polygons[-1])} points")
        else:
            print("Need at least 3 points to complete a polygon")
    
    def draw_polygons(self):
        """Draw all completed polygons"""
        for i, polygon in enumerate(self.polygons):
            if len(polygon) > 2:
                # Draw the polygon outline
                self.image_canvas.create_polygon(
                    polygon, outline='#00FF00', width=2, fill="",
                    tags=f"polygon_{i}"
                )
                
                # Add polygon number
                if polygon:
                    x, y = polygon[0]
                    self.image_canvas.create_text(
                        x + 5, y + 5, text=f"P{i+1}", fill='#00FF00',
                        font=('Arial', 12, 'bold'), tags=f"polygon_text_{i}"
                    )
    
    def clear_boxes(self):
        """Clear all bounding boxes and polygons"""
        self.boxes.clear()
        self.polygons.clear()
        self.polygon_points.clear()
        self.image_canvas.delete("polygon_point")
        self.image_canvas.delete("polygon_line")
        self.display_image()
        print("All annotations cleared")
    
    def save_current_symbol(self):
        """Save the currently selected symbol"""
        if not self.boxes and not self.polygons:
            messagebox.showwarning("Warning", "No annotations to save!")
            return
            
        # Get selected category
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a category first!")
            return
            
        # Get the actual symbol index
        search_text = self.search_var.get().lower()
        filtered_symbols = [symbol for symbol in self.GARDINER_CATEGORIES 
                          if search_text in symbol.lower() or search_text in self.SYMBOL_DESCRIPTIONS.get(symbol, "").lower()]
        if selection[0] >= len(filtered_symbols):
            messagebox.showwarning("Warning", "Invalid symbol selection!")
            return
            
        selected_symbol = filtered_symbols[selection[0]]
        symbol_description = self.SYMBOL_DESCRIPTIONS.get(selected_symbol, "Unknown")
        category_code = selected_symbol
        
        # Save all boxes and polygons
        saved_count = 0
        
        # Save bounding boxes
        for i, (x, y, w, h) in enumerate(self.boxes):
            # Ensure coordinates are within image bounds
            img_h, img_w = self.current_image.shape[:2]
            x1 = max(0, min(x, img_w))
            y1 = max(0, min(y, img_h))
            x2 = max(0, min(x + w, img_w))
            y2 = max(0, min(y + h, img_h))
            
            # Skip if box is invalid
            if x2 <= x1 or y2 <= y1:
                continue
                
            # Extract symbol from original image
            symbol_crop = self.current_image[y1:y2, x1:x2]
            
            # Convert to PIL Image and resize to standard size
            symbol_img = Image.fromarray(symbol_crop)
            symbol_img = symbol_img.resize(self.SAVE_SIZE, Image.Resampling.LANCZOS)
            
            # Save
            filename = f"{os.path.splitext(self.image_files[self.current_image_index])[0]}_box_{i:03d}.png"
            save_path = os.path.join(self.OUTPUT_DIR, category_code, filename)
            symbol_img.save(save_path)
            print(f"Saved Box {i+1}: ({x1},{y1}) to ({x2},{y2}) - Size: {x2-x1}x{y2-y1} -> {save_path}")
            saved_count += 1
        
        # Save polygons as actual selected areas
        for i, polygon in enumerate(self.polygons):
            if len(polygon) > 2:
                # Convert canvas coordinates to image coordinates
                img_polygon = []
                for point in polygon:
                    img_x = int((point[0] + self.offset_x) / self.zoom)
                    img_y = int((point[1] + self.offset_y) / self.zoom)
                    img_polygon.append((img_x, img_y))
                
                # Get bounding box for the crop area
                x_coords = [point[0] for point in img_polygon]
                y_coords = [point[1] for point in img_polygon]
                min_x = min(x_coords)
                max_x = max(x_coords)
                min_y = min(y_coords)
                max_y = max(y_coords)
                
                # Clip to image bounds
                h, w = self.current_image.shape[:2]
                min_x = max(0, min(w, min_x))
                min_y = max(0, min(h, min_y))
                max_x = max(0, min(w, max_x))
                max_y = max(0, min(h, max_y))
                
                if max_x > min_x and max_y > min_y:
                    # Create a mask for the polygon
                    mask = Image.new('L', (w, h), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    
                    # Draw the polygon on the mask
                    mask_draw.polygon(img_polygon, fill=255)
                    
                    # Crop the mask to the bounding box
                    mask_crop = mask.crop((min_x, min_y, max_x, max_y))
                    
                    # Crop the image to the bounding box
                    symbol_crop = self.current_image[min_y:max_y, min_x:max_x]
                    symbol_img = Image.fromarray(symbol_crop)
                    
                    # Apply the mask to get only the polygon area
                    # Create a transparent background
                    result_img = Image.new('RGBA', symbol_img.size, (0, 0, 0, 0))
                    
                    # Convert the original image to RGBA if needed
                    if symbol_img.mode != 'RGBA':
                        symbol_img = symbol_img.convert('RGBA')
                    
                    # Apply the mask
                    for y in range(symbol_img.height):
                        for x in range(symbol_img.width):
                            if mask_crop.getpixel((x, y)) > 0:  # If pixel is inside polygon
                                result_img.putpixel((x, y), symbol_img.getpixel((x, y)))
                    
                    # Resize to standard size
                    result_img = result_img.resize(self.SAVE_SIZE, Image.Resampling.LANCZOS)
                    
                    # Save
                    filename = f"{os.path.splitext(self.image_files[self.current_image_index])[0]}_polygon_{i:03d}.png"
                    save_path = os.path.join(self.OUTPUT_DIR, category_code, filename)
                    result_img.save(save_path)
                    print(f"Saved Polygon {i+1}: Actual polygon shape ({min_x},{min_y}) to ({max_x},{max_y}) - Size: {max_x-min_x}x{max_y-min_y} -> {save_path}")
                    saved_count += 1
        
        if saved_count > 0:
            messagebox.showinfo("Success", f"Saved {saved_count} annotation(s) to category '{selected_symbol} - {symbol_description}'")
            self.clear_boxes()
        else:
            messagebox.showwarning("Warning", "No valid annotations to save!")
    
    def preview_boxes(self):
        """Preview what will be saved from each annotation"""
        if not self.boxes and not self.polygons:
            messagebox.showwarning("Warning", "No annotations to preview!")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("📋 Annotation Preview")
        preview_window.geometry("800x600")
        
        # Create scrollable frame
        canvas = tk.Canvas(preview_window)
        scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Show each bounding box
        for i, (x, y, w, h) in enumerate(self.boxes):
            # Ensure coordinates are within image bounds
            img_h, img_w = self.current_image.shape[:2]
            x1 = max(0, min(x, img_w))
            y1 = max(0, min(y, img_h))
            x2 = max(0, min(x + w, img_w))
            y2 = max(0, min(y + h, img_h))
            
            if x2 <= x1 or y2 <= y1:
                continue
                
            # Extract symbol
            symbol_crop = self.current_image[y1:y2, x1:x2]
            symbol_img = Image.fromarray(symbol_crop)
            
            # Resize for preview (max 200px)
            max_size = 200
            symbol_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(symbol_img)
            
            # Create frame for this preview
            box_frame = ttk.Frame(scrollable_frame)
            box_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Label and image
            ttk.Label(box_frame, text=f"Box {i+1}: ({x1},{y1}) to ({x2},{y2}) - Size: {x2-x1}x{y2-y1}").pack(anchor=tk.W)
            print(f"Preview Box {i+1}: Original coords ({x},{y},{w},{h}) -> Final coords ({x1},{y1}) to ({x2},{y2})")  # Debug
            img_label = ttk.Label(box_frame, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(anchor=tk.W)
        
        # Show each polygon as actual selected area
        for i, polygon in enumerate(self.polygons):
            if len(polygon) > 2:
                # Convert canvas coordinates to image coordinates
                img_polygon = []
                for point in polygon:
                    img_x = int((point[0] + self.offset_x) / self.zoom)
                    img_y = int((point[1] + self.offset_y) / self.zoom)
                    img_polygon.append((img_x, img_y))
                
                # Get bounding box for the crop area
                x_coords = [point[0] for point in img_polygon]
                y_coords = [point[1] for point in img_polygon]
                min_x = min(x_coords)
                max_x = max(x_coords)
                min_y = min(y_coords)
                max_y = max(y_coords)
                
                # Clip to image bounds
                h, w = self.current_image.shape[:2]
                min_x = max(0, min(w, min_x))
                min_y = max(0, min(h, min_y))
                max_x = max(0, min(w, max_x))
                max_y = max(0, min(h, max_y))
                
                if max_x > min_x and max_y > min_y:
                    # Create a mask for the polygon
                    mask = Image.new('L', (w, h), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    
                    # Draw the polygon on the mask
                    mask_draw.polygon(img_polygon, fill=255)
                    
                    # Crop the mask to the bounding box
                    mask_crop = mask.crop((min_x, min_y, max_x, max_y))
                    
                    # Crop the image to the bounding box
                    symbol_crop = self.current_image[min_y:max_y, min_x:max_x]
                    symbol_img = Image.fromarray(symbol_crop)
                    
                    # Apply the mask to get only the polygon area
                    # Create a transparent background
                    result_img = Image.new('RGBA', symbol_img.size, (0, 0, 0, 0))
                    
                    # Convert the original image to RGBA if needed
                    if symbol_img.mode != 'RGBA':
                        symbol_img = symbol_img.convert('RGBA')
                    
                    # Apply the mask
                    for y in range(symbol_img.height):
                        for x in range(symbol_img.width):
                            if mask_crop.getpixel((x, y)) > 0:  # If pixel is inside polygon
                                result_img.putpixel((x, y), symbol_img.getpixel((x, y)))
                    
                    # Resize for preview (max 200px)
                    max_size = 200
                    result_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(result_img)
                    
                    # Create frame for this preview
                    poly_frame = ttk.Frame(scrollable_frame)
                    poly_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    # Label and image
                    ttk.Label(poly_frame, text=f"Polygon {i+1}: Actual selected shape ({min_x},{min_y}) to ({max_x},{max_y}) - Size: {max_x-min_x}x{max_y-min_y} - Points: {len(polygon)}").pack(anchor=tk.W)
                    img_label = ttk.Label(poly_frame, image=photo)
                    img_label.image = photo  # Keep a reference
                    img_label.pack(anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def next_image(self):
        """Go to next image"""
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_current_image()
        else:
            messagebox.showinfo("Info", "This is the last image!")
    
    def previous_image(self):
        """Go to previous image"""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
        else:
            messagebox.showinfo("Info", "This is the first image!")
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if os.path.exists(self.OUTPUT_DIR):
            os.startfile(self.OUTPUT_DIR)
        else:
            messagebox.showwarning("Warning", "Output directory does not exist!")

def main():
    root = tk.Tk()
    app = HieroglyphAnnotatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
