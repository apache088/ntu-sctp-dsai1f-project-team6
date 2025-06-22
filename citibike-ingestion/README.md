# Citibike Trip Data Extraction and Loading

![image alt](https://github.com/apache088/ntu-sctp-dsai1f-project-team6/blob/dev/assets/meltano_data_ingestation.jpg)

Data is downloaded as csv file from the citybikenyc website ([here ](https://citibikenyc.com/system-data) and [here](https://s3.amazonaws.com/tripdata/index.html)) and load into DuckDB (local data source).

Load csv file into DuckDB:
- We have provided 2 ways to perform this:
  - A Jupyter notebook at notebooks/[create_db.ipynb](../notebooks/create_db.ipynb)
  - A Python script at duckdb/[load_csv_to_duckdb.py](../duckdb/load_csv_to_duckdb.py)
- Each of the above methods will produce an output database file at its specified location.
  - For subsequent meltano steps, please ensure the `DUCKDB_PATH` in your [.env](../.env) file reflects the actual path to the file.
- Notes:
  - Using just 1 of the above methods is sufficient.
  - Please ensure the expected csv file (data/in/[JC-202505-citibike-tripdata.csv](../data/in/JC-202505-citibike-tripdata.csv)) is at the location required by the notebook/script before executing them.

We use Meltano to orchestrate an EL pipeline:

  1) Extractor ( tap-duckdb ): to stream the raw data out of DuckDB

  2) Loader ( target-bigquery ): will receive that stream and load it into BigQuery inside Google Cloud Project

After loading the raw data into BigQuery, we verify the ingestion by comparing the row count in the source file with the row count in BigQuery (see screenshots below circle in <code style="color : red">**red**</code>).

<p align="middle">
  <img src="https://github.com/apache088/ntu-sctp-dsai1f-project-team6/blob/dev/assets/excel_data_rows.jpg" width="400" />
  <img src="https://github.com/apache088/ntu-sctp-dsai1f-project-team6/blob/dev/assets/bigquery_data_rows.jpg" width="600" /> 
</p>

Once ther are similar, we will move to [dbt](../citibike_dbt/README.md) to clean, test and model the newly-ingested data.
