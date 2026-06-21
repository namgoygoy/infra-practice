import { useCallback, useEffect, useState, type FormEvent } from 'react'
import {
  createMemo,
  deleteMemo,
  fetchMemo,
  fetchMemos,
  updateMemo,
} from './api/memos'
import type { Memo } from './types/memo'
import { DEPLOY_MESSAGE, DEPLOY_VERSION } from './version'
import './App.css'

function App() {
  const [memos, setMemos] = useState<Memo[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isEditing = selectedId !== null

  const loadMemos = useCallback(async () => {
    setError(null)
    const data = await fetchMemos()
    setMemos(data)
  }, [])

  useEffect(() => {
    loadMemos()
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [loadMemos])

  const resetForm = () => {
    setSelectedId(null)
    setTitle('')
    setContent('')
  }

  const handleSelect = async (id: number) => {
    setError(null)
    setSaving(true)
    try {
      const memo = await fetchMemo(id)
      setSelectedId(memo.id)
      setTitle(memo.title)
      setContent(memo.content)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load memo')
    } finally {
      setSaving(false)
    }
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    if (!title.trim()) {
      setError('제목을 입력해 주세요.')
      return
    }

    setError(null)
    setSaving(true)
    try {
      if (isEditing) {
        await updateMemo(selectedId, { title: title.trim(), content })
      } else {
        await createMemo({ title: title.trim(), content })
      }
      await loadMemos()
      resetForm()
    } catch (err) {
      setError(err instanceof Error ? err.message : '저장에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!window.confirm('이 메모를 삭제할까요?')) return

    setError(null)
    setSaving(true)
    try {
      await deleteMemo(id)
      if (selectedId === id) resetForm()
      await loadMemos()
    } catch (err) {
      setError(err instanceof Error ? err.message : '삭제에 실패했습니다.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-top">
          <div>
            <h1>메모장</h1>
            <p>FastAPI + PostgreSQL 백엔드 연동</p>
          </div>
          <div className="deploy-badge" title="자동 배포 확인용">
            <span className="deploy-badge__version">{DEPLOY_VERSION}</span>
            <span className="deploy-badge__message">{DEPLOY_MESSAGE}</span>
          </div>
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <main className="layout">
        <section className="panel list-panel">
          <div className="panel-header">
            <h2>메모 목록</h2>
            <button type="button" className="btn secondary" onClick={resetForm}>
              새 메모
            </button>
          </div>

          {loading ? (
            <p className="muted">불러오는 중...</p>
          ) : memos.length === 0 ? (
            <p className="muted">아직 메모가 없습니다.</p>
          ) : (
            <ul className="memo-list">
              {memos.map((memo) => (
                <li key={memo.id}>
                  <button
                    type="button"
                    className={`memo-item ${selectedId === memo.id ? 'active' : ''}`}
                    onClick={() => handleSelect(memo.id)}
                  >
                    <strong>{memo.title}</strong>
                    <span>{new Date(memo.updated_at).toLocaleString()}</span>
                  </button>
                  <button
                    type="button"
                    className="btn danger small"
                    onClick={() => handleDelete(memo.id)}
                    disabled={saving}
                  >
                    삭제
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="panel form-panel">
          <h2>{isEditing ? '메모 수정' : '메모 작성'}</h2>
          <form onSubmit={handleSubmit} className="memo-form">
            <label>
              제목
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="제목을 입력하세요"
                maxLength={200}
                disabled={saving}
              />
            </label>
            <label>
              내용
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="내용을 입력하세요"
                rows={12}
                disabled={saving}
              />
            </label>
            <div className="form-actions">
              <button type="submit" className="btn primary" disabled={saving}>
                {saving ? '저장 중...' : isEditing ? '수정' : '작성'}
              </button>
              {isEditing && (
                <button
                  type="button"
                  className="btn secondary"
                  onClick={resetForm}
                  disabled={saving}
                >
                  취소
                </button>
              )}
            </div>
          </form>
        </section>
      </main>
    </div>
  )
}

export default App
