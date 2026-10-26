"use client";
import { useEffect } from "react";

export interface ToastState {
  id: number;
  message: string;
  undo?: () => void;
}

/** Polite live region; the toast itself is the only floating element besides the decision panel. */
export function Toast({ toast, onDismiss }: { toast: ToastState | null; onDismiss: () => void }) {
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(onDismiss, 8000);
    return () => clearTimeout(t);
  }, [toast, onDismiss]);

  return (
    <div aria-live="polite" role="status" className="pointer-events-none fixed inset-x-0 bottom-4 z-30 flex justify-center px-4">
      {toast && (
        <div className="panel-shadow pointer-events-auto flex items-center gap-4 rounded-md bg-ink px-4 py-2 text-white">
          <span>{toast.message}</span>
          {toast.undo && (
            <button
              type="button"
              onClick={() => {
                toast.undo?.();
                onDismiss();
              }}
              className="rounded-xs px-2 font-medium text-white underline"
            >
              Undo
            </button>
          )}
        </div>
      )}
    </div>
  );
}
