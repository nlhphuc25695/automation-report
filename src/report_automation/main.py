from __future__ import annotations

import argparse
import logging
import sys

from report_automation.config import load_config
from report_automation.config_form import build_config_interactive, write_config
from report_automation.orchestrator import run_monthly_job


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def _run_job(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    results = run_monthly_job(
        config=config,
        target_month=args.month,
        credentials_path=args.credentials,
    )

    for result in results:
        logging.info(
            "Client %s: status=%s daily_rows=%s summary_rows=%s sheet=%s slides=%s errors=%s",
            result.client_id,
            result.status,
            result.daily_rows,
            result.summary_rows,
            result.sheet_url,
            result.slides_url,
            result.errors,
        )


def _init_config(args: argparse.Namespace) -> None:
    config = build_config_interactive()
    write_config(config, args.output)
    logging.info("Config written to %s", args.output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monthly Ads Reporting Automation")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run the monthly reporting job")
    run_parser.add_argument("--config", required=True, help="Path to clients config YAML")
    run_parser.add_argument(
        "--credentials",
        default="config/ads_credentials.yaml",
        help="Path to ads credentials YAML",
    )
    run_parser.add_argument("--month", help="Target month in YYYY-MM (default: previous month)")
    run_parser.set_defaults(func=_run_job)

    init_parser = subparsers.add_parser("init-config", help="Interactive config form")
    init_parser.add_argument("--output", default="config/clients.yaml", help="Output YAML path")
    init_parser.set_defaults(func=_init_config)

    if len(sys.argv) > 1 and sys.argv[1] not in {"run", "init-config"}:
        args = parser.parse_args(["run", *sys.argv[1:]])
    else:
        args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
