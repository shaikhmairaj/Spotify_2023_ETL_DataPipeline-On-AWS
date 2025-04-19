import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node tracks
tracks_node1744983693501 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-datasetunique-2023/staging/spotify_tracks_data_2023.csv"], "recurse": True}, transformation_ctx="tracks_node1744983693501")

# Script generated for node album
album_node1744983692607 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-datasetunique-2023/staging/spotify-albums_data_2023.csv"], "recurse": True}, transformation_ctx="album_node1744983692607")

# Script generated for node artist
artist_node1744983691718 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-datasetunique-2023/staging/spotify_artist_data_2023.csv"], "recurse": True}, transformation_ctx="artist_node1744983691718")

# Script generated for node Join Album &Artist
JoinAlbumArtist_node1744983887630 = Join.apply(frame1=album_node1744983692607, frame2=artist_node1744983691718, keys1=["artist_id"], keys2=["id"], transformation_ctx="JoinAlbumArtist_node1744983887630")

# Script generated for node Join 
Join_node1744984382056 = Join.apply(frame1=tracks_node1744983693501, frame2=JoinAlbumArtist_node1744983887630, keys1=["id"], keys2=["track_id"], transformation_ctx="Join_node1744984382056")

# Script generated for node Drop Fields
DropFields_node1744987894963 = DropFields.apply(frame=Join_node1744984382056, paths=["track_id"], transformation_ctx="DropFields_node1744987894963")

# Script generated for node Destination
EvaluateDataQuality().process_rows(frame=DropFields_node1744987894963, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744983642148", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Destination_node1744988145026 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1744987894963, connection_type="s3", format="glueparquet", connection_options={"path": "s3://spotify-datasetunique-2023/datawarehouse/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="Destination_node1744988145026")

job.commit()