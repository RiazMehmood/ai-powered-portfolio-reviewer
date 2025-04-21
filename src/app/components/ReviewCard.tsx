export function ReviewCard({ content }: { content: string }) {
  return (
    <div className="mt-6 p-4 bg-white rounded-xl shadow-md border">
      <h2 className="text-xl font-semibold mb-2">AI Feedback</h2>
      <p className="whitespace-pre-line text-gray-800">{content}</p>
    </div>
  );
}
