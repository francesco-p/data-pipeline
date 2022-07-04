#!/usr/bin/env python3

class OPT:
    APP_CACHE_IMG_FOLDER = "/data/francesco.pelosin"
    APP_CACHE_CSV_PATH = "/data/francesco.csv"
    APP_OUTPUT = '/data/output.json'

    CSV_COLUMNS = 'SourceFile,ExifToolVersion,FileName,Directory,FileSize,FileModifyDate,FileAccessDate,FileInodeChangeDate,FilePermissions,FileType,FileTypeExtension,MIMEType,CurrentIPTCDigest,ImageWidth,ImageHeight,EncodingProcess,BitsPerSample,ColorComponents,YCbCrSubSampling,JFIFVersion,ResolutionUnit,XResolution,YResolution,SpecialInstructions,ImageSize,Megapixels'

    MINIO_URL = "storage:9000"
    MINIO_ACCESS_KEY = "minioadmin"
    MINIO_SECRET_KEY = "minioadmin"
    MINIO_BUCKET_NAME = "francesco-pics"

    PYSPARK_APP_NAME = "PySpark_MySQL"
    PYSPARK_MYSQL_CONNECTOR_JAR_PATH = "/code/mysql-connector-java-8.0.11.jar"

    MYSQL_URL = "database:3306"
    MYSQL_USER = "user"
    MYSQL_PSW = "password"
    MYSQL_DB = "db"
    MYSQL_TABLE_NAME = "TestTable"