// Hand-written mirror of docs/plan/01 section 6. Swap for generated schema.d.ts later.
export type AccountType = "checking" | "credit_card";
export type Direction = "inflow" | "outflow";
export type Status = "auto" | "needs_review" | "user_confirmed" | "duplicate";
export type CategoryKind = "income" | "expense" | "non_pnl";

export interface StatementCounts {
  auto: number;
  needs_review: number;
  user_confirmed: number;
  duplicate: number;
}
export interface ParseWarning {
  code: string;
  message: string;
  row_index: number | null;
}
export interface StatementOut {
  id: string;
  filename: string;
  source_format: "csv" | "ofx";
  account_type: AccountType;
  uploaded_at: string;
  period_start: string | null;
  period_end: string | null;
  row_count: number;
  counts: StatementCounts;
  warnings: ParseWarning[];
}
export interface TransactionOut {
  id: string;
  row_index: number;
  posted_date: string;
  amount_cents: number;
  direction: Direction;
  description: string;
  memo: string | null;
  merchant_key: string;
  category: string | null;
  brain_category: string | null;
  status: Status;
  confidence: number;
  reasons: string[];
  flags: string[];
  is_refund: boolean;
  duplicate_of_id: string | null;
  similar_count: number;
}
export interface TransactionPage {
  items: TransactionOut[];
  total: number;
}
export interface CorrectionIn {
  category: string;
  remember?: boolean;
  apply_to_similar?: boolean;
}
export interface CorrectionOut {
  updated: TransactionOut[];
  rule_created: boolean;
}
export interface CategoryOut {
  code: string;
  label: string;
  kind: CategoryKind;
  schedule_e_line: string | null;
  allowed_directions: Direction[];
}
export interface ScheduleELine {
  line: string;
  label: string;
  category: string;
  total_cents: number;
}
export interface SummaryOut {
  income: Record<string, number>;
  expenses: Record<string, number>;
  schedule_e: ScheduleELine[];
  total_income_cents: number;
  total_expense_cents: number;
  net_cents: number;
  excluded: Record<string, number>;
  unresolved: { count: number; total_abs_cents: number };
  duplicates: { count: number };
}
export interface ProblemJson {
  type?: string;
  title?: string;
  status: number;
  detail?: string;
  instance?: string;
  errors?: { row_index?: number | null; message: string }[];
}
