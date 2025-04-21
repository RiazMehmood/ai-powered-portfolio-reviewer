"use client";

import { useState } from "react";

export default function PortfolioForm() {
  const [url, setUrl] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [provider, setProvider] = useState<"openai" | "gemini">("openai");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const endpoint =
      provider === "openai"
        ? "http://localhost:8000/review"
        : "http://localhost:8000/review/gemini";

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await res.json();
      if (data.review) {
        setReview(data.review);
      } else {
        setReview("Error: " + data.error);
      }
    } catch (err) {
      setReview("Request failed. Is the server running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Enter portfolio or GitHub URL"
          className="border p-2 rounded"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setProvider("openai")}
            className={`px-4 py-2 rounded ${
              provider === "openai"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-black"
            }`}
          >
            Use OpenAI
          </button>
          <button
            type="button"
            onClick={() => setProvider("gemini")}
            className={`px-4 py-2 rounded ${
              provider === "gemini"
                ? "bg-purple-600 text-white"
                : "bg-gray-200 text-black"
            }`}
          >
            Use Gemini
          </button>
        </div>

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Reviewing..." : `Submit to ${provider.toUpperCase()}`}
        </button>
      </form>

      {review && (
        <div className="mt-6 bg-gray-100 p-4 rounded whitespace-pre-wrap">
          {review}
        </div>
      )}
    </div>
  );
}
