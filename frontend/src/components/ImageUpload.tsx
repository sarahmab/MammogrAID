
"use client";

import { useState, useEffect } from "react";
import { uploadImage, testConnection } from "@/services/api"; 
// import { uploadImage, testConnection } from "@/services/mockApi";  // importing mock api functions for now

export default function ImageUpload() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    testConnection()
      .then((result) => console.log("Backend connection test:", result))
      .catch((err) => console.error("Backend connection failed:", err));
  }, []);

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const result = await uploadImage(file);  
      setResult(result);
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="border p-2 rounded"
        aria-label="Upload image"
        disabled={loading}
      />

      {loading && <p>Processing image...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {result && (
        <div className="text-center">
          <h3>Results:</h3>
          <p>Prediction: {result.predicted_class}</p>
          <p>Probability: {(result.cancer_probability * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
