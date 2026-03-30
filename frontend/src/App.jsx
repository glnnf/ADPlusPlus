import { useState } from 'react'
import './App.css'

function App() {
  const [tasks, setTasks] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [input, setInput] = useState('')

  const handleAdd = () => {
    const trimmed = input.trim()
    if (!trimmed) return
    setTasks(prev => [...prev, { id: Date.now(), text: trimmed, done: false }])
    setInput('')
    setModalOpen(false)
  }

  const handleToggle = (id) => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  const handleDelete = (id) => {
    setTasks(prev => prev.filter(t => t.id !== id))
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleAdd()
    if (e.key === 'Escape') setModalOpen(false)
  }

  return (
    <>
      <main id="main">
        <header id="top-bar">
          <h1>Reminders</h1>
          <span className="task-count">{tasks.filter(t => !t.done).length} remaining</span>
        </header>

        <ul id="task-list">
          {tasks.length === 0 && (
            <li className="empty-state">No tasks yet. Hit <strong>+</strong> to add one.</li>
          )}
          {tasks.map(task => (
            <li key={task.id} className={`task-item${task.done ? ' done' : ''}`}>
              <button
                className="task-check"
                onClick={() => handleToggle(task.id)}
                aria-label={task.done ? 'Mark incomplete' : 'Mark complete'}
              >
                {task.done && (
                  <svg viewBox="0 0 12 12" fill="none" width="12" height="12">
                    <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
              <span className="task-text">{task.text}</span>
              <button
                className="task-delete"
                onClick={() => handleDelete(task.id)}
                aria-label="Delete task"
              >
                <svg viewBox="0 0 12 12" fill="none" width="12" height="12">
                  <path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
                </svg>
              </button>
            </li>
          ))}
        </ul>

        <button id="add-btn" onClick={() => setModalOpen(true)} aria-label="Add task">
          <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
            <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round"/>
          </svg>
        </button>
      </main>

      {modalOpen && (
        <div id="modal-overlay" onClick={() => setModalOpen(false)}>
          <div id="modal" onClick={e => e.stopPropagation()}>
            <h2>New Task</h2>
            <input
              id="task-input"
              type="text"
              placeholder="What do you need to do?"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              autoFocus
            />
            <div id="modal-actions">
              <button className="btn-cancel" onClick={() => setModalOpen(false)}>Cancel</button>
              <button className="btn-confirm" onClick={handleAdd} disabled={!input.trim()}>Add Task</button>
            </div>
          </div>
        </div>
      )}

      <footer id="footer">
        <span>© {new Date().getFullYear()} Reminders. All rights reserved.</span>
      </footer>
    </>
  )
}

export default App
