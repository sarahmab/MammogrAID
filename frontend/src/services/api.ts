const API_URL = "http://localhost:5000/";

interface PredictionResponse {
  predicted_class: string;
  cancer_probability: number;
}

export async function uploadImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData();

  formData.append("image", file);

  try {
    const response = await fetch(`${API_URL}/api/predict`, {
      method: "POST",
      body: formData,
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.error || "Failed to process image");
    }

    const data = await response.json();
    return {
      predicted_class: data.predicted_class,
      cancer_probability: data.cancer_probability,
    };
  } catch (error) {
    console.error("Error uploading image:", error);
    throw error;
  }
}

export async function testConnection(): Promise<{ status: string }> {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
      },
    });
    if (!response.ok) {
      console.log(response);
      throw new Error("Failed to connect to backend");
    }
    return await response.json();
  } catch (error) {
    console.error("Connection test failed:", error);
    throw error;
  }
}
