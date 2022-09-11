import { error, json } from "@sveltejs/kit";
import operators from "$lib/data/operators.json";

export function GET({ url }) {
    const charId = url.searchParams.get("id");
    const charData = operators?.[charId];
    if (charData) return json({
        data: charData.name
    })
    throw error(400, "Invalid character ID");
}