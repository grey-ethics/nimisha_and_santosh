/**
 * Loading fallback.
 */
export default function Loading({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="w-full h-[40vh] grid place-items-center">
      <div className="text-gray-600">{label}</div>
    </div>
  );
}
