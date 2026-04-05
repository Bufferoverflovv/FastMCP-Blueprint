from __future__ import annotations

import argparse
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a local development TLS certificate for FastMCP-Blueprint."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("server.pem"),
        help="Path to the combined PEM file containing the private key and certificate chain.",
    )
    parser.add_argument(
        "--ca-output",
        type=Path,
        default=Path("server-ca.pem"),
        help="Path to the generated local certificate authority PEM file.",
    )
    parser.add_argument(
        "--hostname",
        action="append",
        dest="hostnames",
        default=None,
        help="Additional hostname or IP address to include in the certificate. Repeat as needed.",
    )
    return parser


def _write_dev_cert(output_path: Path, ca_output_path: Path, hostnames: list[str]) -> None:
    try:
        import trustme
    except ImportError as exc:
        raise SystemExit(
            "trustme is required to generate local development certificates. "
            'Install dev dependencies with: uv pip install -e ".[dev]"'
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ca_output_path.parent.mkdir(parents=True, exist_ok=True)

    ca = trustme.CA()
    certificate = ca.issue_cert(*hostnames)

    output_path.write_bytes(
        certificate.private_key_pem.bytes()
        + b"".join(blob.bytes() for blob in certificate.cert_chain_pems)
    )
    ca_output_path.write_bytes(ca.cert_pem.bytes())


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    hostnames = ["localhost", "127.0.0.1", "::1"]
    if args.hostnames:
        for hostname in args.hostnames:
            if hostname not in hostnames:
                hostnames.append(hostname)

    _write_dev_cert(args.output, args.ca_output, hostnames)

    print(f"Wrote development certificate to {args.output}")
    print(f"Wrote local CA certificate to {args.ca_output}")
    print("Use SSL_CERTFILE to point at the combined PEM file.")


if __name__ == "__main__":
    main()
