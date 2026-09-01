"""Local browser dashboard for the EHC pilot experiment.

No web-framework dependency is required.

Run:
    python pilot/app.py
Then open:
    http://127.0.0.1:5000
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import time
from urllib.parse import parse_qs, urlparse
import uuid

from mission import ACTIONS, generate_experiment


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SESSIONS = {}

LOG_FIELDS = [
    "timestamp_utc","participant_id","session_id","block",
    "false_positive_burden","temporal_pattern","event_id","robot_id",
    "event_type","is_critical","scheduled_at_s","deadline_s",
    "event_status","chosen_action","correct_action","correct","timely",
    "response_latency_s","queue_depth_at_response",
]


def safe_participant_id(raw):
    cleaned = "".join(ch for ch in raw.strip() if ch.isalnum() or ch in "-_")
    if not cleaned:
        raise ValueError("Use a pseudonymous participant ID.")
    return cleaned[:64]


class ExperimentSession:
    def __init__(self, participant_id, demo=False):
        self.participant_id = safe_participant_id(participant_id)
        self.session_id = uuid.uuid4().hex
        self.demo = demo
        self.blocks = generate_experiment(self.participant_id, demo=demo)
        self.block_index = -1
        self.block_started = None
        self.responses = {}
        self.closed_blocks = set()
        self.log_path = DATA_DIR / f"{self.participant_id}_{self.session_id[:8]}.csv"
        with self.log_path.open("w", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=LOG_FIELDS).writeheader()

    @property
    def block(self):
        return self.blocks[self.block_index] if 0 <= self.block_index < len(self.blocks) else None

    def elapsed(self):
        return 0.0 if self.block_started is None else max(0.0, time.monotonic() - self.block_started)

    def start_next_block(self):
        if self.block_started is not None:
            raise ValueError("Current block is still running.")
        if self.block_index + 1 >= len(self.blocks):
            return {"finished": True}
        self.block_index += 1
        self.block_started = time.monotonic()
        return {"finished": False, "block": self.block_index + 1, "total_blocks": len(self.blocks)}

    def arrived_unanswered(self, elapsed):
        if self.block is None:
            return []
        return [e for e in self.block.events if e.scheduled_at_s <= elapsed and e.event_id not in self.responses]

    def public_state(self):
        b = self.block
        if b is None:
            return {"phase":"ready","block":0,"total_blocks":len(self.blocks)}

        if self.block_started is None and b.block in self.closed_blocks:
            phase = "finished" if self.block_index + 1 >= len(self.blocks) else "between_blocks"
            return {"phase":phase,"block":self.block_index+1,"total_blocks":len(self.blocks)}

        elapsed = self.elapsed()
        if self.block_started is not None and elapsed >= b.duration_s:
            self.close_block()
            phase = "finished" if self.block_index + 1 >= len(self.blocks) else "between_blocks"
            return {"phase":phase,"block":self.block_index+1,"total_blocks":len(self.blocks)}

        pending = []
        for e in self.arrived_unanswered(elapsed):
            item = e.public_dict()
            age = elapsed - e.scheduled_at_s
            item.update({"age_s":age,"deadline_remaining_s":e.deadline_s-age,"overdue":age>e.deadline_s})
            pending.append(item)
        pending.sort(key=lambda x: (x["scheduled_at_s"], x["event_id"]))
        return {
            "phase":"running","block":self.block_index+1,"total_blocks":len(self.blocks),
            "remaining_s":max(0.0,b.duration_s-elapsed),"pending":pending,
            "responded_count":sum(e.event_id in self.responses for e in b.events),
            "total_events":len(b.events),
        }

    def respond(self, event_id, action):
        if action not in ACTIONS:
            raise ValueError("Unknown action.")
        if self.block is None or self.block_started is None:
            raise ValueError("No block is running.")
        if event_id in self.responses:
            raise ValueError("Alert already handled.")
        event = next((e for e in self.block.events if e.event_id == event_id), None)
        if event is None:
            raise ValueError("Unknown alert.")
        elapsed = self.elapsed()
        if elapsed < event.scheduled_at_s:
            raise ValueError("Alert has not arrived yet.")
        latency = elapsed - event.scheduled_at_s
        row = self.log_event(event, "responded", action, latency, len(self.arrived_unanswered(elapsed)))
        self.responses[event.event_id] = row
        return {"ok":True,"event_id":event.event_id}

    def close_block(self):
        b = self.block
        if b is None or b.block in self.closed_blocks:
            self.block_started = None
            return
        elapsed = max(b.duration_s, self.elapsed())
        for event in b.events:
            if event.event_id not in self.responses:
                latency = max(0.0, elapsed - event.scheduled_at_s)
                self.responses[event.event_id] = self.log_event(event, "missed", "", latency, 0)
        self.closed_blocks.add(b.block)
        self.block_started = None

    def log_event(self, event, status, action, latency, queue_depth):
        b = self.block
        correct = action == event.correct_action if status == "responded" else False
        timely = latency <= event.deadline_s if status == "responded" else False
        row = {
            "timestamp_utc":datetime.now(timezone.utc).isoformat(),
            "participant_id":self.participant_id,"session_id":self.session_id,
            "block":b.block,"false_positive_burden":b.condition.false_positive_burden,
            "temporal_pattern":b.condition.temporal_pattern,"event_id":event.event_id,
            "robot_id":event.robot_id,"event_type":event.event_type,
            "is_critical":event.is_critical,"scheduled_at_s":round(event.scheduled_at_s,3),
            "deadline_s":event.deadline_s,"event_status":status,"chosen_action":action,
            "correct_action":event.correct_action,"correct":correct,"timely":timely,
            "response_latency_s":round(latency,3),"queue_depth_at_response":queue_depth,
        }
        with self.log_path.open("a", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, fieldnames=LOG_FIELDS).writerow(row)
        return row


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self):
        body = HTML.encode()
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def payload(self):
        n = int(self.headers.get("Content-Length","0") or 0)
        return {} if n == 0 else json.loads(self.rfile.read(n).decode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self.send_html()
        if parsed.path == "/api/state":
            try:
                sid = parse_qs(parsed.query).get("session_id",[None])[0]
                return self.send_json(SESSIONS[sid].public_state())
            except Exception as exc:
                return self.send_json({"error":str(exc)},400)
        return self.send_json({"error":"Not found"},404)

    def do_POST(self):
        try:
            p = self.payload()
            if self.path == "/api/start":
                s = ExperimentSession(p.get("participant_id",""), bool(p.get("demo",False)))
                SESSIONS[s.session_id] = s
                return self.send_json({"session_id":s.session_id,"total_blocks":len(s.blocks),"demo":s.demo})
            s = SESSIONS[p["session_id"]]
            if self.path == "/api/start_block":
                return self.send_json(s.start_next_block())
            if self.path == "/api/respond":
                return self.send_json(s.respond(p["event_id"],p["action"]))
            return self.send_json({"error":"Not found"},404)
        except Exception as exc:
            return self.send_json({"error":str(exc)},400)


HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Multi-Robot Supervision Pilot</title>
<style>
body{font-family:system-ui;margin:0;background:#11151b;color:#eef2f7}
main{max-width:1000px;margin:auto;padding:28px}.panel{background:#1a2029;border:1px solid #303947;border-radius:14px;padding:20px;margin-bottom:16px}
input,button{padding:9px;border-radius:8px;border:1px solid #596274;background:#273140;color:white}button{cursor:pointer;margin:4px}
.alert{border:1px solid #4b5668;border-left:5px solid #6aa6e8;border-radius:10px;padding:14px;margin:10px 0;background:#151b23}.overdue{border-left-color:#dd6b6b}
.meta{color:#aeb8c7}.hidden{display:none}.timer{font-size:1.4rem}
</style></head><body><main>
<section class="panel" id="setup"><h1>Multi-Robot Supervision Study</h1>
<p>You supervise six autonomous rescue robots. Some alerts are unnecessary; several may appear close together.</p>
<ul><li><b>ABORT</b>: battery below safe-return threshold.</li><li><b>REASSIGN</b>: route blocked or high-confidence victim requires reallocation.</li><li><b>HOLD</b>: thermal, structural, or telemetry threshold crossed.</li><li><b>DISMISS</b>: no intervention threshold crossed.</li></ul>
<input id="pid" placeholder="Participant ID"> <label><input type="checkbox" id="demo"> accelerated demo</label>
<button onclick="startExperiment()">Initialize</button></section>
<section class="panel hidden" id="run"><div style="display:flex;justify-content:space-between"><div><h2 id="title">Ready</h2><div class="meta" id="status"></div></div><div class="timer" id="timer">--:--</div></div>
<button id="startBlock" onclick="startBlock()">Start block</button><div id="alerts"></div></section>
<section class="panel hidden" id="done"><h2>Experiment complete</h2><p>Please notify the researcher.</p></section>
</main><script>
let sid=null,poller=null;
async function api(path,method="GET",body=null){let url=path;if(method==="GET"&&sid)url+="?session_id="+encodeURIComponent(sid);let o={method,headers:{"Content-Type":"application/json"}};if(body)o.body=JSON.stringify({...body,session_id:sid});let r=await fetch(url,o),d=await r.json();if(!r.ok)throw Error(d.error||"Request failed");return d}
async function startExperiment(){try{let d=await api("/api/start","POST",{participant_id:document.getElementById("pid").value,demo:document.getElementById("demo").checked});sid=d.session_id;setup.classList.add("hidden");run.classList.remove("hidden");title.textContent="Ready for block 1";status.textContent="Conditions are blinded."}catch(e){alert(e.message)}}
async function startBlock(){try{let d=await api("/api/start_block","POST",{});if(d.finished)return finish();document.getElementById("startBlock").classList.add("hidden");if(poller)clearInterval(poller);await refresh();poller=setInterval(refresh,500)}catch(e){alert(e.message)}}
function fmt(x){x=Math.max(0,Math.ceil(x));return String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0")}
function esc(x){let d=document.createElement("div");d.textContent=x;return d.innerHTML}
async function refresh(){let s=await api("/api/state");if(s.phase==="finished"){if(poller)clearInterval(poller);return finish()}if(s.phase==="between_blocks"){if(poller)clearInterval(poller);alerts.innerHTML="";timer.textContent="--:--";title.textContent="Block "+s.block+" complete";status.textContent="Take a brief break.";let b=document.getElementById("startBlock");b.textContent="Start block "+(s.block+1);b.classList.remove("hidden");return}if(s.phase!=="running")return;title.textContent="Block "+s.block+" of "+s.total_blocks;timer.textContent=fmt(s.remaining_s);status.textContent=s.responded_count+"/"+s.total_events+" alerts handled";alerts.innerHTML="";if(!s.pending.length){alerts.innerHTML='<p class="meta">No pending supervisory alerts.</p>';return}s.pending.forEach(e=>{let d=document.createElement("div");d.className="alert"+(e.overdue?" overdue":"");let rem=e.overdue?"deadline exceeded":Math.max(0,e.deadline_remaining_s).toFixed(0)+" s to deadline";d.innerHTML='<h3>Robot '+e.robot_id+': '+esc(e.title)+'</h3><p>'+esc(e.description)+'</p><div class="meta">'+rem+'</div><button onclick="respond(\''+e.event_id+'\',\'ABORT\')">ABORT</button><button onclick="respond(\''+e.event_id+'\',\'REASSIGN\')">REASSIGN</button><button onclick="respond(\''+e.event_id+'\',\'HOLD\')">HOLD</button><button onclick="respond(\''+e.event_id+'\',\'DISMISS\')">DISMISS</button>';alerts.appendChild(d)})}
async function respond(id,a){try{await api("/api/respond","POST",{event_id:id,action:a});await refresh()}catch(e){alert(e.message)}}
function finish(){run.classList.add("hidden");done.classList.remove("hidden")}
</script></body></html>"""


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 5000), Handler)
    print("EHC pilot running at http://127.0.0.1:5000")
    print("Logs:", DATA_DIR)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
