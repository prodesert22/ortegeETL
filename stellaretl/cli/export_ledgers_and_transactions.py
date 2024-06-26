import click

from stellaretl.jobs.export_ledgers_job import ExportLedgersJob
from stellaretl.jobs.exporters.ledgers_and_transactions_item_exporter import ledgers_and_transactions_item_exporter
from stellaretl.api.horizon_api import HorizonApi
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-ledger', default=0, type=int, help='Start ledger sequence')
@click.option('-e', '--end-ledger', required=True, type=int, help='End ledger sequence')
@click.option('-b', '--batch-size', default=1, type=int, help='The number of ledgers to export at a time.')
@click.option('-a', '--api-uri', default='https://horizon-testnet.stellar.org', type=str,
              help='The URI of the Horizon api')
@click.option('-w', '--max-workers', default=5, type=int, help='The maximum number of workers.')
@click.option('--ledgers-output', default=None, type=str,
              help='The output file for ledgers. '
                   'If not provided ledgers will not be exported. Use "-" for stdout')
@click.option('--transactions-output', default=None, type=str,
              help='The output file for transactions. '
                   'If not provided transactions will not be exported. Use "-" for stdout')
def export_ledgers_and_transactions(start_ledger, end_ledger, batch_size, api_uri,
                                   max_workers, ledgers_output, transactions_output):
    """Export blocks and transactions."""
    if ledgers_output is None and transactions_output is None:
        raise ValueError('Either --ledgers-output or --transactions-output options must be provided')

    job = ExportLedgersJob(
        start_ledger=start_ledger,
        end_ledger=end_ledger,
        batch_size=batch_size,
        horizon_api=HorizonApi(api_uri),
        max_workers=max_workers,
        item_exporter=ledgers_and_transactions_item_exporter(ledgers_output, transactions_output),
        export_ledgers=ledgers_output is not None,
        export_transactions=transactions_output is not None)
    job.run()
