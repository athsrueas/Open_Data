# Generic DAO-Space Templates

These are generic DAO-space publish templates derived from a working Geo publisher setup and then sanitized for reuse.

Included:
- `publish-week-type.mjs`
- `publish-week-property.mjs`
- `publish-learn-tab.mjs`

## What They Demonstrate

- publishing to a DAO space with proposal flow
- deriving the caller's personal-space ID from the smart-account address
- creating schema objects
- creating UI surfaces like pages and data blocks

## How They Work

These templates read from `.env`, not from any prefilled personal or DAO-space values.

They expect at least:
- `GEO_PRIVATE_KEY`
- `GEO_TARGET_SPACE_ID`
- `GEO_TARGET_SPACE_ADDRESS`
- `GEO_TARGET_SPACE_NAME`
- `GEO_TARGET_SPACE_ENTITY_ID`

Optional:
- `GEO_TARGET_PAGE_TYPE_ID`

They are examples to adapt, not one-click production scripts.

## Practical Caution

One live-session lesson was that after creating a data block, the block source or filter still needed a quick UI correction.

So if a curator adapts these scripts:
- publish
- open the result in Geo
- verify the block is scoped to the intended space
