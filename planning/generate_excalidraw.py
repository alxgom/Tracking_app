import json
import uuid

def create_rect(id, x, y, w, h, bg="transparent", border="#000000", dashed=False):
    return {
      "type": "rectangle",
      "version": 1,
      "versionNonce": 1,
      "isDeleted": False,
      "id": id,
      "fillStyle": "hachure",
      "strokeWidth": 1,
      "strokeStyle": "dashed" if dashed else "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "x": x,
      "y": y,
      "strokeColor": border,
      "backgroundColor": bg,
      "width": w,
      "height": h,
      "seed": 1,
      "groupIds": [],
      "boundElements": []
    }

def create_text(id, x, y, text, size=16, color="#000000"):
    width = len(text) * (size * 0.55)
    return {
      "type": "text",
      "version": 1,
      "versionNonce": 1,
      "isDeleted": False,
      "id": id,
      "fillStyle": "hachure",
      "strokeWidth": 1,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "x": x,
      "y": y,
      "strokeColor": color,
      "backgroundColor": "transparent",
      "width": width,
      "height": size * 1.25,
      "seed": 1,
      "groupIds": [],
      "fontSize": size,
      "fontFamily": 1,
      "text": text,
      "textAlign": "left",
      "verticalAlign": "top",
      "originalText": text,
      "boundElements": []
    }

def create_arrow(id, x, y, dx, dy, start=None, end=None):
    return {
      "type": "arrow",
      "version": 1,
      "versionNonce": 1,
      "isDeleted": False,
      "id": id,
      "fillStyle": "hachure",
      "strokeWidth": 1,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "x": x,
      "y": y,
      "strokeColor": "#000000",
      "backgroundColor": "transparent",
      "width": abs(dx),
      "height": abs(dy),
      "seed": 1,
      "groupIds": [],
      "points": [[0,0], [dx, dy]],
      "startBinding": start,
      "endBinding": end,
      "startArrowhead": None,
      "endArrowhead": "arrow"
    }

# DB Schema
db_schema = {
  "type": "excalidraw",
  "version": 2,
  "source": "antigravity",
  "elements": []
}
db_els = []
db_els.append(create_rect("t-tasks", 100, 100, 250, 260))
db_els.append(create_text("tt-tasks", 110, 110, "Table: Tasks", 20))
db_els.append(create_text("tt-t1", 110, 150, "PK id (INTEGER)", 16, "#e03e3e"))
db_els.append(create_text("tt-t2", 110, 180, "name (VARCHAR)", 16))
db_els.append(create_text("tt-t3", 110, 210, "color (VARCHAR)", 16))
db_els.append(create_text("tt-t4", 110, 240, "is_archived (BOOLEAN)", 16))
db_els.append(create_text("tt-t5", 110, 270, "sort_order (INTEGER)", 16))
db_els.append(create_text("tt-t6", 110, 300, "created_at (DATETIME)", 16))

db_els.append(create_rect("t-logs", 500, 100, 300, 210))
db_els.append(create_text("tl-logs", 510, 110, "Table: TimeLogs", 20))
db_els.append(create_text("tl-l1", 510, 150, "PK id (INTEGER)", 16, "#e03e3e"))
db_els.append(create_text("tl-l2", 510, 180, "FK task_id (INTEGER)", 16, "#2f9e44"))
db_els.append(create_text("tl-l3", 510, 210, "date (DATE)", 16))
db_els.append(create_text("tl-l4", 510, 240, "duration_minutes (INT)", 16))
db_els.append(create_arrow("arr-1", 500, 190, -150, -40, {"elementId": "t-logs", "focus": 0.5, "gap": 1}, {"elementId": "t-tasks", "focus": -0.5, "gap": 1}))
db_els.append(create_text("rel", 370, 140, "1 to Many", 14))

db_schema["elements"] = db_els
with open(r"c:\DEV\Tracking_app\planning\db_schema.excalidraw", "w") as f:
    json.dump(db_schema, f, indent=2)

# UX Wireframe
ux_schema = {
  "type": "excalidraw",
  "version": 2,
  "source": "antigravity",
  "elements": []
}
ux_els = []
ux_els.append(create_rect("app", 50, 50, 800, 600))
ux_els.append(create_rect("line", 250, 50, 2, 600))
ux_els.append(create_text("side", 60, 70, "My Tasks", 20))
ux_els.append(create_rect("t1", 60, 120, 170, 40, "#e2e8f0"))
ux_els.append(create_text("t1_t", 70, 130, "Learn Python", 16))
ux_els.append(create_rect("t2", 60, 170, 170, 40))
ux_els.append(create_text("t2_t", 70, 180, "Read a Book", 16))
ux_els.append(create_rect("btn-add", 60, 590, 170, 40, "transparent", "#3b82f6", True))
ux_els.append(create_text("btn-add-txt", 110, 600, "+ Add Task", 16, "#3b82f6"))

ux_els.append(create_text("main-t", 280, 70, "Active: Learn Python", 28))
ux_els.append(create_rect("stopwatch", 280, 130, 540, 180))
ux_els.append(create_text("sw-time", 420, 160, "00:45:12", 40))

ux_els.append(create_rect("b1", 350, 240, 100, 40, "#dcfce7", "#22c55e"))
ux_els.append(create_text("b1-t", 380, 250, "Start", 16, "#15803d"))
ux_els.append(create_rect("b2", 480, 240, 100, 40, "#fee2e2", "#ef4444"))
ux_els.append(create_text("b2-t", 510, 250, "Stop", 16, "#b91c1c"))
ux_els.append(create_rect("b3", 610, 240, 100, 40, "#dbeafe", "#3b82f6"))
ux_els.append(create_text("b3-t", 640, 250, "Save", 16, "#1d4ed8"))

ux_els.append(create_rect("manual", 280, 340, 540, 80, "transparent", "#000000", True))
ux_els.append(create_text("manual-t", 290, 350, "Manual Entry (After the fact):", 14))
ux_els.append(create_rect("m-date", 290, 375, 120, 30, "transparent", "#64748b"))
ux_els.append(create_text("m-date-t", 300, 380, "2026-03-09", 14, "#64748b"))
ux_els.append(create_rect("m-dur", 430, 375, 100, 30, "transparent", "#64748b"))
ux_els.append(create_text("m-dur-t", 440, 380, "45 mins", 14, "#64748b"))
ux_els.append(create_rect("btn-m-save", 550, 375, 80, 30, "transparent", "#3b82f6"))
ux_els.append(create_text("b-m-s-t", 575, 380, "Add", 14, "#3b82f6"))

ux_els.append(create_rect("chart", 280, 440, 540, 190))
ux_els.append(create_text("chart-t", 460, 520, "[ Chart Area ]", 20, "#94a3b8"))

ux_schema["elements"] = ux_els
with open(r"c:\DEV\Tracking_app\planning\ux_wireframes.excalidraw", "w") as f:
    json.dump(ux_schema, f, indent=2)

print("Done generating proper excalidraw files with text bounding boxes.")
