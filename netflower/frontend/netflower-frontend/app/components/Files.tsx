import { useEffect, useState } from "react";

interface FileProps {
  onRefresh: boolean;
}

function FileList({ onRefresh }: FileProps) {
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  useEffect(() => {
    fetchFiles().then()
  }, [onRefresh]);

  // Fetch file list from backend
  const fetchFiles = async () => {
  setLoading(true);
  setError(null);
  try {
    const response = await fetch("http://localhost:5000/files");
    if (!response.ok) {
      alert("Failed to fetch files");
    }

    const data: string[] = await response.json();
    setFiles(data);
  } catch (err) {
    setError(err instanceof Error ? err.message : "Unknown error");
  } finally {
    setLoading(false);
  }
};


  // Delete file request
  const deleteFile = async (fileName: string) => {
    if (!confirm(`Are you sure you want to delete "${fileName}"?`)) return;

    try {
      const response = await fetch(`http://localhost:5000/files/${fileName}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        alert("Failed to delete a file!")
      }

      // Refresh file list after deletion
      fetchFiles().then();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error deleting file");
    }
  };

  return (
    <div className="p-4 bg-gray-100 dark:bg-gray-900 rounded-lg shadow-lg w-full">
      <h1 className="text-4xl font-bold mb-5 text-gray-900 dark:text-white mt-4">
        Converted Files
      </h1>

      {loading && <p className="text-gray-700 dark:text-gray-300">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <table className="w-full border-collapse border border-gray-300 dark:border-gray-700 ">
        <thead>
          <tr className="bg-gray-200 dark:bg-gray-800">
            <th className="p-1.5 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white">
              File Name
            </th>
            <th className="p-1.5 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          {files.map((file, index) => (
            <tr
              key={index}
              className={`cursor-pointer ${
                selectedFile === file
                  ? "bg-blue-300 dark:bg-blue-800"
                  : "hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
              onClick={() => setSelectedFile(file)}
            >
              <td className="p-2 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white">
                {file}
              </td>
              <td className="p-2 border border-gray-300 dark:border-gray-700 text-center">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteFile(file).then();
                  }}
                  className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={() => { fetchFiles().then() }}
        className="w-32 mt-8 bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200 transform hover:scale-105"
      >
        Refresh
      </button>
    </div>
  );
}

export default FileList;
