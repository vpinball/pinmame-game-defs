"""Observed factory-drawing projections for Haunted House's three physical levels.

Pixels were read independently before the reader saw table coordinates. The fits
reconcile plan views; they do not turn a circled label into a physical socket.
"""
from __future__ import annotations

from typing import Any
from pathlib import Path

from drawing_callouts import apply, distance, fit, leave_one_out


def world_object_bounds(path: Path, names: set[str]) -> dict[str, dict[str, Any]]:
	"""Bounds of named meshes in vpxtool's world-space VPU export, not stored pivots."""
	points={name:[] for name in names}
	current=None
	with path.open("rb") as stream:
		for line in stream:
			if line.startswith(b"o "):
				current=line[2:].strip().decode("utf-8")
			elif current in points and line.startswith(b"v "):
				points[current].append(tuple(map(float,line.split()[1:4])))
	result={}
	for name,vertices in points.items():
		if not vertices:
			raise RuntimeError(f"world export lacks mesh {name}")
		bounds=[min(v[i] for v in vertices) for i in range(3)]+[max(v[i] for v in vertices) for i in range(3)]
		result[name]={"bounds":bounds,"vertex_count":len(vertices),"center":[(bounds[i]+bounds[i+3])/2 for i in range(3)]}
	return result


def inside_hull(point: list[float], controls: list[list[float]]) -> bool:
	"""Convex hull, rather than a bounding-box interpolation claim."""
	def cross(o: tuple, a: tuple, b: tuple) -> float:
		return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
	points=sorted(set(map(tuple,controls)))
	low=[]
	for p in points:
		while len(low)>=2 and cross(low[-2],low[-1],p)<=0:
			low.pop()
		low.append(p)

	upper=[]
	for p in reversed(points):
		while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
			upper.pop()
		upper.append(p)
	hull=low[:-1]+upper[:-1]
	return len(hull)>=3 and all(cross(hull[i],hull[(i+1)%len(hull)],tuple(point))>=-1e-6 for i in range(len(hull)))


def plan(facts: dict[str, Any], layout: dict[str, Any]) -> dict[str, Any]:
	result={"format":"haunted-house-drawing-projections","version":1,"frames":{},"measurements":{},
		"policy":"All drawing-derived placements remain observed. Only distinct lamp symbols, the display rectangle and own-mechanism anchors may supply coordinates. Circled/leaderless labels are excluded. No measurement is checked against its own drawing.",
		"excluded_controls":["main rear round opening: identity among nearby openings is ambiguous"],"excluded_lamp_labels":[]}
	for name,frame in layout["frames"].items():
		objects=layout["primary_verification"]["control_objects"][name]
		controls=[]
		for read,obj in zip(frame["controls"],objects):
			point=facts["table_points"][obj]
			controls.append({"pixel":read["pixel"],"object":obj,"xy":[point["x"]/1116,point["y"]/2186],"meaning":read["meaning"]})
		if name=="main":
			read=layout["primary_verification"]["main_additional_control"]
			point=facts["table_points"][read["table_object"]]
			controls.append({"pixel":read["pixel"],"object":read["table_object"],"xy":[point["x"]/1116,point["y"]/2186],"meaning":read["basis"]})
		pairs=[(tuple(c["pixel"]),tuple(c["xy"])) for c in controls]
		transform=fit(pairs)
		span=max(c["xy"][1] for c in controls)-min(c["xy"][1] for c in controls)
		result["frames"][name]={"locator":frame["locator"],"image":frame["image"],"image_sha256":frame["image_sha256"],"image_size_px":frame["image_size_px"],"frame_corners_px_approx":frame["frame_corners_px_approx"],"controls":controls,"transform":transform,"control_y_span":round(span,6),"minimum_full_field_span_met":span>=.5,"control_loo_max":round(max(leave_one_out(pairs)),6),"control_rms":round((sum(distance(apply(transform,p),xy)**2 for p,xy in pairs)/len(pairs))**.5,6)}
		for read in frame["reads"]:
			if not read["label"].startswith("L"):
				continue
			if read["point"]!="symbol_center" or not read["usable_for_part_check"]:
				result["excluded_lamp_labels"].append({"frame":name,"label":read["label"],"pixel":read["pixel"],"reason":"Circled label or leaderless inscription, not a separately located bulb symbol."})
				continue
			xy=apply(transform,read["pixel"])
			if not all(0<=v<=1 for v in xy):
				raise RuntimeError(f"drawing projection outside playfield: {name}, {read}")
			result["measurements"][f"lamp:{int(read['label'][1:])}"]={"frame":name,"pixel":read["pixel"],"xy":[round(v,3) for v in xy],"extrapolated":not inside_hull(read["pixel"],[c["pixel"] for c in controls]),"basis":"Distinct drawn lamp symbol; observed projection, not a measured physical socket."}
	for read in layout["primary_verification"]["primary_measurements"]:
		frame=result["frames"][read["frame"]]
		xy=apply(frame["transform"],read["pixel"])
		if not all(0<=v<=1 for v in xy):
			raise RuntimeError(f"primary drawing projection outside playfield: {read}")
		key="display:8" if read["target"]=="display.monster-bonus" else "switch:67"
		result["measurements"][key]={"frame":read["frame"],"pixel":read["pixel"],"xy":[round(v,3) for v in xy],"extrapolated":not inside_hull(read["pixel"],[c["pixel"] for c in frame["controls"]]),"basis":read["basis"]}
	result["measurements"]["solenoid:9"]={**result["measurements"]["switch:67"],"basis":"Outhole effect projected onto its own drain bar; not an observed winding centre."}
	return result
