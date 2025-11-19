import { useEffect, useState } from "react";


function ModelList() {
  const [models, setModels] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  // Fetch file list from backend
  const fetchModels = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch("http://localhost:5000/models");
        if (!response.ok) {
          alert("Failed to fetch any models from the server")
        }

        const data: string[] = await response.json();
        setModels(data);
      } catch (err) {
          setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
          setLoading(false);
      }
  };


  useEffect(() => {
    fetchModels().then();
  }, []);

  return (
    <div className="p-4 bg-gray-100 dark:bg-gray-900 rounded-lg shadow-lg w-full">
      <h2 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">
        Choose from available Models
      </h2>

      {loading && <p className="text-gray-700 dark:text-gray-300">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <table className="w-full border-collapse border border-gray-300 dark:border-gray-700">
        <thead>
          <tr className="bg-gray-200 dark:bg-gray-800 justify-left">
            <th className="p-2 text-left border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white">
              Model Name
            </th>
          </tr>
        </thead>
        <tbody>
          {models.map((model, index) => (
            <tr
              key={index}
              className={`cursor-pointer ${
                selectedModel === model
                  ? "bg-blue-300 dark:bg-blue-800"
                  : "hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
              onClick={() => setSelectedModel(model)}
            >
              <td className="p-2 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white">
                {model}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={() => { fetchModels().then() }}
        className="w-32 mt-8 bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200 transform hover:scale-105"
      >
        Refresh
      </button>
    </div>
  );
}

export default ModelList;
