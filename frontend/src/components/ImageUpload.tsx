"use client";

import { useState } from "react";
import { uploadImage } from "@/services/api";

export default function ImageUpload() {
  const [prediction, setPrediction] = useState<{
    predicted_class: string;
    cancer_probability: number;
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await uploadImage(file);
      setPrediction(result);
    } catch (err) {
      setError("Failed to process image");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="border p-2 rounded"
      />

      {loading && <p>Processing image...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {prediction && (
        <div className="text-center">
          <p>Prediction: {prediction.predicted_class}</p>
          <p>
            Probability: {(prediction.cancer_probability * 100).toFixed(2)}%
          </p>
        </div>
      )}
    </div>
  );
}
