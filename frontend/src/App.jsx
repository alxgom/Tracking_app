import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const API = "http://localhost:8000";

const COLORS = ['#f26b38','#10b981','#6366f1','#f59e0b','#ec4899','#14b8a6','#8b5cf6','#ef4444'];
function randomColor() { return COLORS[Math.floor(Math.random() * COLORS.length)]; }
const todayStr = () => new Date().toISOString().slice(0, 10);

// ─── Generic confirm modal ───────────────────────────────────────────
function ConfirmModal({ title='Are you sure?', message, confirmLabel='Confirm', danger=false, onConfirm, onCancel }) {
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2 style={{ marginBottom: 12 }}>{title}</h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: 28, lineHeight: 1.5 }}>{message}</p>
        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
          <button className="btn btn-secondary" onClick={onCancel}>Cancel</button>
          <button
            className="btn btn-primary"
            style={danger ? { background: 'var(--danger)', boxShadow: 'none' } : {}}
            onClick={onConfirm}
          >{confirmLabel}</button>
        </div>
      </div>
    </div>
  );
}

// ─── Sidebar task row ────────────────────────────────────────────────
function TaskRow({ task, isActive, totalMinutes, onSelect, onUpdated, onDeleted }) {
  const [editing, setEditing]     = useState(false);
  const [editName, setEditName]   = useState(task.name);
  const [editColor, setEditColor] = useState(task.color);
  const [confirming, setConfirming] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => { if (editing) inputRef.current?.focus(); }, [editing]);

  const startEdit = (e) => { e.stopPropagation(); setEditName(task.name); setEditColor(task.color); setEditing(true); };

  const saveEdit = async () => {
    const trimmed = editName.trim();
    if (!trimmed) { setEditing(false); return; }
    try {
      const res = await fetch(`${API}/tasks/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: trimmed, color: editColor })
      });
      onUpdated(await res.json());
    } catch {/* swallow */}
    setEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') saveEdit();
    if (e.key === 'Escape') setEditing(false);
  };

  // Total time badge
  const totalLabel = totalMinutes >= 60
    ? `${Math.floor(totalMinutes / 60)}h ${totalMinutes % 60}m`
    : totalMinutes > 0 ? `${totalMinutes}m` : null;

  return (
    <>
      {confirming && (
        <ConfirmModal
          danger
          confirmLabel="Delete"
          message={`Delete "${task.name}" and all its time logs? This cannot be undone.`}
          onConfirm={async () => {
            await fetch(`${API}/tasks/${task.id}`, { method: 'DELETE' });
            onDeleted(task.id);
            setConfirming(false);
          }}
          onCancel={() => setConfirming(false)}
        />
      )}

      <div className={`task-row ${isActive ? 'active' : ''}`} onClick={() => !editing && onSelect(task)}>
        {editing ? (
          <>
            <label
              className="color-swatch"
              style={{ backgroundColor: editColor, position: 'relative' }}
              onClick={e => e.stopPropagation()}
            >
              <input
                type="color"
                value={editColor}
                onChange={e => setEditColor(e.target.value)}
                onClick={e => e.stopPropagation()}
              />
            </label>
            <input ref={inputRef} className="task-edit-input" value={editName}
              onChange={e => setEditName(e.target.value)}
              onKeyDown={handleKeyDown} onBlur={saveEdit}
              onClick={e => e.stopPropagation()} />
            <button className="btn-ghost" onClick={saveEdit}>✓</button>
          </>
        ) : (
          <>
            <span className="task-dot" style={{ backgroundColor: task.color }} />
            <span className="task-name">{task.name}</span>
            {totalLabel && !isActive && (
              <span style={{ fontSize: 11, color: 'var(--text-muted)', flexShrink: 0, marginRight: 4 }}>{totalLabel}</span>
            )}
            <span className="task-actions">
              <button className="btn-ghost" onClick={startEdit} title="Rename">✏️</button>
              <button className="btn-ghost danger" onClick={e => { e.stopPropagation(); setConfirming(true); }} title="Delete">🗑️</button>
            </span>
          </>
        )}
      </div>
    </>
  );
}

// ─── Main App ────────────────────────────────────────────────────────
export default function App() {
  const [tasks,        setTasks]        = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [newTaskName,  setNewTaskName]  = useState('');
  const [newTaskColor, setNewTaskColor] = useState(randomColor());

  // Timer
  const [timerRunning, setTimerRunning] = useState(false);
  const [elapsedMs,    setElapsedMs]    = useState(0);
  const [timerNotes,   setTimerNotes]   = useState('');
  const [timerMode,    setTimerMode]    = useState('stopwatch'); // 'stopwatch' or 'timer'
  const [timerTarget,  setTimerTarget]  = useState(25); // Target minutes for timer mode

  // History
  const [history,       setHistory]       = useState([]);
  const [manualMinutes, setManualMinutes] = useState('');
  const [manualDate,    setManualDate]    = useState(todayStr());
  const [manualNotes,   setManualNotes]   = useState('');

  // Navigation
  const [showAnalytics, setShowAnalytics]  = useState(false);
  const [analyticsView, setAnalyticsView]  = useState('by-task'); // 'by-task' or 'by-date'

  // Timer-running guard modal
  const [pendingAction, setPendingAction] = useState(null); // { label, action }

  // ── Fetch ─────────────────────────────────────
  const fetchTasks   = async () => { const r = await fetch(`${API}/tasks`);         setTasks(await r.json()); };
  const fetchHistory = async () => { const r = await fetch(`${API}/history?limit=100`); setHistory(await r.json()); };
  useEffect(() => { fetchTasks(); fetchHistory(); }, []);

  // ── Timer interval ────────────────────────────
  useEffect(() => {
    if (!timerRunning) return;
    const id = setInterval(() => {
      setElapsedMs(p => {
        if (timerMode === 'timer') {
          const next = p - 1000;
          if (next <= 0) {
            setTimerRunning(false);
            // Play a subtle beep or alert if desired
            if (Notification.permission === "granted") {
              new Notification("Timer Finished!", { body: `Session for ${selectedTask?.name} is complete.` });
            } else {
              alert("Timer Finished!");
            }
            return 0;
          }
          return next;
        }
        return p + 1000;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [timerRunning, timerMode, selectedTask]);

  // Request notification permission
  useEffect(() => {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, []);

  const formatTime = ms => {
    const s = Math.floor(ms / 1000);
    return [Math.floor(s / 3600), Math.floor((s % 3600) / 60), s % 60]
      .map(n => String(n).padStart(2, '0')).join(':');
  };

  // ── Navigation guard ──────────────────────────
  // If timer is running and user tries to leave the current context, ask first.
  const guardedAction = (label, action) => {
    if (timerRunning) {
      setPendingAction({ label, action });
    } else {
      action();
    }
  };

  // ── Keyboard shortcut — Space to toggle timer ──
  useEffect(() => {
    const handler = (e) => {
      if (e.code !== 'Space') return;
      // Ignore when focus is inside an input/textarea
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
      e.preventDefault();
      if (selectedTask) setTimerRunning(r => !r);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTask]);

  // ── Task selection ────────────────────────────
  const handleSelectTask = (task) => {
    if (selectedTask?.id === task.id) return;
    guardedAction(`switch to "${task.name}"`, () => {
      setTimerRunning(false);
      setElapsedMs(0);
      setSelectedTask(task);
      setShowAnalytics(false);
    });
  };

  const handleShowAnalytics = () => {
    guardedAction('open Analytics', () => {
      setTimerRunning(false);
      setElapsedMs(0);
      setSelectedTask(null);
      setShowAnalytics(true);
    });
  };

  // ── Add task ──────────────────────────────────
  const handleAddTask = async (e) => {
    e.preventDefault();
    const name = newTaskName.trim();
    if (!name) return;
    if (tasks.some(t => t.name.toLowerCase() === name.toLowerCase())) {
      alert(`"${name}" already exists.`); return;
    }
    await fetch(`${API}/tasks`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, color: newTaskColor })
    });
    setNewTaskName('');
    setNewTaskColor(randomColor());
    fetchTasks();
  };

  // ── Task CRUD callbacks ───────────────────────
  const handleTaskUpdated = (updated) => {
    setTasks(prev => prev.map(t => t.id === updated.id ? updated : t));
    if (selectedTask?.id === updated.id) setSelectedTask(updated);
  };

  const handleTaskDeleted = (id) => {
    setTasks(prev => prev.filter(t => t.id !== id));
    if (selectedTask?.id === id) { setSelectedTask(null); setTimerRunning(false); setElapsedMs(0); }
    fetchHistory();
  };

  // ── Save timer log ────────────────────────────
  const saveTimerLog = async () => {
    const loggedMs = timerMode === 'stopwatch' ? elapsedMs : (timerTarget * 60000 - elapsedMs);
    const minutes = Math.floor(loggedMs / 60000);

    if (minutes < 1 || !selectedTask) { alert('Log at least 1 minute first.'); return; }
    await fetch(`${API}/history`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: selectedTask.id, duration_minutes: minutes, notes: timerNotes || null })
    });
    setTimerRunning(false); 
    setElapsedMs(timerMode === 'timer' ? timerTarget * 60000 : 0); 
    setTimerNotes(''); 
    fetchHistory();
  };

  // ── Manual log ────────────────────────────────
  const handleManualSave = async (e) => {
    e.preventDefault();
    const mins = parseInt(manualMinutes);
    if (!mins || mins < 1 || !selectedTask) return;
    // Combine selected date with current time
    const dateObj = new Date(manualDate + 'T12:00:00');
    await fetch(`${API}/history`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: selectedTask.id, duration_minutes: mins, date: dateObj.toISOString() })
    });
    setManualMinutes(''); fetchHistory();
  };

  // ── Delete log ────────────────────────────────
  const deleteLog = async (id) => {
    await fetch(`${API}/history/${id}`, { method: 'DELETE' });
    fetchHistory();
  };

  // ── Derived data ──────────────────────────────
  // Per-task totals for sidebar badges
  const taskTotals = history.reduce((acc, log) => {
    acc[log.task_id] = (acc[log.task_id] || 0) + log.duration_minutes;
    return acc;
  }, {});

  // History filtered to selected task when viewing dashboard
  const visibleHistory = selectedTask
    ? history.filter(l => l.task_id === selectedTask.id)
    : history;

  // Analytics by task name
  const analyticsData = Object.values(
    history.reduce((acc, log) => {
      const key = log.task.id;
      if (!acc[key]) acc[key] = { name: log.task.name, color: log.task.color, total: 0 };
      acc[key].total += log.duration_minutes;
      return acc;
    }, {})
  );
  const maxAnalytics = Math.max(...analyticsData.map(d => d.total), 1);

  const tc = selectedTask?.color || 'var(--primary)';

  return (
    <div className="app-container" style={{ '--task-color': tc }}>
      {/* ── Timer-guard modal ───────────────────── */}
      {pendingAction && (
        <ConfirmModal
          title="Active timer!"
          message={`You have a running timer. Are you sure you want to ${pendingAction.label}? The current session will be discarded.`}
          confirmLabel="Yes, discard timer"
          danger
          onConfirm={() => { pendingAction.action(); setPendingAction(null); }}
          onCancel={() => setPendingAction(null)}
        />
      )}

      {/* ── Sidebar ─────────────────────────────── */}
      <aside className="sidebar">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h2 style={{ color: 'var(--primary)', fontSize: 20 }}>⏱ Tracking App</h2>
          {timerRunning && (
            <span style={{ fontSize: 12, fontWeight: 700, color: tc,
              background: `${tc}22`, padding: '3px 8px', borderRadius: 20,
              animation: 'pulse 1.5s ease-in-out infinite' }}>
              🔴 {formatTime(elapsedMs)}
            </span>
          )}
        </div>

        {/* Add task form */}
        <form onSubmit={handleAddTask} style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <label className="color-swatch" style={{ backgroundColor: newTaskColor, position: 'relative', flexShrink: 0 }}>
            <input type="color" value={newTaskColor} onChange={e => setNewTaskColor(e.target.value)} />
          </label>
          <input className="input" style={{ flex: 1, minWidth: 0 }}
            placeholder="New task..." value={newTaskName}
            onChange={e => setNewTaskName(e.target.value)} />
          <button type="submit" className="btn btn-primary" style={{ padding: '10px 14px' }}>+</button>
        </form>

        {/* Task list */}
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 4 }}>
          <h3 style={{ marginBottom: 8 }}>Tasks</h3>
          {tasks.map(t => (
            <TaskRow key={t.id} task={t} isActive={selectedTask?.id === t.id}
              totalMinutes={taskTotals[t.id] || 0}
              onSelect={handleSelectTask}
              onUpdated={handleTaskUpdated}
              onDeleted={handleTaskDeleted} />
          ))}
          {tasks.length === 0 && (
            <p style={{ color: 'var(--text-muted)', fontSize: 13, padding: '12px 0' }}>No tasks yet — add one above!</p>
          )}
        </div>

        <button className={showAnalytics ? 'btn btn-primary' : 'btn btn-secondary'}
          style={{ width: '100%' }} onClick={handleShowAnalytics}>
          📊 Analytics
        </button>
      </aside>

      {/* ── Main Content ────────────────────────── */}
      <main className="main-content">
        {showAnalytics ? (
          /* Analytics view */
          <div className="animate-slide" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 }}>
              <div>
                <h1>Activity Analytics 📊</h1>
                <div style={{ display: 'flex', gap: 12, marginTop: 12 }}>
                  <button className={`btn ${analyticsView === 'by-task' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setAnalyticsView('by-task')}>By Task</button>
                  <button className={`btn ${analyticsView === 'by-date' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setAnalyticsView('by-date')}>By Date</button>
                </div>
              </div>
              <button className="btn btn-secondary" onClick={() => setShowAnalytics(false)}>← Dashboard</button>
            </header>

            <div className="glass-panel" style={{ flex: 1, padding: '32px', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              {history.length === 0 ? (
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
                  No data yet — start logging some time!
                </div>
              ) : (
                <div className="chart-container">
                  {(analyticsView === 'by-task' 
                    ? analyticsData.sort((a,b) => b.total - a.total)
                    : Object.values(history.reduce((acc, log) => {
                        const date = new Date(log.date).toLocaleDateString();
                        if (!acc[date]) acc[date] = { name: date, total: 0, color: 'var(--primary)' };
                        acc[date].total += log.duration_minutes;
                        return acc;
                      }, {})).sort((a,b) => new Date(b.name) - new Date(a.name))
                  ).map(d => (
                    <div key={d.name} className="chart-row">
                      <div className="chart-label" title={d.name}>{d.name}</div>
                      <div className="chart-bar-bg">
                        <div className="chart-bar-fill" style={{ 
                          width: `${(d.total / (analyticsView === 'by-task' ? maxAnalytics : Math.max(...history.map(l => l.duration_minutes), 1))) * 100}%`,
                          background: d.color || 'var(--primary)'
                        }} />
                      </div>
                      <div className="chart-value">
                        {d.total >= 60 ? `${Math.floor(d.total/60)}h ${d.total%60}m` : `${d.total}m`}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          /* Dashboard view */
          <>
            <header style={{ marginBottom: 36 }} className="animate-slide">
              {selectedTask ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span className="task-dot" style={{ backgroundColor: selectedTask.color, width: 18, height: 18 }} />
                  <h1>{selectedTask.name}</h1>
                </div>
              ) : (
                <h1 style={{ color: 'var(--text-muted)', fontWeight: 600 }}>Select a task to begin 🚀</h1>
              )}
            </header>

            <div style={{ display: 'flex', gap: 24, flex: 1 }}>
              {/* Stopwatch panel */}
              <div className={`glass-panel animate-slide ${timerRunning ? 'timer-active' : ''}`}
                style={{ flex: 1, padding: 40, display: 'flex', flexDirection: 'column',
                  '--glow-color': tc }}>
                
                <div className="timer-controls">
                  <div className="mode-toggle">
                    <button className={`mode-btn ${timerMode === 'stopwatch' ? 'active' : ''}`}
                      onClick={() => { setTimerMode('stopwatch'); setElapsedMs(0); setTimerRunning(false); }}>
                      Stopwatch
                    </button>
                    <button className={`mode-btn ${timerMode === 'timer' ? 'active' : ''}`}
                      onClick={() => { setTimerMode('timer'); setElapsedMs(timerTarget * 60000); setTimerRunning(false); }}>
                      Timer
                    </button>
                  </div>

                  {timerMode === 'timer' && (
                    <div className="timer-picker">
                      <button className={`chip ${timerTarget === 25 ? 'active' : ''}`} 
                        onClick={() => { setTimerTarget(25); setElapsedMs(25 * 60000); }}>25m</button>
                      <button className={`chip ${timerTarget === 50 ? 'active' : ''}`} 
                        onClick={() => { setTimerTarget(50); setElapsedMs(50 * 60000); }}>50m</button>
                      <input className="input" type="number" placeholder="Mins" 
                        value={timerTarget} onChange={e => {
                          const val = parseInt(e.target.value) || 0;
                          setTimerTarget(val); 
                          setElapsedMs(val * 60000);
                        }} style={{ width: 70, padding: '4px 8px' }} />
                    </div>
                  )}
                </div>

                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 28, marginTop: 20 }}>
                  <span style={{
                    fontSize: 84, fontWeight: 700, letterSpacing: '-3px',
                    fontVariantNumeric: 'tabular-nums',
                    color: timerRunning ? tc : 'var(--text-muted)',
                    transition: 'color 0.4s ease'
                  }}>
                    {formatTime(elapsedMs)}
                  </span>
                  <div style={{ display: 'flex', gap: 12 }}>
                    <button
                      className={timerRunning ? 'btn btn-secondary' : 'btn btn-primary'}
                      style={!timerRunning && selectedTask ? { background: tc, boxShadow: `0 4px 14px ${tc}55` } : {}}
                      onClick={() => setTimerRunning(r => !r)} disabled={!selectedTask}>
                      {timerRunning ? '⏸ Pause' : '▶ Start'}
                    </button>
                    <button className="btn btn-secondary" onClick={saveTimerLog}
                      disabled={!selectedTask || (timerMode === 'stopwatch' ? elapsedMs < 60000 : (timerTarget * 60000 - elapsedMs) < 60000)}>
                      💾 Save
                    </button>
                    <button className="btn btn-secondary"
                      onClick={() => { setTimerRunning(false); setElapsedMs(timerMode === 'timer' ? timerTarget * 60000 : 0); }}
                      disabled={timerMode === 'stopwatch' ? !elapsedMs : elapsedMs === timerTarget * 60000}>
                      ↺ Reset
                    </button>
                  </div>
                  {/* Session notes for timer */}
                  <textarea
                    className="input"
                    placeholder="Session notes (optional)..."
                    value={timerNotes}
                    onChange={e => setTimerNotes(e.target.value)}
                    disabled={!selectedTask}
                    rows={2}
                    style={{ width: '100%', resize: 'none', fontSize: 13, marginTop: 4 }}
                  />
                </div>
              </div>

              {/* History panel */}
              <div className="glass-panel animate-slide"
                style={{ flex: 1, padding: 32, display: 'flex', flexDirection: 'column',
                  borderLeft: selectedTask ? `3px solid ${tc}` : undefined }}>
                <h2 style={{ marginBottom: 20, color: selectedTask ? tc : 'var(--text-main)' }}>
                  {selectedTask ? `${selectedTask.name} — Logs` : 'Manual Entry & History'}
                </h2>

                <form onSubmit={handleManualSave} style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 24 }}>
                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                    <input className="input" type="date" value={manualDate}
                      onChange={e => setManualDate(e.target.value)}
                      disabled={!selectedTask} style={{ flex: '1 1 120px' }} max={todayStr()} />
                    <input className="input" type="number" placeholder="Minutes"
                      value={manualMinutes} onChange={e => setManualMinutes(e.target.value)}
                      disabled={!selectedTask} style={{ width: 100 }} min="1" />
                    <button className="btn btn-primary" type="submit" disabled={!selectedTask}
                      style={selectedTask ? { background: tc, boxShadow: `0 4px 14px ${tc}44` } : {}}>
                      Add Log
                    </button>
                  </div>
                  <textarea
                    className="input"
                    placeholder="Notes (optional)..."
                    value={manualNotes}
                    onChange={e => setManualNotes(e.target.value)}
                    disabled={!selectedTask}
                    rows={2}
                    style={{ resize: 'none', fontSize: 13 }}
                  />
                </form>

                <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {visibleHistory.length === 0 ? (
                    <div style={{ color: 'var(--text-muted)', textAlign: 'center', marginTop: 40, fontSize: 14 }}>
                      {selectedTask ? 'No logs for this task yet.' : 'No logs yet.'}
                    </div>
                  ) : visibleHistory.map(log => (
                    <div key={log.id} className="history-row animate-fade">
                      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 8, flex: 1 }}>
                        <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: log.task.color, flexShrink: 0, marginTop: 4 }} />
                        <div style={{ flex: 1 }}>
                          {!selectedTask && <strong style={{ display: 'block', fontSize: 13 }}>{log.task.name}</strong>}
                          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                            {new Date(log.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                          </span>
                          {log.notes && (
                            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 3, fontStyle: 'italic', lineHeight: 1.4 }}>
                              {log.notes}
                            </p>
                          )}
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexShrink: 0 }}>
                        <span style={{ fontWeight: 700, color: log.task.color, fontSize: 14 }}>{log.duration_minutes} min</span>
                        <button className="btn-ghost danger" onClick={() => deleteLog(log.id)} title="Delete">✕</button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
