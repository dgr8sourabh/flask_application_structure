import warnings
from logging import exception

from flask import Blueprint, request, abort, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.models.database_connectivity import session_scope
from app.models.model_designer import *


warnings.filterwarnings("ignore")

dashboard_bp = Blueprint("loan+qc_dashboard", __name__)

api_dashboard = Api(dashboard_bp)


class LoanQcDashboard(Resource):
    def get(self):
        try:
            with session_scope('PRIMARY') as session:
                dashboard_data_obj = session.query(AIDrivenInsightsDashboard).all()
                print(dashboard_data_obj)
        except Exception as e:
            print(e)


api_dashboard.add_resource(LoanQcDashboard, '/dashboard_country')
