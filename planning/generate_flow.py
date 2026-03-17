import json

def create_rect(id, x, y, w, h, bg="transparent", border="#000000", dashed=False):
    return {"type": "rectangle", "version": 1, "versionNonce": 1, "isDeleted": False, "id": id, "fillStyle": "hachure", "strokeWidth": 1, "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "angle": 0, "x": x, "y": y, "strokeColor": border, "backgroundColor": bg, "width": w, "height": h, "seed": 1, "groupIds": [], "boundElements": []}

def create_text(id, x, y, text, size=16, color="#000000"):
    width = len(text) * (size * 0.55)
    return {"type": "text", "version": 1, "versionNonce": 1, "isDeleted": False, "id": id, "fillStyle": "hachure", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100, "angle": 0, "x": x, "y": y, "strokeColor": color, "backgroundColor": "transparent", "width": width, "height": size * 1.25, "seed": 1, "groupIds": [], "fontSize": size, "fontFamily": 1, "text": text, "textAlign": "left", "verticalAlign": "top", "originalText": text, "boundElements": []}

def create_arrow(id, x, y, dx, dy):
    return {"type": "arrow", "version": 1, "versionNonce": 1, "isDeleted": False, "id": id, "fillStyle": "hachure", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100, "angle": 0, "x": x, "y": y, "strokeColor": "#3b82f6", "backgroundColor": "transparent", "width": abs(dx), "height": abs(dy), "seed": 1, "groupIds": [], "points": [[0,0], [dx, dy]], "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow"}

ux_schema = {"type": "excalidraw", "version": 2, "source": "antigravity", "elements": []}
els = []

# View 1: Default State
els.append(create_text("t1", 50, 20, "1. Default View (No Popups)", 20))
els.append(create_rect("app1", 50, 50, 600, 450))
els.append(create_rect("app1_side", 200, 50, 2, 450))
els.append(create_text("app1_tasks", 60, 70, "Tasks", 18))
els.append(create_text("app1_t1", 60, 110, "▶ Learn Python", 16, "#3b82f6"))
els.append(create_text("app1_t2", 60, 140, "   Read Book", 16))

els.append(create_text("app1_main", 220, 70, "Active: Learn Python", 24))
els.append(create_text("app1_sw", 380, 110, "00:45:12", 32))
els.append(create_rect("app1_start", 300, 160, 80, 30, "#dcfce7", "#22c55e"))
els.append(create_text("app1_start_t", 320, 165, "Start", 14, "#15803d"))
els.append(create_rect("app1_save", 450, 160, 80, 30, "#dbeafe", "#3b82f6"))
els.append(create_text("app1_save_t", 470, 165, "Save", 14, "#1d4ed8"))

# History Area inside the same window
els.append(create_rect("app1_hist_area", 220, 230, 410, 250, "transparent", "#94a3b8", True))
els.append(create_text("app1_hist_ttl", 230, 240, "Recent History", 16))
# Existing Row
els.append(create_rect("app1_row", 230, 270, 390, 30, "#f1f5f9", "#cbd5e1"))
els.append(create_text("app1_row_date", 240, 275, "2026-03-09", 14))
els.append(create_text("app1_row_dur", 370, 275, "45 mins", 14))
els.append(create_rect("app1_row_edit", 520, 273, 40, 24, "#ffffff", "#3b82f6"))
els.append(create_text("app1_row_edit_t", 525, 276, "Edit", 12, "#3b82f6"))
els.append(create_rect("app1_row_del", 570, 273, 40, 24, "#ffffff", "#ef4444"))
els.append(create_text("app1_row_del_t", 575, 276, "Del", 12, "#ef4444"))


# View 2: Inline Edit State
els.append(create_text("t2", 750, 20, "2. Inline Edit State (Changes in-place, NO popups)", 20))
els.append(create_rect("app2", 750, 50, 600, 450))
els.append(create_rect("app2_side", 900, 50, 2, 450))
els.append(create_text("app2_tasks", 760, 70, "Tasks", 18))
els.append(create_text("app2_t1", 760, 110, "▶ Learn Python", 16, "#3b82f6"))
els.append(create_text("app2_t2", 760, 140, "   Read Book", 16))

els.append(create_text("app2_main", 920, 70, "Active: Learn Python", 24))
els.append(create_text("app2_sw", 1080, 110, "00:45:12", 32))
els.append(create_rect("app2_start", 1000, 160, 80, 30, "#dcfce7", "#22c55e"))
els.append(create_text("app2_start_t", 1020, 165, "Start", 14, "#15803d"))
els.append(create_rect("app2_save", 1150, 160, 80, 30, "#dbeafe", "#3b82f6"))
els.append(create_text("app2_save_t", 1170, 165, "Save", 14, "#1d4ed8"))

# History Area (Editable)
els.append(create_rect("app2_hist_area", 920, 230, 410, 250, "transparent", "#94a3b8", True))
els.append(create_text("app2_hist_ttl", 930, 240, "Recent History", 16))
# Editable Row expands
els.append(create_rect("app2_row", 930, 270, 390, 80, "#eef2ff", "#818cf8"))
els.append(create_text("app2_row_date", 940, 280, "Date: [ 2026-03-09 ]", 14))
els.append(create_text("app2_row_dur", 1120, 280, "Duration: [ 45 ] mins", 14))
els.append(create_rect("app2_row_save", 1130, 310, 80, 30, "#c7d2fe", "#4f46e5"))
els.append(create_text("app2_row_save_t", 1145, 315, "Update", 14, "#3730a3"))
els.append(create_rect("app2_row_canc", 1220, 310, 80, 30, "#fee2e2", "#ef4444"))
els.append(create_text("app2_row_canc_t", 1235, 315, "Cancel", 14, "#b91c1c"))

# Arrow explaining click
els.append(create_arrow("arrow_edit", 600, 285, 330, 0))
els.append(create_text("arrow_text", 650, 260, "Clicking 'Edit'\nExpands the row inline", 14, "#3b82f6"))

ux_schema["elements"] = els
with open(r"c:\DEV\Tracking_app\planning\ux_flow.excalidraw", "w") as f:
    json.dump(ux_schema, f, indent=2)

print("UX Interaction Flow drawn successfully.")
