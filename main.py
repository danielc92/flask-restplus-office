from flask import Flask, request, url_for, render_template
from flask_restplus import Resource, Api, fields
import json

app = Flask(__name__)
api = Api(app,
          title="Office API",
          description="A test restful-api by Daniel.",
          validate=True)


an_employee = api.model('Employee',
                        {
                            "full-name": fields.String(required=True, description="Full name of employee."),
                            "occupation": fields.String(required=True, description="Job title in company."),
                            "hours-worked": fields.Integer(required=True, description="Number of hours worked for company.")
                        })


an_office = api.model('Office',
                      {
                          "name": fields.String(required=True, description="Office name."),
                          "address": fields.String(required=True, description="Office address."),
                          "postcode": fields.Integer(required=True, description="Office postcode.")
                      })


# Read in Data
with open('./data.json', 'r') as f:
    data = json.load(f)


@api.route('/export')
class Export(Resource):
    def get(self):
        with open('./data2.json', 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)
            f.close()
        return {"message": "Data saved locally."}


@api.route('/employees')
class Employee(Resource):
    def get(self):
        return data['employees']


@api.route('/employees/<string:emp_id>')
class Employee(Resource):
    def get(self, emp_id):

        result_set = [e for e in data['employees'] if emp_id == e['id']]

        if len(result_set) > 0:
            # Return the first result from the list if results are found.
            return result_set[0]
        else:
            # Return no results feedback
            return {"message": "No results found for employee id {}".format(emp_id)}

    @api.expect(an_employee)
    def post(self, emp_id):

        result_set = [e for e in data['employees'] if emp_id == e["id"]]

        if len(result_set) > 0:
            return {"message": "ID already exists. Choose another one"}
        else:
            post_data = api.payload
            post_data["id"] = emp_id
            data['employees'].append(post_data)
            return data['employees']

if __name__ == '__main__':
    app.run(debug=True)