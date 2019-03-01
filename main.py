from flask import Flask, request, url_for, render_template
from flask_restplus import Resource, Api, fields
import json

app = Flask(__name__)
app.config['DATA_PATH'] = './data/data.json'

api = Api(app,
          title="Office API",
          description="A Restful-API by Daniel.",
          validate=True)


an_employee = api.model('Employee',
                        {
                            "full-name": fields.String(required=True,
                                                       description="Full name of employee."),
                            "occupation": fields.String(required=True,
                                                        description="Job title in company."),
                            "hours-worked": fields.Integer(required=True,
                                                           description="Number of hours worked for company.")
                        })


an_office = api.model('Office',
                      {
                          "name": fields.String(required=True,
                                                description="Office name."),
                          "address": fields.String(required=True,
                                                   description="Office address."),
                          "postcode": fields.Integer(required=True,
                                                     description="Office postcode.")
                      })

an_occupation = api.model('Occupation',
                          {
                              "title": fields.String(required=True,
                                                     description="Job title.") ,
                              "salary": fields.Integer(required=True,
                                                       description="Job salary.") ,
                              "bonus": fields.Integer(required=True,
                                                      description="Job salary bonus.") ,
                              "capacity": fields.Integer(required=True,
                                                         description="Job capacity (positions).") 
                          })


# Read in Data
with open(app.config['DATA_PATH'], 'r') as f:
    data = json.load(f)


def save_data(data):
    """Simple data saving function to be called at the end of POST methods."""
    with open(app.config['DATA_PATH'], 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
        f.close()


@api.route('/api/occupations/list')
class Occupation(Resource):
    def get(self):

        result_set = [item['id'] for item in data['occupations']]
        return result_set


@api.route('/api/offices/list')
class Office(Resource):
    def get(self):

        result_set = [item['id'] for item in data['offices']]
        return result_set


@api.route('/api/employees/list')
class Employee(Resource):
    def get(self):

        result_set = [item['id'] for item in data['employees']]
        return result_set


@api.route('/api/occupations/view/all')
class Occupation(Resource):
    def get(self):
        return data['occupations']


@api.route('/api/occupations/<string:ID>')
class Occupation(Resource):
    def get(self, ID):

        # Filter results by id
        result_set = [item for item in data['occupations'] if ID == item['id']]

        # If results exceeds 0, return the first result from the list
        if len(result_set) > 0:
            return result_set[0]
        else:
            return {"message": "No results found for occupations id {}".format(ID)}

    @api.expect(an_occupation)
    def post(self, ID):

        # Handle if result set is empty, if not find out if ID exists
        if len(data['occupations']) == 0:
            result_set = None
        else:
            result_set = [item for item in data['occupations'] if ID == item["id"]]

        if result_set:
            return {"message": "ID already exists. Choose another one"}
        else:
            post_data = api.payload
            post_data["id"] = ID
            data['occupations'].append(post_data)
            save_data(data)
            return data['occupations']


@api.route('/api/offices/view/all')
class Office(Resource):
    def get(self):
        return data['offices']


@api.route('/api/offices/<string:ID>')
class Office(Resource):
    def get(self, ID):

        # Filter results by id
        result_set = [item for item in data['offices'] if ID == item['id']]

        # If results exceeds 0, return the first result from the list
        if len(result_set) > 0:
            return result_set[0]
        else:
            return {"message": "No results found for office id {}".format(ID)}

    @api.expect(an_office)
    def post(self, ID):

        # Handle if result set is empty, if not find out if ID exists
        if len(data['offices']) == 0:
            result_set = None
        else:
            result_set = [item for item in data['offices'] if ID == item["id"]]

        if result_set:
            return {"message": "ID already exists. Choose another one"}
        else:
            post_data = api.payload
            post_data["id"] = ID
            data['offices'].append(post_data)
            save_data(data)
            return data['offices']


@api.route('/api/employees/view/all')
class Employee(Resource):
    def get(self):
        return data['employees']


@api.route('/api/employees/<string:ID>')
class Employee(Resource):
    def get(self, ID):

        # Filter results by id
        result_set = [item for item in data['employees'] if ID == item['id']]

        # If results exceeds 0, return the first result from the list
        if len(result_set) > 0:
            return result_set[0]
        else:
            return {"message": "No results found for employee id {}".format(ID)}

    @api.expect(an_employee)
    def post(self, ID):

        # Handle if result set is empty, if not find out if ID exists
        if len(data['employees']) == 0:
            result_set = None
        else:
            result_set = [item for item in data['employees'] if ID == item["id"]]

        if len(result_set) > 0:
            return {"message": "ID already exists. Choose another one"}
        else:
            post_data = api.payload
            post_data["id"] = ID
            data['employees'].append(post_data)
            save_data(data)
            return data['employees']


if __name__ == '__main__':
    app.run(debug=True)