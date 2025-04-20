from flask import Blueprint, request, jsonify
from src.algorithms.iia.LOChildFetcher import LOChildFetcher

lo_child_controller = Blueprint('lo_child_controller', __name__)

@lo_child_controller.route('/lo/child-sub-los', methods=['POST'])
def get_sub_los_by_lo_id():
    try:
        data = request.get_json()
        lo_id = data.get('lo_id')

        if lo_id is None:
            return jsonify({"error": "Missing 'lo_id' in request body"}), 400

        fetcher = LOChildFetcher()
        sub_los = fetcher.get_ordered_sub_los_by_internal_id(lo_id)

        formatted_sub_los = [
            {
                "name": sub.get("name", "Unnamed"),
                "material": sub.get("material", "No material found"),
                "reference": sub.get("reference", "No reference")
            }
            for sub in sub_los
        ]

        return jsonify({
            "lo_id": lo_id,
            "sub_los": formatted_sub_los
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
