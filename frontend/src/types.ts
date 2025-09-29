export interface Evaluation {
  id: number;
  applicant_id: number;
  model_name: string;
  scores?: Record<string, unknown> | null;
  summary?: string | null;
  recommendations?: Record<string, unknown>[] | null;
  created_at?: string | null;
}

export interface Suggestion {
  id: number;
  evaluation_id: number;
  title: string;
  description: string;
  impact?: string | null;
  effort?: string | null;
  deadline?: string | null;
  acknowledged_at?: string | null;
  is_archived?: boolean;
}

export interface Milestone {
  id: number;
  applicant_id: number;
  title: string;
  description?: string | null;
  due_date?: string | null;
  completed_at?: string | null;
}

export interface Essay {
  id: number;
  applicant_id: number;
  prompt: string;
  content: string;
  version?: number | null;
  created_at?: string | null;
}
