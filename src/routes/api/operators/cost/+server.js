import { error, json } from "@sveltejs/kit";
import operators from "$lib/data/operators.json";

export function GET({ url }) {
    const charId = url.searchParams.get("id");
    const upgradeName = url.searchParams.get("upgrade");
    const upgradeCost = operators?.[charId].costs?.[upgradeName];
    if (upgradeCost) return json(upgradeCost);
    throw error(400, "Invalid query parameters");
}