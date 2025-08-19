/**
 * Very small modal for inline forms.
 */
export default function Modal({
  open, onClose, title, children
}: { open: boolean; onClose: () => void; title: string; children: React.ReactNode }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 bg-black/30 grid place-items-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg">
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold">{title}</h3>
          <button onClick={onClose} className="px-2 py-1 text-sm border rounded-lg">Close</button>
        </div>
        <div className="p-4">{children}</div>
      </div>
    </div>
  );
}
