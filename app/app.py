from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection URL and database/collection names
url = 'mongodb://localhost:27017'
dbName = 'Finance'
client = MongoClient(url)
db = client[dbName]

@app.route('/')
def index():
    try:
        # Fetch the list of collections (industries)
        collections = db.list_collection_names()
        industries = collections

        # Fetch the selected industry from query parameters
        selected_industry = request.args.get('industry', industries[0])
        collection = db[selected_industry]

        # Fetch distinct sectors
        sectors = collection.distinct('Industry')

        # Fetch the selected sector from query parameters
        selected_sector = request.args.get('sector', sectors[0])

        # Fetch sorting criteria from query parameters
        sort_by = request.args.get('sort_by', 'Revenue ($B)')
        sort_order = request.args.get('sort_order', 'desc')
        sort_direction = 1 if sort_order == 'asc' else -1

        # Create sort field
        if sort_by in ["Revenue ($B)", "Net income ($B)", "Market Cap ($B)"]:
            sort_field = f"Income.{sort_by}"
        elif sort_by == "Free cash flow ($B)":
            sort_field = f"Cash Flow.{sort_by}"

        # Fetch the top 20 items sorted by the selected field and order
        items = list(collection.find({'Industry': selected_sector})
                     .sort([(sort_field, sort_direction)])
                     .limit(20))

        return render_template('index.html', items=items, industries=industries,
                               selected_industry=selected_industry, 
                               sectors=sectors, selected_sector=selected_sector,
                               sort_by=sort_by, sort_order=sort_order)
    except Exception as e:
        print('Error connecting to MongoDB or fetching data:', e)
        return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(port=3000)
