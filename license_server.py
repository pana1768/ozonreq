from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LICENSES_FILE = "licenses.json"

# Загрузка лицензий из файла
def load_licenses():
    if os.path.exists(LICENSES_FILE):
        with open(LICENSES_FILE, "r") as file:
            return json.load(file)
    return {}

# Сохранение лицензий в файл
def save_licenses(licenses):
    with open(LICENSES_FILE, "w") as file:
        json.dump(licenses, file, indent=4)

# Проверка лицензии
@app.route('/verify_license', methods=['POST'])
def verify_license():
    data = request.json
    license_key = data.get("license_key")
    device_id = data.get("device_id")

    licenses = load_licenses()
    license_info = licenses.get(license_key)

    # Проверка существования, соответствия устройству и статуса лицензии
    if license_info and license_info.get("device_id") == device_id and license_info.get("status") == "active":
        return jsonify({"status": "valid"}), 200
    else:
        return jsonify({"status": "invalid"}), 403

# Отключение лицензии
@app.route('/deactivate_license', methods=['POST'])
def deactivate_license():
    data = request.json
    license_key = data.get("license_key")

    licenses = load_licenses()
    if license_key in licenses:
        licenses[license_key]["status"] = "inactive"
        save_licenses(licenses)
        return jsonify({"status": "deactivated"}), 200
    else:
        return jsonify({"status": "license_not_found"}), 404

if __name__ == "__main__":
    app.run(port=5000)
