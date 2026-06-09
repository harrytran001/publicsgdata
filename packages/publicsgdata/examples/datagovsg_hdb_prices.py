"""Fetch a sample of HDB resale flat prices from data.gov.sg."""

from publicsgdata import DataGovSGClient

HDB_RESALE_DATASET_ID = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"


def main() -> None:
    with DataGovSGClient() as client:
        response = client.datasets.list_rows(HDB_RESALE_DATASET_ID, limit=5)
        print(f"Dataset: {response.dataset_name}")
        for row in response.rows:
            data = row.model_dump()
            print(f"{data.get('month')} | {data.get('town')} | ${data.get('resale_price')}")


if __name__ == "__main__":
    main()
