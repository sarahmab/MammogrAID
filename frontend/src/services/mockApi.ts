// services/mockApi.ts
export async function testConnection(): Promise<{ status: string }> {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ status: 'healthy' });
      }, 1000);
    });
  }
  
  export async function uploadImage(file: File): Promise<any> {
    return new Promise((resolve) => {
      setTimeout(() => {
    
        const mockResponses = [
          {
            predicted_class: 'Benign',
            cancer_probability: 0.05,
          },
          {
            predicted_class: 'Stage 1',
            cancer_probability: 0.35,
          },
          {
            predicted_class: 'Stage 2',
            cancer_probability: 0.65,
          },
          {
            predicted_class: 'Stage 3',
            cancer_probability: 0.90,
          },
        ];
  
        const randomIndex = Math.floor(Math.random() * mockResponses.length);
        resolve(mockResponses[randomIndex]);
      }, 1000);
    });
  }
  