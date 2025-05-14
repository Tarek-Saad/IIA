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

        # Process the LO ID - extract numeric part if it's a complex ID
        try:
            if isinstance(lo_id, str):
                if ':' in lo_id:
                    # Extract the part after the last colon (which is the numeric ID)
                    numeric_part = lo_id.split(':')[-1]
                    if numeric_part.isdigit():
                        lo_id = int(numeric_part)
                elif lo_id.isdigit():
                    lo_id = int(lo_id)
            # If it's already a number, it's fine
        except Exception as e:
            print(f"Warning: Could not process complex LO ID: {e}")
            # Continue with original lo_id if conversion fails

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
