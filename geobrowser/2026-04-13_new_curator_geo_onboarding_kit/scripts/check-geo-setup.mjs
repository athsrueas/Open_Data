import { fileURLToPath } from "node:url";
import dotenv from "dotenv";

import { createPublicClient, http } from "viem";
import {
  TESTNET_RPC_URL,
  getSmartAccountWalletClient,
  personalSpace,
} from "@geoprotocol/geo-sdk";
import { SpaceRegistryAbi } from "@geoprotocol/geo-sdk/abis";
import { TESTNET } from "@geoprotocol/geo-sdk/contracts";

dotenv.config({
  path: fileURLToPath(new URL("../.env", import.meta.url)),
});

function normalizePrivateKey(value) {
  if (!value) return null;
  return value.startsWith("0x") ? value : `0x${value}`;
}

const privateKey = normalizePrivateKey(process.env.GEO_PRIVATE_KEY);

if (!privateKey) {
  console.error(
    "Missing GEO_PRIVATE_KEY. Copy .env.example to .env and fill it first."
  );
  process.exit(1);
}

const wallet = await getSmartAccountWalletClient({
  privateKey,
});

const smartAccountAddress = wallet.account.address;
const publicClient = createPublicClient({
  transport: http(TESTNET_RPC_URL),
});

const hasPersonalSpace = await personalSpace.hasSpace({
  address: smartAccountAddress,
});

let derivedPersonalSpaceId = null;

if (hasPersonalSpace) {
  const callerSpaceIdHex = await publicClient.readContract({
    address: TESTNET.SPACE_REGISTRY_ADDRESS,
    abi: SpaceRegistryAbi,
    functionName: "addressToSpaceId",
    args: [smartAccountAddress],
  });

  derivedPersonalSpaceId = String(callerSpaceIdHex).slice(2, 34).toLowerCase();
}

const envPersonalSpaceId = process.env.GEO_PERSONAL_SPACE_ID || null;
const personalSpaceMismatch =
  Boolean(envPersonalSpaceId) &&
  Boolean(derivedPersonalSpaceId) &&
  envPersonalSpaceId !== derivedPersonalSpaceId;

const summary = {
  ok: hasPersonalSpace && !personalSpaceMismatch,
  smartAccountAddress,
  hasPersonalSpace,
  derivedPersonalSpaceId,
  envPersonalSpaceId,
  personalSpaceMismatch,
  walletFieldPresent: Boolean(process.env.GEO_WALLET),
  targetSpaceConfigured: Boolean(process.env.GEO_TARGET_SPACE_ID),
  targetSpace: {
    id: process.env.GEO_TARGET_SPACE_ID || null,
    address: process.env.GEO_TARGET_SPACE_ADDRESS || null,
    name: process.env.GEO_TARGET_SPACE_NAME || null,
    pageId: process.env.GEO_TARGET_SPACE_PAGE_ID || null,
  },
  network: process.env.GEO_NETWORK || "TESTNET",
};

console.log(JSON.stringify(summary, null, 2));

if (!hasPersonalSpace) {
  console.error(
    "No personal space found for this smart-account address. Create one in Geo first."
  );
  process.exit(1);
}

if (personalSpaceMismatch) {
  console.error(
    "GEO_PERSONAL_SPACE_ID does not match the derived personal space ID. Update .env."
  );
  process.exit(1);
}
