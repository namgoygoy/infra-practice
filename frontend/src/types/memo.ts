export interface Memo {
  id: number
  title: string
  content: string
  created_at: string
  updated_at: string
}

export interface MemoCreate {
  title: string
  content: string
}

export interface MemoUpdate {
  title?: string
  content?: string
}
