## Running the app:

1. Install requirements
2. Unzip data.zip
3. run the app

        python app.py
        
4. open browser and request predictions, e.g.

        http://127.0.0.1:5000/predict_clv/000011265b8a3727c4cc77b494134aca/
        


## Questions

#### How​ ​would​ ​you​ ​deploy​ ​the​ ​app?
API: Own app server or cloud, e.g. AWS Lambda

Databases: Redis/some cloud key-value store for predictions, Monet DB/some cloud columnar DB for order data.


#### How​ ​to​ ​schedule​ ​the​ ​ETL​ ​job?
Instead of a csv file, the raw data would probably be stored in a (columnar?) database;
the group by ops could be handled by the DB directly.

Predictions would be run periodically (e.g. every hour), depending on the data size possibly
only for a subset of the data, e.g. orders of the last 180 days.

The predictions could be stored in-memory on the app server or for larger datasets in a
key-value store (e.g. Redis).
 