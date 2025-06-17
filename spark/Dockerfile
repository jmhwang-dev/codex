FROM bitnami/spark:4.0.0

COPY convert_csv_to_iceberg.py /opt/spark/work-dir/

CMD ["/opt/bitnami/scripts/spark/entrypoint.sh", "bash"]
