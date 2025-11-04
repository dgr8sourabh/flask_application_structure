from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

homepage_bp = Blueprint("homepage", __name__)

api_homepage = Api(homepage_bp)


class SdStaticHomePage(Resource):
    def get(self):
        return str("welcome to the homepage of LOAN QC MARSHALL")


api_homepage.add_resource(SdStaticHomePage, '/')
