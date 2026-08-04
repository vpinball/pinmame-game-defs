"""Reviewed AC/DC normalized playfield placements for each supported edition."""

from __future__ import annotations


INPUT_POSITIONS = {
	1: [(0.082350, 0.568794)], 2: [(0.094800, 0.539655)], 3: [(0.106265, 0.513278)], 4: [(0.118582, 0.486390)],
	5: [(0.128387, 0.461360)], 6: [(0.870273, 0.458149)], 7: [(0.870273, 0.484732)], 8: [(0.870273, 0.511270)],
	9: [(0.870273, 0.537999)], 10: [(0.512028, 0.311990)], 11: [(0.569330, 0.321673)], 12: [(0.628993, 0.331598)],
	13: [(0.057878, 0.097009)], 14: [(0.257677, 0.205595)],
	18: [(0.580000, 0.940000)], 19: [(0.650000, 0.921000)], 20: [(0.720000, 0.903000)], 21: [(0.790000, 0.884000)], 22: [(0.835000, 0.872000)],
	23: [(0.947605, 0.890661)], 24: [(0.051591, 0.763999)], 25: [(0.128560, 0.743684)],
	26: [(0.220215, 0.726524)], 27: [(0.685802, 0.726524)], 28: [(0.775077, 0.743384)], 29: [(0.852337, 0.763147)],
	30: [(0.524113, 0.155556)], 31: [(0.736963, 0.151240)], 32: [(0.639000, 0.235974)], 33: [(0.163467, 0.353290)],
	34: [(0.235358, 0.359817)], 35: [(0.378990, 0.336108)], 36: [(0.399947, 0.145745)], 37: [(0.450843, 0.016417)],
	38: [(0.542534, 0.083160)], 39: [(0.632607, 0.074157)], 40: [(0.722549, 0.064641)], 41: [(0.802046, 0.150042)],
	42: [(0.784142, 0.364083)], 43: [(0.936687, 0.441300)], 44: [(0.104831, 0.106953)], 45: [(0.773227, 0.630580)],
	48: [(0.947901, 0.757156)], 59: [(0.939389, 0.104705)], 61: [(0.720277, 0.695345)], 62: [(0.720277, 0.695345)],
	81: [(0.620752, 0.847281)], 83: [(0.284974, 0.847281)],
}

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament", 16: "cabinet.start", 64: "cabinet.fire",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "cabinet.flipper", 84: "cabinet.flipper", -7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 22): "cabinet.rear-panel",
	("pinmame.output.solenoid", 24): "cabinet.knocker",
	("physical.output.ticket", 33): "service.ticket",
	("physical.output.ticket", 34): "service.ticket",
	("physical.output.ticket", 35): "service.ticket",
}

SOLENOID_POSITIONS = {
	1: [(0.861682, 0.865767)], 2: [(0.947605, 0.890661)], 3: [(0.720277, 0.695345)], 4: [(0.939496, 0.516017)],
	5: [(0.783568, 0.017554)], 9: [(0.524113, 0.155556)], 10: [(0.736963, 0.151240)], 11: [(0.639000, 0.235974)],
	12: [(0.450843, 0.016417)], 13: [(0.220215, 0.726524)], 14: [(0.685802, 0.726524)],
	15: [(0.284974, 0.847281)], 16: [(0.620752, 0.847281)], 17: [(0.085300, 0.064573)],
	20: [(0.268998, 0.232922)], 21: [(0.140206, 0.658291)], 23: [(0.340202, 0.012178)],
	25: [(0.524113, 0.155556), (0.736963, 0.151240), (0.639000, 0.235974)], 26: [(0.416532, 0.219762)],
	27: [(0.220513, 0.336352)], 28: [(0.370644, 0.308138)], 29: [(0.799869, 0.345778)],
	30: [(0.768324, 0.258153)], 31: [(0.863152, 0.622217)], 32: [(0.720277, 0.695345)],
}

LAMP_POSITIONS = {
	3: [(0.051196, 0.689776)], 4: [(0.129113, 0.677336)], 5: [(0.234637, 0.675286)], 6: [(0.669840, 0.673464)],
	7: [(0.773183, 0.676316)], 8: [(0.851702, 0.688299)], 9: [(0.205410, 0.467186)], 10: [(0.194818, 0.494780)],
	11: [(0.182945, 0.521927)], 12: [(0.171577, 0.549355)], 13: [(0.159593, 0.576496)],
	18: [(0.176836, 0.382324)], 19: [(0.249102, 0.383727)], 20: [(0.319156, 0.371832)], 21: [(0.385290, 0.360157)],
	22: [(0.490126, 0.345101)], 23: [(0.548768, 0.354897)], 24: [(0.609506, 0.365405)], 25: [(0.504132, 0.402215)],
	26: [(0.693897, 0.380765)], 27: [(0.883718, 0.302332)], 28: [(0.853487, 0.354285)], 29: [(0.815417, 0.408785)],
	30: [(0.810210, 0.456092)], 31: [(0.810557, 0.483704)], 32: [(0.810557, 0.511518)], 33: [(0.811142, 0.539268)],
	34: [(0.701395, 0.470890)], 35: [(0.415790, 0.223289)], 36: [(0.430513, 0.281517)], 37: [(0.542605, 0.044275)],
	38: [(0.631802, 0.034929)], 39: [(0.722618, 0.025580)], 40: [(0.634728, 0.009639)], 41: [(0.324593, 0.763245)],
	42: [(0.365233, 0.788881)], 43: [(0.385618, 0.820375)], 44: [(0.450544, 0.758364)], 45: [(0.452709, 0.784999)],
	46: [(0.452292, 0.806801)], 47: [(0.452909, 0.830226)], 48: [(0.453572, 0.855999)], 49: [(0.577164, 0.762689)],
	50: [(0.539155, 0.790352)], 51: [(0.521402, 0.820196)], 52: [(0.126360, 0.300005)],
	57: [(0.344369, 0.009803)], 58: [(0.724697, 0.009803)], 60: [(0.523187, 0.157771)], 61: [(0.734840, 0.151549)],
	62: [(0.637734, 0.236849)], 64: [(0.762463, 0.390665)],
}

LED_PRO_LAMP_POSITIONS = {
	**LAMP_POSITIONS,
	14: [(0.387038, 0.534787)], 15: [(0.520102, 0.534166)], 17: [(0.452994, 0.604875)],
}

ORIGINAL_PRO_INPUT_POSITIONS = {
	**INPUT_POSITIONS,
	36: [(0.387677, 0.092558)],
}

ORIGINAL_PRO_LAMP_POSITIONS = LED_PRO_LAMP_POSITIONS

GI_POSITIONS = [
	(0.900285, 0.469020), (0.874862, 0.583358), (0.042912, 0.489004), (0.786737, 0.291340), (0.048016, 0.289073),
	(0.147091, 0.159873), (0.051867, 0.020208), (0.835677, 0.052008), (0.692302, 0.824228), (0.216433, 0.825743),
	(0.891462, 0.415710), (0.833431, 0.124491), (0.949749, 0.005717), (0.370579, 0.032017), (0.187581, 0.045169),
	(0.348518, 0.211355), (0.541245, 0.282769), (0.355565, 0.270940), (0.206599, 0.288832), (0.758747, 0.802286),
	(0.720491, 0.724956), (0.181816, 0.698841), (0.151883, 0.803504), (0.757544, 0.228868), (0.498101, 0.087248),
	(0.587316, 0.077237), (0.677718, 0.068298), (0.768350, 0.059083), (0.497783, 0.091346), (0.588134, 0.083212),
	(0.677903, 0.074554), (0.766505, 0.063271), (0.653348, 0.275933), (0.033099, 0.599149), (0.896912, 0.524478),
	(0.697530, 0.758900), (0.206559, 0.759480), (0.100182, 0.411436),
]

LED_PRO_GI_POSITIONS = [
	*GI_POSITIONS[:11],
	(0.833431, 0.123162), (0.949749, 0.004389), (0.370579, 0.030689), (0.187581, 0.043841),
	(0.348518, 0.210027), (0.541245, 0.281441), (0.355565, 0.269611), (0.206599, 0.287503),
	(0.758747, 0.800958), (0.720491, 0.723627), (0.181816, 0.697513), (0.151883, 0.802175),
	(0.757544, 0.227540), (0.498101, 0.085920), (0.587316, 0.075908), (0.677718, 0.066970),
	(0.768350, 0.057755), (0.497783, 0.090017), (0.588134, 0.081884), (0.677903, 0.073225),
	(0.766505, 0.061943),
	*GI_POSITIONS[32:],
]

REAR_PANEL_LAMP_ADDRESSES = {53, 54, 55, 56, 65, 66, 67, 68, 69, 70, 71, 72}


# These coordinates are derived mechanically from the exact LUCI v15 extraction
# (bounds 0,0--952.9412231445312,2117.64697265625).  Object names are retained
# separately so a placement cannot silently become an unlabeled guessed point.
PREMIUM_INPUT_POSITIONS = {
	1: [(0.084339, 0.567704)], 2: [(0.097297, 0.539122)], 3: [(0.107914, 0.513202)], 4: [(0.119048, 0.486293)], 5: [(0.130327, 0.460519)],
	6: [(0.867271, 0.454523)], 7: [(0.867628, 0.482680)], 8: [(0.867985, 0.510149)], 9: [(0.867985, 0.537166)],
	10: [(0.513186, 0.313158)], 11: [(0.568901, 0.322299)], 12: [(0.628529, 0.332405)],
	13: [(0.057821, 0.096887)], 14: [(0.257423, 0.205338)],
	23: [(0.941520, 0.886771)], 24: [(0.056596, 0.759188)], 25: [(0.133521, 0.740783)],
	26: [(0.213347, 0.726417)], 27: [(0.695815, 0.726284)], 28: [(0.774102, 0.740337)], 29: [(0.850182, 0.759672)],
	30: [(0.528029, 0.157926)], 31: [(0.736783, 0.153288)], 32: [(0.640060, 0.237520)], 33: [(0.163305, 0.352849)],
	34: [(0.240449, 0.362890)], 35: [(0.383627, 0.337379)], 36: [(0.393808, 0.101018)], 37: [(0.455140, 0.016397)],
	38: [(0.546823, 0.083724)], 39: [(0.635323, 0.073730)], 40: [(0.724806, 0.064227)], 41: [(0.801254, 0.149854)],
	42: [(0.779577, 0.367541)], 43: [(0.935761, 0.440748)], 44: [(0.104727, 0.106820)], 45: [(0.772463, 0.629791)],
	46: [(0.585565, 0.304920)], 47: [(0.405036, 0.174300)], 48: [(0.940714, 0.752224)], 49: [(0.416605, 0.703139)],
	50: [(0.378088, 0.503585)], 51: [(0.452425, 0.480970)], 52: [(0.529839, 0.502724)],
	53: [(0.322104, 0.463886)], 54: [(0.584037, 0.463449)], 59: [(0.937734, 0.104574)],
	61: [(0.719565, 0.694476)], 62: [(0.719565, 0.694476)],
}

PREMIUM_INPUT_OBJECTS = {
	1: "Wall.sw1 collision polygon centroid", 2: "Wall.sw2 collision polygon centroid", 3: "Wall.sw3 collision polygon centroid",
	4: "Wall.sw4 collision polygon centroid", 5: "Wall.sw5 collision polygon centroid", 6: "HitTarget.sw6", 7: "HitTarget.sw7",
	8: "HitTarget.sw8", 9: "HitTarget.sw9", 10: "Wall.sw10 collision polygon centroid", 11: "Wall.sw11 collision polygon centroid",
	12: "Wall.sw12 collision polygon centroid", 13: "Trigger.Sw13", 14: "Trigger.Sw14", 23: "Trigger.sw23", 24: "Trigger.Sw24",
	25: "Trigger.Sw25", 26: "LeftSlingshot collision polygon centroid", 27: "RightSlingshot collision polygon centroid",
	28: "Trigger.Sw28", 29: "Trigger.Sw29", 30: "Bumper.Bumper1", 31: "Bumper.Bumper2", 32: "Bumper.Bumper3",
	33: "Spinner.Sw33", 34: "HitTarget.sw34", 35: "HitTarget.sw35", 36: "Kicker.sw36", 37: "Kicker.Sw37",
	38: "Trigger.Sw38", 39: "Trigger.Sw39", 40: "Trigger.Sw40", 41: "Trigger.Sw41", 42: "HitTarget.sw42", 43: "Trigger.Sw43",
	44: "Trigger.sw44", 45: "Kicker.Sw45", 46: "HitTarget.sw46", 47: "Primitive.Bell + Kicker.BellK assembly anchor; script-computed opto",
	48: "Trigger.Sw48", 49: "Kicker.sw49", 50: "HitTarget.sw50", 51: "HitTarget.sw51", 52: "HitTarget.sw52",
	53: "Trigger.sw53", 54: "Trigger.sw54", 59: "Trigger.Sw59", 61: "Primitive.Cannon_assyM projected center",
	62: "Primitive.Cannon_assyM projected center",
}

PREMIUM_SOLENOID_POSITIONS = {
	2: [(0.941915, 0.966801)], 3: [(0.416605, 0.703139)], 4: [(0.318004, 0.645937)], 5: [(0.586196, 0.645937)],
	9: [(0.528029, 0.157926)], 10: [(0.736783, 0.153288)], 11: [(0.640060, 0.237520)], 12: [(0.455140, 0.016397)],
	13: [(0.213347, 0.726417)], 14: [(0.695815, 0.726284)], 15: [(0.287741, 0.844088)], 16: [(0.620185, 0.844088)],
	17: [(0.085216, 0.063968)], 18: [(0.597339, 0.287719)], 19: [(0.147760, 0.854118), (0.741758, 0.856477)],
	20: [(0.273839, 0.233987)], 21: [(0.138565, 0.641524)], 23: [(0.339866, 0.012163)],
	25: [(0.528029, 0.157926), (0.736783, 0.153288), (0.640060, 0.237520)], 26: [(0.416120, 0.219487)],
	27: [(0.220295, 0.335931)], 28: [(0.370278, 0.307753)], 29: [(0.799079, 0.345346)], 30: [(0.765326, 0.259846)],
	31: [(0.861784, 0.616648)], 32: [(0.719565, 0.694476)], 51: [(0.838793, 0.093755)], 52: [(0.393808, 0.101018)],
	53: [(0.719565, 0.694476)], 54: [(0.405036, 0.174300)], 55: [(0.938608, 0.565702)],
	56: [(0.780084, 0.019541)], 57: [(0.056424, 0.251087)],
}

PREMIUM_SOLENOID_OBJECTS = {
	2: "Plunger", 3: "Kicker.sw49", 4: "LeftFlipperMini", 5: "RightFlipperMini", 9: "Bumper.Bumper1", 10: "Bumper.Bumper2",
	11: "Bumper.Bumper3", 12: "Kicker.Sw37", 13: "LeftSlingshot collision polygon centroid", 14: "RightSlingshot collision polygon centroid",
	15: "LeftFlipper", 16: "RightFlipper", 17: "Light.f17 (f17a/f17b/f17c/f17r collapsed)", 18: "Primitive.Detonator",
	19: "Light.f19 + Light.f19a", 20: "Light.f20", 21: "Primitive.Flasherbase1 (custom FlashSol121 helper stack collapsed)",
	23: "Light.f23", 25: "Bumper.Bumper1 + Bumper.Bumper2 + Bumper.Bumper3 (f25/f25a helpers collapsed)", 26: "Flasher.f26",
	27: "Light.f27", 28: "Light.f28", 29: "Light.f29", 30: "Light.f30", 31: "Primitive.Flasherbase2 (custom FlashSol131 helper stack collapsed)",
	32: "Primitive.Cannon_assyM", 51: "BandToy collection: Figure_Angus/Figure_Malcolm/Figure_Brian/Figure_Cliff/Figure_DrumL/Figure_DrumR centroid",
	52: "Kicker.sw36", 53: "Primitive.Cannon_assyM", 54: "Primitive.Bell + Kicker.BellK assembly anchor", 55: "Wall.DiverterR collision polygon centroid",
	56: "Gate", 57: "Wall.DiverterL collision polygon centroid",
}

PREMIUM_LAMP_POSITIONS = {
	1: [(0.326540, 0.760931)], 2: [(0.367895, 0.787139)], 3: [(0.387924, 0.817990)], 4: [(0.453373, 0.756396)], 5: [(0.455285, 0.782809)],
	6: [(0.454868, 0.805037)], 7: [(0.454813, 0.828130)], 8: [(0.455139, 0.852813)], 9: [(0.522902, 0.818113)], 10: [(0.541142, 0.788457)],
	11: [(0.579113, 0.760943)], 12: [(0.058112, 0.686331)], 13: [(0.135166, 0.674527)], 14: [(0.239494, 0.673296)],
	17: [(0.207752, 0.467584)], 18: [(0.198625, 0.495306)], 19: [(0.186036, 0.522420)], 20: [(0.175770, 0.548832)], 21: [(0.166343, 0.575612)],
	22: [(0.253050, 0.384128)], 23: [(0.389942, 0.360839)], 24: [(0.506779, 0.402420)], 25: [(0.284021, 0.511266)], 32: [(0.077454, 0.124886)],
	33: [(0.809280, 0.538117)], 34: [(0.808695, 0.510719)], 35: [(0.808695, 0.483100)], 36: [(0.807994, 0.455522)], 37: [(0.626326, 0.510706)],
	38: [(0.699287, 0.472371)], 40: [(0.880644, 0.303228)], 41: [(0.761081, 0.390743)], 42: [(0.670254, 0.671654)], 43: [(0.772419, 0.674986)],
	44: [(0.851339, 0.686040)], 49: [(0.494674, 0.346085)], 50: [(0.552000, 0.355585)], 51: [(0.611106, 0.366080)],
	62: [(0.527584, 0.157574)], 63: [(0.737879, 0.153151)], 64: [(0.638627, 0.237613)],
	81: [(0.452546, 0.604119)], 82: [(0.452546, 0.604119)], 83: [(0.452546, 0.604119)], 84: [(0.420097, 0.224992)], 85: [(0.420097, 0.224992)], 86: [(0.420097, 0.224992)],
	87: [(0.636148, 0.038464)], 88: [(0.636148, 0.038464)], 89: [(0.636148, 0.038464)],
	90: [(0.638408, 0.013355)], 91: [(0.638408, 0.013355)], 92: [(0.638408, 0.013355)], 93: [(0.850918, 0.354409)], 94: [(0.850918, 0.354409)], 95: [(0.850918, 0.354409)],
	96: [(0.435435, 0.283146)], 97: [(0.435435, 0.283146)], 98: [(0.435435, 0.283146)], 99: [(0.547039, 0.047947)], 100: [(0.547039, 0.047947)], 101: [(0.547039, 0.047947)],
	102: [(0.692629, 0.380988)], 103: [(0.692629, 0.380988)], 104: [(0.692629, 0.380988)], 105: [(0.181135, 0.383104)], 106: [(0.181135, 0.383104)], 107: [(0.181135, 0.383104)],
	108: [(0.812724, 0.408981)], 109: [(0.812724, 0.408981)], 110: [(0.812724, 0.408981)], 111: [(0.132385, 0.301140)], 112: [(0.132385, 0.301140)], 113: [(0.132385, 0.301140)],
	117: [(0.519588, 0.533498)], 118: [(0.519588, 0.533498)], 119: [(0.519588, 0.533498)], 120: [(0.386655, 0.534119)], 121: [(0.386655, 0.534119)], 122: [(0.386655, 0.534119)],
	123: [(0.323505, 0.372206)], 124: [(0.323505, 0.372206)], 125: [(0.323505, 0.372206)], 126: [(0.727537, 0.029127)], 127: [(0.727537, 0.029127)], 128: [(0.727537, 0.029127)],
	151: [(0.941607, 0.219490)], 152: [(0.909892, 0.220982)], 153: [(0.941607, 0.271819)], 154: [(0.941607, 0.322657)],
	155: [(0.909892, 0.322657)], 156: [(0.941607, 0.375512)], 157: [(0.970626, 0.374019)], 158: [(0.970626, 0.271819)],
}

PREMIUM_LAMP_OBJECTS = {
	1: "Light.l41", 2: "Light.l42", 3: "Light.l43", 4: "Light.l44", 5: "Light.l45", 6: "Light.l46", 7: "Light.l47", 8: "Light.l48",
	9: "Light.l51", 10: "Light.l50", 11: "Light.l49", 12: "Light.l3", 13: "Light.l4", 14: "Light.l5", 17: "Light.l9", 18: "Light.l10",
	19: "Light.l11", 20: "Light.l12", 21: "Light.l13", 22: "Light.l19", 23: "Light.l21", 24: "Light.l25", 25: "Light.l1", 32: "Flasher.f32",
	33: "Light.l33", 34: "Light.l32", 35: "Light.l31", 36: "Light.l30", 37: "Light.l2", 38: "Light.l34", 40: "Light.l27", 41: "Light.l64",
	42: "Light.l6", 43: "Light.l7", 44: "Light.l8", 49: "Light.l22", 50: "Light.l23", 51: "Light.l24",
	62: "Light.l60 (l60a/l60b collapsed)", 63: "Light.l61 (l61a/l61b collapsed)", 64: "Light.l62 (l62a/l62b collapsed)",
	81: "Light.l17 RGB insert (81-83 collapsed)", 82: "Light.l17 RGB insert (81-83 collapsed)", 83: "Light.l17 RGB insert (81-83 collapsed)",
	84: "Light.l35 RGB insert (84-86 collapsed)", 85: "Light.l35 RGB insert (84-86 collapsed)", 86: "Light.l35 RGB insert (84-86 collapsed)",
	87: "Light.l38 RGB insert; Primitive.p38 helper excluded (87-89 collapsed)", 88: "Light.l38 RGB insert; Primitive.p38 helper excluded (87-89 collapsed)", 89: "Light.l38 RGB insert; Primitive.p38 helper excluded (87-89 collapsed)",
	90: "Light.l40 RGB insert; l40a reflection helper excluded (90-92 collapsed)", 91: "Light.l40 RGB insert; l40a reflection helper excluded (90-92 collapsed)", 92: "Light.l40 RGB insert; l40a reflection helper excluded (90-92 collapsed)",
	93: "Light.l28 RGB insert; p28 helper excluded (93-95 collapsed)", 94: "Light.l28 RGB insert; p28 helper excluded (93-95 collapsed)", 95: "Light.l28 RGB insert; p28 helper excluded (93-95 collapsed)",
	96: "Light.l36 RGB insert; p36 helper excluded (96-98 collapsed)", 97: "Light.l36 RGB insert; p36 helper excluded (96-98 collapsed)", 98: "Light.l36 RGB insert; p36 helper excluded (96-98 collapsed)",
	99: "Light.l37 RGB insert; p37 helper excluded (99-101 collapsed)", 100: "Light.l37 RGB insert; p37 helper excluded (99-101 collapsed)", 101: "Light.l37 RGB insert; p37 helper excluded (99-101 collapsed)",
	102: "Light.l26 RGB insert; p26 helper excluded (102-104 collapsed)", 103: "Light.l26 RGB insert; p26 helper excluded (102-104 collapsed)", 104: "Light.l26 RGB insert; p26 helper excluded (102-104 collapsed)",
	105: "Light.l18 RGB insert; p18 helper excluded (105-107 collapsed)", 106: "Light.l18 RGB insert; p18 helper excluded (105-107 collapsed)", 107: "Light.l18 RGB insert; p18 helper excluded (105-107 collapsed)",
	108: "Light.l29 RGB insert; p29 helper excluded (108-110 collapsed)", 109: "Light.l29 RGB insert; p29 helper excluded (108-110 collapsed)", 110: "Light.l29 RGB insert; p29 helper excluded (108-110 collapsed)",
	111: "Light.l52 RGB insert; p52 helper excluded (111-113 collapsed)", 112: "Light.l52 RGB insert; p52 helper excluded (111-113 collapsed)", 113: "Light.l52 RGB insert; p52 helper excluded (111-113 collapsed)",
	117: "Light.l15 RGB insert (117-119 collapsed)", 118: "Light.l15 RGB insert (117-119 collapsed)", 119: "Light.l15 RGB insert (117-119 collapsed)",
	120: "Light.l14 RGB insert (120-122 collapsed)", 121: "Light.l14 RGB insert (120-122 collapsed)", 122: "Light.l14 RGB insert (120-122 collapsed)",
	123: "Light.l20 RGB insert (123-125 collapsed)", 124: "Light.l20 RGB insert (123-125 collapsed)", 125: "Light.l20 RGB insert (123-125 collapsed)",
	126: "Light.l39 RGB insert; l39a reflection helper excluded (126-128 collapsed)", 127: "Light.l39 RGB insert; l39a reflection helper excluded (126-128 collapsed)", 128: "Light.l39 RGB insert; l39a reflection helper excluded (126-128 collapsed)",
	151: "Flasher.l151", 152: "Flasher.l152", 153: "Flasher.l153", 154: "Flasher.l154", 155: "Flasher.l155", 156: "Flasher.l156", 157: "Flasher.l157", 158: "Flasher.l158",
}

PREMIUM_GI_POSITIONS = {
	130: [(0.901167, 0.467439), (0.875769, 0.581635), (0.044641, 0.487399), (0.649870, 0.299535), (0.783197, 0.293212), (0.049740, 0.287717), (0.190012, 0.240413), (0.148717, 0.158679), (0.892352, 0.414196), (0.689985, 0.823198), (0.218318, 0.824711)],
	132: [(0.327029, 0.123126), (0.785307, 0.194835), (0.350156, 0.239405), (0.052235, 0.429373), (0.032593, 0.598612), (0.895553, 0.525139), (0.099195, 0.411135), (0.696842, 0.757951), (0.205526, 0.758530)],
	134: [(0.667721, 0.549967), (0.597674, 0.669091), (0.309516, 0.671329), (0.232448, 0.554047), (0.322225, 0.429759), (0.579557, 0.432537)],
	136: [(0.833344, 0.124335), (0.249667, 0.110978), (0.246148, 0.153287), (0.172954, 0.136491), (0.348911, 0.211091), (0.541448, 0.282416), (0.355338, 0.270601), (0.205033, 0.288471), (0.052964, 0.371272), (0.757533, 0.228582), (0.900181, 0.495610), (0.463190, 0.102380), (0.498347, 0.087139), (0.587473, 0.077140), (0.677785, 0.068212), (0.768329, 0.059009), (0.498029, 0.091232), (0.588290, 0.083108), (0.677970, 0.074460), (0.766485, 0.063192), (0.757997, 0.801703), (0.146136, 0.802499), (0.720782, 0.695926), (0.181086, 0.697128)],
}

PREMIUM_GI_COLLECTIONS = {
	130: "GI_Red direct Light members: 11 playfield emitters placed; two rear-panel bulbs intentionally omitted from playfield coordinates; non-Light helpers excluded",
	132: "GI_Blue direct Light members: nine playfield emitters placed; one rear-panel bulb intentionally omitted from playfield coordinates; non-Light helpers excluded",
	134: "GI_LowPf direct Light members (6); non-Light helpers excluded",
	136: "GI_White direct Light members: 24 playfield emitters placed; four rear-panel bulbs intentionally omitted from playfield coordinates; ShadowGI flasher helper excluded",
}

PREMIUM_GI_PHYSICAL_QUANTITIES = {130: 13, 132: 10, 134: 6, 136: 28}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _annotate(device: dict[str, object], note: str) -> None:
	physical = device.setdefault("physical", {})
	previous = physical.get("notes")
	physical["notes"] = f"{previous} {note}" if isinstance(previous, str) and previous else note


def _located(
	device: dict[str, object],
	role: str,
	positions: list[tuple[float, float]],
	source_refs: tuple[str, ...],
	note: str | None = None,
) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "validated", "placements": placements}
	if note:
		_annotate(device, note)


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str, role: str | None = None, note: str | None = None) -> None:
	if role:
		roles = device.setdefault("roles", [])
		if role not in roles:
			roles.append(role)
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}
	if note:
		_annotate(device, note)


def _apply_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	input_positions: dict[int, list[tuple[float, float]]],
	lamp_positions: dict[int, list[tuple[float, float]]],
	gi_positions: list[tuple[float, float]],
	located_sources: tuple[str, ...],
	manual_source: str,
	core_source: str,
	switch36_sources: tuple[str, ...] | None = None,
) -> None:
	"""Apply a fail-closed, manually reviewed spatial disposition to every device."""
	for device in inputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", manual_source)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif address in input_positions:
			spatial_sources = switch36_sources if switch36_sources is not None and group == "pinmame.input.switch" and address == 36 else located_sources
			_located(device, "sensor", input_positions[address], spatial_sources)
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", manual_source)
		else:
			raise ValueError(f"AC/DC input {group} {address} has no reviewed spatial disposition")
		if group == "pinmame.input.switch" and address in {18, 19, 20, 21, 22}:
			physical = device.setdefault("physical", {})
			physical["location"] = "Under-apron four-ball trough assembly 500-6318-24-ND"
		if group == "pinmame.input.switch" and address in {61, 62}:
			device.setdefault("physical", {})["location"] = "Rotating cannon motor-and-switch assembly"

	for device in outputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif kind == "virtual":
			_not_applicable(device, "virtual", core_source)
		elif group == "pinmame.output.lamp" and address in {1, 2, 63}:
			device["roles"] = [{1: "cabinet.start", 2: "cabinet.tournament", 63: "cabinet.fire"}[address]]
			_not_applicable(device, "cabinet_or_service", manual_source)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			_not_applicable(device, "cabinet_or_service", manual_source)
			if group == "pinmame.output.solenoid" and address == 22:
				device.setdefault("physical", {}).update({"quantity": 1, "location": "Rear-panel right flasher fixture", "notes": "The official coil/location chart proves one physical rear-panel flasher bulb outside normalized playfield space; no playfield coordinate is asserted."})
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], located_sources)
			if address == 25:
				device.setdefault("physical", {})["quantity"] = 3
		elif group == "pinmame.output.lamp" and address in REAR_PANEL_LAMP_ADDRESSES:
			device["roles"] = ["cabinet.rear-panel"]
			_not_applicable(device, "cabinet_or_service", manual_source)
			device.setdefault("physical", {}).update({"quantity": 1, "location": "Rear-panel song/track lamp assembly", "notes": "The official lamp-location chart proves one physical rear-panel lamp at this address outside normalized playfield space; no playfield coordinate is asserted."})
		elif group == "pinmame.output.lamp" and address in lamp_positions:
			_located(device, "emitter", lamp_positions[address], located_sources)
		elif group == "pinmame.output.gi" and address == 0:
			if len(gi_positions) != 38:
				raise ValueError(f"AC/DC reviewed playfield GI map must contain 38 placements, got {len(gi_positions)}")
			_located(device, "emitter", gi_positions, located_sources)
			device.setdefault("physical", {}).update({"quantity": 45, "notes": "One conventional GI channel drives 38 reviewed playfield bulbs and seven off-playfield back-panel bulbs. Only the 38 playfield bulbs receive normalized coordinates."})
		else:
			raise ValueError(f"AC/DC output {group} {address} ({kind}) has no reviewed spatial disposition")


def apply_vault_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	table_source: str,
	script_source: str,
	manual_source: str,
	core_source: str,
) -> None:
	"""Apply the reviewed normalized spatial disposition to every Vault device."""
	located_sources = (table_source, script_source, manual_source)
	_apply_spatial(
		inputs,
		outputs,
		input_positions=INPUT_POSITIONS,
		lamp_positions=LAMP_POSITIONS,
		gi_positions=GI_POSITIONS,
		located_sources=located_sources,
		manual_source=manual_source,
		core_source=core_source,
	)


def apply_original_pro_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	table_source: str,
	script_source: str,
	manual_source: str,
	core_source: str,
) -> None:
	"""Apply the reviewed normalized spatial disposition to the original Pro."""
	located_sources = (table_source, script_source, manual_source)
	_apply_spatial(
		inputs,
		outputs,
		input_positions=ORIGINAL_PRO_INPUT_POSITIONS,
		lamp_positions=ORIGINAL_PRO_LAMP_POSITIONS,
		gi_positions=LED_PRO_GI_POSITIONS,
		located_sources=located_sources,
		manual_source=manual_source,
		core_source=core_source,
	)


def apply_led_pro_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	table_source: str,
	script_source: str,
	manual_source: str,
	core_source: str,
	bell_table_source: str,
	bell_script_source: str,
	identity_source: str,
) -> None:
	"""Apply the reviewed normalized spatial disposition to every LED Pro device."""
	_apply_spatial(
		inputs,
		outputs,
		input_positions=INPUT_POSITIONS,
		lamp_positions=LED_PRO_LAMP_POSITIONS,
		gi_positions=LED_PRO_GI_POSITIONS,
		located_sources=(table_source, script_source, manual_source),
		switch36_sources=(bell_table_source, bell_script_source, identity_source),
		manual_source=manual_source,
		core_source=core_source,
	)


def apply_premium_luci_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	table_source: str,
	script_source: str,
	premium_manual_source: str,
	luci_manual_source: str,
	core_source: str,
) -> None:
	"""Apply the exact LUCI v15 mechanical first draft to Premium-family devices.

	The v15 table is the source of object identity and controller causality. The
	manuals control physical multiplicity and cabinet/back-panel disposition. A
	missing physical plane is deliberately represented as N/A rather than a
	projected playfield coordinate.
	"""
	located_sources = (table_source, script_source, premium_manual_source, luci_manual_source)
	manual_sources = (premium_manual_source, luci_manual_source)

	for device in inputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", *manual_sources)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", *manual_sources)
		elif address in PREMIUM_INPUT_POSITIONS:
			_located(device, "sensor", PREMIUM_INPUT_POSITIONS[address], located_sources, PREMIUM_INPUT_OBJECTS[address])
		elif address in {18, 19, 20, 21, 22}:
			_not_applicable(
				device,
				"internal_nonvisual",
				*manual_sources,
				role="internal.trough",
				note="Sw18-Sw22 are the under-apron four-ball trough assembly; no playfield XY is asserted.",
			)
		elif address == 64:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.fire", note="Cabinet FIRE button; no playfield XY.")
		elif address == 15:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.tournament", note="Cabinet tournament/start button; no playfield XY.")
		elif address == 16:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.start", note="Cabinet start button; no playfield XY.")
		elif address in {65, 66, 67, 68, 69}:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.coin", note="Cabinet coin-chute input; no playfield XY.")
		elif address in {81, 82, 83, 84, 86, 88}:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.flipper", note="Dedicated cabinet flipper button/EOS input; no playfield XY.")
		elif address in CABINET_INPUT_ROLES:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role=CABINET_INPUT_ROLES[address], note="Cabinet/service input; no playfield XY.")
		else:
			raise ValueError(f"AC/DC Premium input {group} {address} has no reviewed spatial disposition")
		if group == "pinmame.input.switch" and address in {18, 19, 20, 21, 22}:
			physical = device.setdefault("physical", {})
			physical["location"] = "Under-apron four-ball trough assembly 500-6318-24-ND"
			physical["assembly_part_number"] = "500-6318-24-ND"
		if group == "pinmame.input.switch" and address in {61, 62}:
			device.setdefault("physical", {})["location"] = "Rotating cannon motor-and-switch assembly"

	for device in outputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_not_applicable(device, "unused", *manual_sources)
		elif kind == "virtual":
			_not_applicable(device, "virtual", core_source)
		elif group == "physical.output.ticket":
			device["roles"] = ["service.ticket"]
			_not_applicable(device, "cabinet_or_service", *manual_sources, note="Optional ticket/service output; no playfield XY.")
		elif group == "pinmame.output.solenoid" and address in {8, 24}:
			role = CABINET_OUTPUT_ROLES[(group, address)]
			_not_applicable(device, "cabinet_or_service", *manual_sources, role=role, note="Cabinet/service hardware; no playfield XY.")
		elif group == "pinmame.output.solenoid" and address == 22:
			_not_applicable(device, "cabinet_or_service", *manual_sources, role="cabinet.rear-panel", note="Manual and script identify output 22 as the back-panel flasher; no playfield XY.")
		elif group == "pinmame.output.solenoid" and address in {1, 6, 7}:
			roles = {1: "internal.trough", 6: "internal.drop-bank-reset", 7: "internal.drop-bank-reset"}
			notes = {
				1: "Solenoid 1 is the under-apron trough up-kicker; no playfield XY.",
				6: "Solenoid 6 resets the five-bank drop-target hardware; coil location is internal and no playfield XY is asserted.",
				7: "Solenoid 7 resets the three-bank drop-target hardware; coil location is internal and no playfield XY is asserted.",
			}
			_not_applicable(device, "internal_nonvisual", *manual_sources, role=roles[address], note=notes[address])
			if address == 1:
				device.setdefault("physical", {})["assembly_part_number"] = "500-6318-24-ND"
			elif address == 6:
				device.setdefault("physical", {})["quantity"] = 2
		elif group == "pinmame.output.solenoid" and address in PREMIUM_SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			_located(device, role, PREMIUM_SOLENOID_POSITIONS[address], located_sources, PREMIUM_SOLENOID_OBJECTS[address])
			if address in {19, 25}:
				device.setdefault("physical", {})["quantity"] = len(PREMIUM_SOLENOID_POSITIONS[address])
		elif group == "pinmame.output.lamp" and address in {57, 58, 59, 60, 61}:
			roles = {57: "cabinet.start", 58: "cabinet.tournament", 59: "cabinet.fire", 60: "cabinet.fire", 61: "cabinet.fire"}
			_not_applicable(device, "cabinet_or_service", *manual_sources, role=roles[address], note="Cabinet button lamp; no playfield XY.")
		elif group == "pinmame.output.lamp" and address in {53, 54, *range(65, 77)}:
			_not_applicable(
				device,
				"cabinet_or_service",
				*manual_sources,
				role="cabinet.rear-panel",
				note="Manual location sheet identifies this as a rear-panel lamp; no playfield XY is asserted.",
			)
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.lamp" and address in PREMIUM_LAMP_POSITIONS:
			_located(device, "emitter", PREMIUM_LAMP_POSITIONS[address], located_sources, PREMIUM_LAMP_OBJECTS[address])
		elif group == "pinmame.output.lamp" and address in PREMIUM_GI_POSITIONS:
			_located(device, "emitter", PREMIUM_GI_POSITIONS[address], located_sources, PREMIUM_GI_COLLECTIONS[address])
			device.setdefault("physical", {})["quantity"] = PREMIUM_GI_PHYSICAL_QUANTITIES[address]
		elif group == "pinmame.output.gi" and address == 0:
			_not_applicable(
				device,
				"internal_nonvisual",
				script_source,
				*manual_sources,
				role="internal.compatibility",
				note="Exact v15 script declares UseGI=0 and provides no direct GI-0 object map, so this compatibility channel has no playfield placement.",
			)
		else:
			raise ValueError(f"AC/DC Premium output {group} {address} ({kind}) has no reviewed spatial disposition")
