import React, { useState } from 'react';
import Files from '~/components/Files'; // Import the Files component

function Convert() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState<boolean>(false);  // State to trigger refresh

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };


  // Handle file conversion
  const handleConvert = async () => {
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/convert', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        alert(`Success: ${result.message}`);
      } else {
        alert(`Error: ${result.error || 'File upload failed'}`);
      }

      setRefreshTrigger(!refreshTrigger);  // Toggle the refresh trigger state

    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload file.');
    }

    setSelectedFile(null);
    setRefreshTrigger(!refreshTrigger);  // Toggle the refresh trigger state
  };

  return (
    <div className="grid grid-cols-2 gap-2 w-full">
      {/* Upload Form */}
      <div className="bg-white dark:bg-gray-900 p-8 rounded-lg shadow-lg w-full">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900 dark:text-white">
          File Converter
        </h1>
        <div className="mb-6">
          <input
            id="file-input"
            type="file"
            onChange={handleFileChange}
            accept=".pcap"
            className="hidden"
          />
          <div
            onClick={() => document.getElementById('file-input')?.click()}
            className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-lg cursor-pointer flex items-center justify-between bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            <span>{selectedFile ? selectedFile.name : 'Browse...'}</span>
            <span className="text-blue-500">Choose File</span>
          </div>
        </div>
        <div className="mb-6">
          <button
            onClick={handleConvert}
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200 transform hover:scale-105"
          >
            Convert
          </button>
        </div>
      </div>

      {/* Files List */}
      <Files onRefresh={refreshTrigger} />
    </div>
  );
}

export default Convert;
