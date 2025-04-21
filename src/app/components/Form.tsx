"use client";

import { useState } from "react";

export default function PortfolioForm() {
  const [url, setUrl] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/review", {
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
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Reviewing..." : "Submit"}
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
