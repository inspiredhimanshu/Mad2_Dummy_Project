from flask import Flask # type: ignore
from flask_security import Security # type: ignore
from flask_restful import Api # type: ignore



from controllers.database import db
from controllers.config import Config as config
from controllers.user_datastore import user_datastore



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    
    security = Security(app,user_datastore)
    
    api = Api(app, prefix = '/api')
    
    
    with app.app_context():
        db.create_all()
        
        admin_role = user_datastore.find_or_create_role(name = 'admin', description = 'Administrator')
        user_role = user_datastore.find_or_create_role(name = 'user', description = 'Regular User')
        
        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(
                email = 'admin@gmail.com',
                password = 'admin123',
                roles = [admin_role]
            )
        
        db.session.commit()
        
    return app,api

    
    
app,api = create_app()


@app.route("/")
def home():
    return {
        'message':"Welcome to the Flask API!"
        },200
    
    
    
# class Index(Resource):
#     def get(self):
#         return {
#             'message':"Welcome to the Flask API!"
#             },200
# api.add_resource(Index,'/')


from controllers.authentication_api import LoginAPI,LogoutAPI,RegisterAPI # type: ignore
api.add_resource(LoginAPI,'/login')
api.add_resource(LogoutAPI,'/logout')
api.add_resource(RegisterAPI,'/register')

from controllers.crud_apis import CategoryCRUDAPI 
api.add_resource(CategoryCRUDAPI,'/categories','/categories/<int:category_id>')



if __name__ == "__main__":
    app.run(debug = True) # pyright: ignore[reportAttributeAccessIssue]