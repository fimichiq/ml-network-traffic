import os
import pickle
import requests

from flask import Blueprint, request, jsonify
from config import UPLOAD_FOLDER, CICFLOWMETER_URL, MODEL_FOLDER, UTILS_FOLDER
from utils.classification_preprocessor import ClassificationPreprocessor


manage_bp = Blueprint('manage', __name__)

@manage_bp.route('/convert', methods=['POST'])
def convert_pcap():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400
        
        # Save file temporarily with new name
        file_name = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)
        
        response = requests.get(
            f"{CICFLOWMETER_URL}/convert/{file_name}"
        )
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({"error": "Conversion failed", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@manage_bp.route('/classify', methods=['POST'])
def classify():
    """
    Classify netflow data using selected model.

    Request JSON:
        - model: model filename (e.g. "svc_bin.pkl")
        - file: netflow CSV filename

    Response JSON:
        - statistics: dict with counts and percentages per class
        - predictions: list of {flow_id, src_ip, dst_ip, timestamp, prediction}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        model_name = data.get('model')
        file_name = data.get('file')

        if not model_name or not file_name:
            return jsonify({"error": "Both 'model' and 'file' are required"}), 400

        # Load model
        model_path = os.path.join(MODEL_FOLDER, model_name)
        if not os.path.isfile(model_path):
            return jsonify({"error": f"Model {model_name} not found"}), 404

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Preprocess data
        preprocessor = ClassificationPreprocessor(file_name)
        X_pca, id_columns = preprocessor.preprocess()

        # Predict (use .values to avoid feature names warning)
        predictions_raw = model.predict(X_pca.values)

        # Check if model uses LabelEncoder (KNN multi-class)
        if model_name.startswith('knn') and 'bin' not in model_name:
            label_encoder_path = os.path.join(UTILS_FOLDER, 'label_encoder.pkl')
            with open(label_encoder_path, 'rb') as f:
                label_encoder = pickle.load(f)
            predictions_labels = label_encoder.inverse_transform(predictions_raw)
        elif 'bin' in model_name:
            # Binary model: 0 = BENIGN, 1 = ATTACK
            predictions_labels = ['BENIGN' if p == 0 else 'ATTACK' for p in predictions_raw]
        else:
            # Multi-class model with string labels
            predictions_labels = predictions_raw

        # Build predictions list
        predictions = []
        for i, pred in enumerate(predictions_labels):
            predictions.append({
                "flow_id": str(id_columns.iloc[i]["Flow ID"]),
                "src_ip": str(id_columns.iloc[i]["Src IP"]),
                "dst_ip": str(id_columns.iloc[i]["Dst IP"]),
                "timestamp": str(id_columns.iloc[i]["Timestamp"]),
                "prediction": str(pred)
            })

        # Calculate statistics
        from collections import Counter
        counts = Counter(predictions_labels)
        total = len(predictions_labels)
        statistics = {
            "total": total,
            "counts": dict(counts),
            "percentages": {k: round(v / total * 100, 2) for k, v in counts.items()}
        }

        return jsonify({
            "statistics": statistics,
            "predictions": predictions
        }), 200

    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
