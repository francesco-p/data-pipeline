#!/usr/bin/env python3

import subprocess
import glob
from minio import Minio
from minio.error import S3Error
from exiftool import ExifTool
from pyspark.sql import SparkSession
import pandas as pd
from opt import OPT
import json


def dic_to_row(dictionary):
    """ Given a dict it creates a .csv row
    Args:
    dictionary -- dict(str:str)
    return -- str
    """
    values = []
    for k in dictionary:
        values.append(str(dictionary[k]))
    return ', '.join(values)


def store_imgs_to_minio(df):
    """ Parse a list of paths and move the files to a minio bucket
    Args:
    df -- pandas.DataFrame with SourceFile column as paths
    return -- None
    """
    try:
        # Create a client
        client = Minio(OPT.MINIO_URL, access_key=OPT.MINIO_ACCESS_KEY, secret_key=OPT.MINIO_SECRET_KEY, secure=False)

        # Make bucket
        found = client.bucket_exists(OPT.MINIO_BUCKET_NAME)
        if not found:
            client.make_bucket(OPT.MINIO_BUCKET_NAME)
        else:
            print(f"Bucket {OPT.MINIO_BUCKET_NAME} already exists")

        # Upload EXIF csv 
        client.fput_object(OPT.MINIO_BUCKET_NAME, OPT.APP_CACHE_CSV_PATH.split('/')[-1], OPT.APP_CACHE_CSV_PATH)

        # Upload imgs
        for img_path in df['SourceFile'].values:
            client.fput_object(OPT.MINIO_BUCKET_NAME, f"imgs/{img_path.split('/')[-1]}", img_path)
            print(f"[ OK ] {img_path.split('/')[-1]} Uploaded!")

    except S3Error as exc:
        print("[ X ]  occurred in minio.", exc)


def dwnld_data():
    """ Download imgs batch data and returns a pandas dataframe with EXIF info
    Args:
    returns -- pandas.DataFrame, where each entry is the EXIF of each dwnloaded img
    """

    # Download a batch of Images from Instagram
    subprocess.call(['instaloader', 'francesco.pelosin', '--no-captions', '--no-video-thumbnails', '--no-videos','--no-metadata-json', '--dirname-pattern', OPT.APP_CACHE_IMG_FOLDER])
    
    # Create a .csv from images' EXIF
    img_paths = [fname for fname in glob.glob(f"{OPT.APP_CACHE_IMG_FOLDER}/*.jpg")]

    with ExifTool() as e:
        with open(OPT.APP_CACHE_CSV_PATH, 'w') as f:
            f.write(f'{OPT.CSV_COLUMNS}\n')
            for img_path in img_paths:
                f.write(f'{dic_to_row(e.get_metadata(img_path)[0])}\n')
    df = pd.read_csv(OPT.APP_CACHE_CSV_PATH)

    return df 


def connect_and_query(df):
    """ Write spark dataframe to mysql database and return the results of 2 queries
    Args:
    df -- pandas.DataFrame
    returns -- json, object with the output template form 
    """

    spark = SparkSession.builder.config("spark.jars", OPT.PYSPARK_MYSQL_CONNECTOR_JAR_PATH).master("local").appName(OPT.PYSPARK_APP_NAME).getOrCreate()

    sparkDF=spark.createDataFrame(df) 

    sparkDF.write.format('jdbc').options(
        url=f'jdbc:mysql://{OPT.MYSQL_URL}/{OPT.MYSQL_DB}?allowPublicKeyRetrieval=true&useSSL=false',
        driver='com.mysql.jdbc.Driver',
        dbtable=OPT.MYSQL_TABLE_NAME,
        user=OPT.MYSQL_USER,
        password=OPT.MYSQL_PSW).mode('append').save()

    sparkDF.createGlobalTempView(OPT.MYSQL_TABLE_NAME)
    
    output = {}

    # Process output for query 1
    df = spark.sql(f"SELECT COUNT(SourceFile), ImageWidth FROM global_temp.{OPT.MYSQL_TABLE_NAME} GROUP BY ImageWidth")
    df.show()    
    df2 = df.toPandas()
    keys = [int(x) for x in df2[df2.columns[1]].values]
    values = [int(x) for x in df2[df2.columns[0]].values]
    output['ImageWidth'] = dict(zip(keys, values))
    
    # Process output for query 2
    df = spark.sql(f"SELECT COUNT(SourceFile), Megapixels FROM global_temp.{OPT.MYSQL_TABLE_NAME} GROUP BY Megapixels")
    df.show()
    df2 = df.toPandas()
    keys = [str(x) for x in df2[df2.columns[1]].values]
    values = [int(x) for x in df2[df2.columns[0]].values]
    output['Megapixels'] = dict(zip(keys, values))

    return json.dumps(output)

def main():

    # Step 2  
    df  = dwnld_data()
    # Step 3 4
    store_imgs_to_minio(df)    
    # Step 5 and 6
    out = connect_and_query(df)
    # Write output
    with open(OPT.APP_OUTPUT, 'w') as f:
        f.write(out)
    print(f'Json output: {out}')
    print('Finish!')

if __name__ == '__main__':
    main()



