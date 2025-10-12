"""Utility script to update Inkthreadable-managed inventory locations.

This script scans Shopify products associated with Inkthreadable or
Spreadconnect and adjusts inventory locations and quantities to use the Lille
Bislett 16 location while keeping the existing SKU and fulfillment linkage
intact.

Usage example:
    python scripts/update_inkthreadable_inventory.py \
        --store-domain example.myshopify.com \
        --access-token <TOKEN>

Environment variables SHOPIFY_STORE_DOMAIN and SHOPIFY_ACCESS_TOKEN can be used
instead of command-line arguments. Use --dry-run to preview the changes without
calling the Shopify Admin API.
"""
from __future__ import annotations

import argparse
import base64
import logging
import os
import sys
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Sequence

import requests


API_VERSION_DEFAULT = "2023-10"
DEFAULT_QUERY = "vendor:Inkthreadable OR vendor:Spreadconnect"
DEFAULT_TARGET_LOCATION = "Lille Bislett 16"
DEFAULT_SOURCE_LOCATIONS = (
    "Multiple locations",
    "Inkthreadable Warehouse",
    "Spreadconnect Warehouse",
)
GRAPHQL_ENDPOINT = "admin/api/{version}/graphql.json"
REST_ENDPOINT = "admin/api/{version}/{path}"


@dataclass
class InventoryLevel:
    """Represents an inventory level for a variant at a specific location."""

    location_name: str
    location_id: str
    available: int


@dataclass
class VariantInventoryState:
    """Snapshot of inventory information for a product variant."""

    variant_gid: str
    sku: str
    product_title: str
    variant_title: str
    inventory_policy: str
    inventory_item_gid: str
    levels: List[InventoryLevel]

    @property
    def variant_id(self) -> str:
        return gid_to_id(self.variant_gid)

    @property
    def inventory_item_id(self) -> str:
        return gid_to_id(self.inventory_item_gid)


class ShopifyInventoryUpdater:
    def __init__(
        self,
        session: requests.Session,
        store_domain: str,
        api_version: str,
        target_location: str,
        source_locations: Sequence[str],
        dry_run: bool = False,
    ) -> None:
        self.session = session
        self.store_domain = store_domain
        self.api_version = api_version
        self.target_location = target_location
        self.source_locations = tuple(source_locations)
        self.dry_run = dry_run
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self, product_query: Optional[str]) -> None:
        locations = self._fetch_locations()
        location_by_name = {loc["name"]: str(loc["id"]) for loc in locations}

        if self.target_location not in location_by_name:
            raise RuntimeError(
                f"Target location '{self.target_location}' not found in store locations."
            )

        target_location_id = location_by_name[self.target_location]
        missing_locations = [
            name for name in self.source_locations if name not in location_by_name
        ]
        if missing_locations:
            self.logger.warning(
                "Source locations missing from store: %s",
                ", ".join(missing_locations),
            )

        source_location_ids = {
            name: location_by_name[name]
            for name in self.source_locations
            if name in location_by_name
        }

        if not source_location_ids:
            self.logger.warning(
                "None of the source locations %s exist in the store; nothing to do.",
                ", ".join(self.source_locations),
            )
            return

        total_variants = 0
        updated_variants = 0

        for state in self._iter_inkthreadable_variants(product_query):
            total_variants += 1
            actions = self._plan_actions(state, source_location_ids, target_location_id)
            if not actions:
                continue

            updated_variants += 1
            self._apply_actions(state, actions)

        self.logger.info(
            "Processed %d variants; updated %d variants needing location changes.",
            total_variants,
            updated_variants,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _fetch_locations(self) -> List[Dict[str, object]]:
        path = REST_ENDPOINT.format(version=self.api_version, path="locations.json")
        url = f"https://{self.store_domain}/{path}"
        response = self.session.get(url)
        self._raise_for_status(response, "Failed to fetch locations")
        payload = response.json()
        return payload.get("locations", [])

    def _iter_inkthreadable_variants(
        self, product_query: Optional[str]
    ) -> Iterator[VariantInventoryState]:
        cursor: Optional[str] = None
        while True:
            data = self._run_graphql_query(
                FETCH_PRODUCTS_QUERY,
                {
                    "cursor": cursor,
                    "query": product_query or DEFAULT_QUERY,
                },
            )

            products = data["products"]
            for edge in products["edges"]:
                product = edge["node"]
                product_title = product["title"]
                for variant_edge in product["variants"]["edges"]:
                    variant = variant_edge["node"]
                    levels = [
                        InventoryLevel(
                            location_name=level_node["location"]["name"],
                            location_id=gid_to_id(level_node["location"]["id"]),
                            available=_extract_available_quantity(level_node),
                        )
                        for level_node in (
                            level_edge["node"]
                            for level_edge in variant["inventoryItem"]["inventoryLevels"]["edges"]
                        )
                    ]

                    yield VariantInventoryState(
                        variant_gid=variant["id"],
                        sku=variant.get("sku", ""),
                        product_title=product_title,
                        variant_title=variant.get("title", ""),
                        inventory_policy=variant.get("inventoryPolicy", ""),
                        inventory_item_gid=variant["inventoryItem"]["id"],
                        levels=levels,
                    )

            page_info = products["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            cursor = page_info["endCursor"]

    def _plan_actions(
        self,
        state: VariantInventoryState,
        source_location_ids: Dict[str, Optional[str]],
        target_location_id: str,
    ) -> List["PlannedAction"]:
        actions: List[PlannedAction] = []
        needs_target = True

        for level in state.levels:
            if level.location_id == target_location_id:
                needs_target = False
            elif level.location_id in source_location_ids.values():
                actions.append(
                    PlannedAction(
                        kind="reassign",
                        location_id=level.location_id,
                        location_name=level.location_name,
                        quantity=level.available,
                    )
                )

        if actions or needs_target:
            actions.append(
                PlannedAction(
                    kind="ensure_target",
                    location_id=target_location_id,
                    location_name=self.target_location,
                    quantity=999,
                )
            )

        if state.inventory_policy.lower() != "continue":
            actions.append(
                PlannedAction(
                    kind="set_inventory_policy",
                    location_id=target_location_id,
                    location_name=self.target_location,
                    quantity=999,
                )
            )

        return actions

    def _apply_actions(self, state: VariantInventoryState, actions: Sequence["PlannedAction"]) -> None:
        variant_label = f"{state.product_title} — {state.variant_title} ({state.sku or 'no SKU'})"
        self.logger.info("Updating %s", variant_label)

        for action in actions:
            if action.kind == "reassign":
                self._handle_reassign(state, action)
            elif action.kind == "ensure_target":
                self._handle_ensure_target(state, action)
            elif action.kind == "set_inventory_policy":
                self._handle_inventory_policy(state)

    def _handle_reassign(self, state: VariantInventoryState, action: "PlannedAction") -> None:
        if self.dry_run:
            self.logger.info(
                "Dry-run: would clear %d units at %s",
                action.quantity,
                action.location_name,
            )
            return

        if action.quantity:
            self._set_inventory_level(state.inventory_item_id, action.location_id, 0)
        self._disconnect_location(state.inventory_item_id, action.location_id)

    def _handle_ensure_target(self, state: VariantInventoryState, action: "PlannedAction") -> None:
        if self.dry_run:
            self.logger.info(
                "Dry-run: would ensure %s has %d units",
                action.location_name,
                action.quantity,
            )
            return

        self._connect_location(state.inventory_item_id, action.location_id)
        self._set_inventory_level(state.inventory_item_id, action.location_id, action.quantity)

    def _handle_inventory_policy(self, state: VariantInventoryState) -> None:
        if self.dry_run:
            self.logger.info("Dry-run: would set inventory policy to CONTINUE")
            return

        path = REST_ENDPOINT.format(
            version=self.api_version,
            path=f"variants/{state.variant_id}.json",
        )
        url = f"https://{self.store_domain}/{path}"
        response = self.session.put(
            url,
            json={"variant": {"id": int(state.variant_id), "inventory_policy": "continue"}},
        )
        self._raise_for_status(response, "Failed to update inventory policy")

    def _set_inventory_level(self, inventory_item_id: str, location_id: str, quantity: int) -> None:
        path = REST_ENDPOINT.format(
            version=self.api_version,
            path="inventory_levels/set.json",
        )
        url = f"https://{self.store_domain}/{path}"
        response = self.session.post(
            url,
            json={
                "location_id": int(location_id),
                "inventory_item_id": int(inventory_item_id),
                "available": quantity,
            },
        )
        self._raise_for_status(response, "Failed to set inventory level")

    def _disconnect_location(self, inventory_item_id: str, location_id: str) -> None:
        path = REST_ENDPOINT.format(
            version=self.api_version,
            path="inventory_levels/delete.json",
        )
        url = f"https://{self.store_domain}/{path}"
        response = self.session.delete(
            url,
            json={
                "location_id": int(location_id),
                "inventory_item_id": int(inventory_item_id),
            },
        )
        if response.status_code == 422:
            # The inventory level might already be disconnected; treat as success.
            self.logger.debug(
                "Location %s already disconnected for inventory item %s",
                location_id,
                inventory_item_id,
            )
            return
        self._raise_for_status(response, "Failed to disconnect location")

    def _connect_location(self, inventory_item_id: str, location_id: str) -> None:
        path = REST_ENDPOINT.format(
            version=self.api_version,
            path="inventory_levels/connect.json",
        )
        url = f"https://{self.store_domain}/{path}"
        response = self.session.post(
            url,
            json={
                "location_id": int(location_id),
                "inventory_item_id": int(inventory_item_id),
            },
        )
        if response.status_code == 422:
            self.logger.debug(
                "Location %s already connected for inventory item %s",
                location_id,
                inventory_item_id,
            )
            return
        self._raise_for_status(response, "Failed to connect location")

    def _run_graphql_query(self, query: str, variables: Dict[str, object]) -> Dict[str, object]:
        path = GRAPHQL_ENDPOINT.format(version=self.api_version)
        url = f"https://{self.store_domain}/{path}"
        response = self.session.post(url, json={"query": query, "variables": variables})
        self._raise_for_status(response, "GraphQL query failed")
        payload = response.json()
        if "errors" in payload:
            raise RuntimeError(payload["errors"])
        return payload["data"]

    def _raise_for_status(self, response: requests.Response, message: str) -> None:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:  # pragma: no cover - network dependent
            detail = None
            try:
                detail = response.json()
            except ValueError:
                pass
            if detail:
                raise RuntimeError(f"{message}: {detail}") from exc
            raise RuntimeError(f"{message}: {response.status_code}") from exc


@dataclass
class PlannedAction:
    kind: str
    location_id: str
    location_name: str
    quantity: int


def gid_to_id(gid: str) -> str:
    """Extract the numeric ID from a Shopify GID string."""

    if gid.isdigit():
        return gid

    try:
        decoded = base64.b64decode(gid).decode()
    except (ValueError, UnicodeDecodeError):
        decoded = gid

    if "/" in decoded:
        return decoded.rsplit("/", 1)[-1]
    return decoded


def _extract_available_quantity(level_node: Dict[str, object]) -> int:
    quantity = level_node.get("available")
    if quantity is None:
        quantity = level_node.get("availableQuantity")
    if quantity is None:
        return 0
    return int(quantity)

# Updated for Shopify Admin API 2024-07: replaced 'available' with 'availableQuantity'
FETCH_PRODUCTS_QUERY = """
query FetchProducts($cursor: String, $query: String) {
  products(first: 50, after: $cursor, query: $query) {
    edges {
      node {
        title
        variants(first: 100) {
          edges {
            node {
              id
              title
              sku
              inventoryPolicy
              inventoryItem {
                id
                inventoryLevels(first: 10) {
                  edges {
                    node {
                      id
                      availableQuantity
                      location {
                        name
                      }
                      inventoryItem {
                        id
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--store-domain",
        default=os.getenv("SHOPIFY_STORE_DOMAIN"),
        help="Shopify store domain (e.g. example.myshopify.com)",
    )
    parser.add_argument(
        "--access-token",
        default=os.getenv("SHOPIFY_ACCESS_TOKEN"),
        help="Private app or custom app access token",
    )
    parser.add_argument(
        "--api-version",
        default=os.getenv("SHOPIFY_API_VERSION", API_VERSION_DEFAULT),
        help="Shopify Admin API version",
    )
    parser.add_argument(
        "--product-query",
        default=os.getenv("INKTHREADABLE_PRODUCT_QUERY", DEFAULT_QUERY),
        help="Product query string to identify Inkthreadable-linked items",
    )
    parser.add_argument(
        "--target-location",
        default=os.getenv("INKTHREADABLE_TARGET_LOCATION", DEFAULT_TARGET_LOCATION),
        help="Target location name to assign inventory to",
    )
    parser.add_argument(
        "--source-locations",
        default=os.getenv("INKTHREADABLE_SOURCE_LOCATIONS", ",".join(DEFAULT_SOURCE_LOCATIONS)),
        help="Comma-separated list of source location names to migrate from",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Log planned changes without modifying Shopify data",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Logging level (e.g. INFO, DEBUG)",
    )
    return parser


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if not args.store_domain:
        parser.error("--store-domain or SHOPIFY_STORE_DOMAIN is required")
    if not args.access_token:
        parser.error("--access-token or SHOPIFY_ACCESS_TOKEN is required")

    configure_logging(args.log_level)

    session = requests.Session()
    session.headers.update(
        {
            "X-Shopify-Access-Token": args.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    source_locations = [name.strip() for name in args.source_locations.split(",") if name.strip()]

    updater = ShopifyInventoryUpdater(
        session=session,
        store_domain=args.store_domain,
        api_version=args.api_version,
        target_location=args.target_location,
        source_locations=source_locations,
        dry_run=args.dry_run,
    )

    try:
        updater.run(args.product_query)
    except Exception as exc:  # pragma: no cover - CLI entry point
        logging.getLogger(__name__).error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - script entry point
    sys.exit(main())
