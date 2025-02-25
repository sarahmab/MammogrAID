"use client";
import { useState, useEffect } from "react";
import ImageUpload from "@/components/ImageUpload";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-lg w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-semibold text-center text-gray-800 mb-6">
          Breast Cancer Detection
        </h1>
        <p className="text-center text-gray-500 mb-8">
          Upload a mammogram image for automated analysis to assist in breast cancer detection.
        </p>
        
        <div className="mb-8">
          <ImageUpload />
        </div>

        <div className="text-center text-gray-500">
          <p>Powered by AI for accurate predictions.</p>
        </div>
      </div>
    </div>
  );
}
