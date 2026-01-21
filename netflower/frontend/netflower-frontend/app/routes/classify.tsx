import { useState } from "react";
import ModelList from "~/components/Models";
import FileList from "~/components/Files";

interface Statistics {
    total: number;
    counts: Record<string, number>;
    percentages: Record<string, number>;
}

interface Prediction {
    flow_id: string;
    src_ip: string;
    dst_ip: string;
    timestamp: string;
    prediction: string;
}

interface ClassifyResponse {
    statistics: Statistics;
    predictions: Prediction[];
}

function Classify() {
    const [selectedModel, setSelectedModel] = useState<string | null>(null);
    const [selectedFile, setSelectedFile] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ClassifyResponse | null>(null);

    const handleClassify = async () => {
        if (!selectedModel || !selectedFile) {
            alert("Please select both a model and a file");
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch("http://localhost:5000/classify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ model: selectedModel, file: selectedFile }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || "Classification failed");
            }

            const data: ClassifyResponse = await response.json();
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error");
        } finally {
            setLoading(false);
        }
    };

    const downloadCsv = () => {
        if (!result) return;

        const headers = ["Flow ID", "Src IP", "Dst IP", "Timestamp", "Prediction"];
        const rows = result.predictions.map((pred) =>
            [pred.flow_id, pred.src_ip, pred.dst_ip, pred.timestamp, pred.prediction].join(",")
        );
        const csvContent = [headers.join(","), ...rows].join("\n");

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `classification_${selectedFile?.replace(".csv", "")}_${selectedModel?.replace(".pkl", "")}.csv`;
        link.click();
        URL.revokeObjectURL(url);
    };

    return (
        <div className="w-full">
            <div className="grid grid-cols-2 gap-2 w-full">
                <ModelList onModelSelect={setSelectedModel} />
                <FileList onRefresh={false} onFileSelect={setSelectedFile} showDelete={false} />
            </div>

            <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-900 rounded-lg">
                <div className="flex items-center gap-4">
                    <button
                        onClick={handleClassify}
                        disabled={!selectedModel || !selectedFile || loading}
                        className={`px-6 py-3 rounded-lg font-bold text-white transition duration-200 ${
                            !selectedModel || !selectedFile || loading
                                ? "bg-gray-400 cursor-not-allowed"
                                : "bg-green-500 hover:bg-green-600 hover:scale-105"
                        }`}
                    >
                        {loading ? "Classifying..." : "Classify"}
                    </button>
                    <span className="text-gray-700 dark:text-gray-300">
                        {selectedModel && selectedFile
                            ? `Model: ${selectedModel} | File: ${selectedFile}`
                            : "Select a model and a file to classify"}
                    </span>
                </div>

                {error && <p className="mt-4 text-red-500">{error}</p>}

                {result && (
                    <div className="mt-6">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                            Results
                        </h2>

                        {/* Statistics */}
                        <div className="mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg">
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                Statistics (Total: {result.statistics.total} flows)
                            </h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {Object.entries(result.statistics.counts).map(([label, count]) => (
                                    <div key={label} className="p-3 bg-gray-100 dark:bg-gray-700 rounded">
                                        <p className="font-bold text-gray-900 dark:text-white">{label}</p>
                                        <p className="text-gray-700 dark:text-gray-300">
                                            {count} ({result.statistics.percentages[label]}%)
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Download button */}
                        <button
                            onClick={downloadCsv}
                            className="px-6 py-3 rounded-lg font-bold text-white bg-blue-500 hover:bg-blue-600 transition duration-200 hover:scale-105"
                        >
                            Download CSV
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Classify;
