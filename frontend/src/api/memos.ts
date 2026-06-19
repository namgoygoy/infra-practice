import type { Memo, MemoCreate, MemoUpdate } from '../types/memo'

const API_BASE = '/api/memos'

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed: ${response.status}`)
  }
  if (response.status === 204) {
    return undefined as T
  }
  return response.json() as Promise<T>
}

export async function fetchMemos(): Promise<Memo[]> {
  const response = await fetch(API_BASE)
  return handleResponse<Memo[]>(response)
}

export async function fetchMemo(id: number): Promise<Memo> {
  const response = await fetch(`${API_BASE}/${id}`)
  return handleResponse<Memo>(response)
}

export async function createMemo(data: MemoCreate): Promise<Memo> {
  const response = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse<Memo>(response)
}

export async function updateMemo(id: number, data: MemoUpdate): Promise<Memo> {
  const response = await fetch(`${API_BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse<Memo>(response)
}

export async function deleteMemo(id: number): Promise<void> {
  const response = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' })
  return handleResponse<void>(response)
}
